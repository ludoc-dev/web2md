#!/usr/bin/env node
/**
 * Smart Fetcher - Clean Room, Free, Efficient Web Scraping
 *
 * Strategy hierarchy (fastest to slowest):
 * 1. Direct API detection (hidden JSON endpoints)
 * 2. Static fetch with smart headers
 * 3. Specialized extractors (domain-specific)
 * 4. Readability fallback
 * 5. Playwright (last resort)
 */

import { chromium } from 'playwright';

// Domain-specific extractors (clean room implementations)
const DOMAIN_EXTRACTORS = {
  'github.com': async (url) => {
    // GitHub raw URL pattern
    if (url.includes('/blob/')) {
      const rawUrl = url
        .replace('github.com', 'raw.githubusercontent.com')
        .replace('/blob/', '/');
      return fetch(rawUrl).then(r => r.text());
    }

    // GitHub API for repo data
    if (url.match(/github\.com\/[^\/]+\/[^\/]+$/)) {
      const [, owner, repo] = url.match(/github\.com\/([^\/]+)\/([^\/]+)/);
      const apiUrl = `https://api.github.com/repos/${owner}/${repo}/readme`;
      const response = await fetch(apiUrl, {
        headers: { 'Accept': 'application/vnd.github.v3.html' }
      });
      if (response.ok) {
        const data = await response.json();
        return `<div class="markdown-body">${data.content}</div>`;
      }
    }

    return null;
  },

  'reddit.com': async (url) => {
    // Reddit JSON API (official, free)
    const jsonUrl = url.replace('reddit.com', 'reddit.com') + '.json';
    try {
      const response = await fetch(jsonUrl);
      if (response.ok) {
        const data = await response.json();
        // Extract text from Reddit JSON structure
        const post = data[0]?.data?.children[0]?.data;
        if (post) {
          return `<div><h1>${post.title}</h1><p>${post.selftext_html || ''}</p></div>`;
        }
      }
    } catch {}
    return null;
  },

  'medium.com': async (url) => {
    // Medium has hidden JSON payload
    try {
      const response = await fetch(url);
      const html = await response.text();
      const match = html.match(/<script type="application\/ld\+json">(.*?)<\/script>/s);
      if (match) {
        const data = JSON.parse(match[1]);
        if (data.articleBody) {
          return `<div><article>${data.articleBody}</article></div>`;
        }
      }
    } catch {}
    return null;
  },

  'dev.to': async (url) => {
    // dev.to has official API
    const articleId = url.match(/dev\.to\/[^\/]+\/([^\/]+)/)?.[1];
    if (articleId) {
      try {
        const response = await fetch(`https://dev.to/api/articles/${articleId}`);
        if (response.ok) {
          const data = await response.json();
          return `<div><h1>${data.title}</h1><div class="markdown-body">${data.body_markdown}</div></div>`;
        }
      } catch {}
    }
    return null;
  },

  'stackexchange.com': async (url) => {
    // StackExchange has official API
    const questionId = url.match(/questions\/(\d+)/)?.[1];
    if (questionId) {
      try {
        const response = await fetch(`https://api.stackexchange.com/2.3/questions/${questionId}?order=desc&sort=activity&site=stackoverflow&filter=withbody`);
        if (response.ok) {
          const data = await response.json();
          if (data.items?.[0]) {
            const item = data.items[0];
            return `<div><h1>${item.title}</h1><div class="markdown-body">${item.body}</div></div>`;
          }
        }
      } catch {}
    }
    return null;
  }
};

// Smart headers to bypass basic bot detection
const SMART_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.9,pt;q=0.8',
  'Accept-Encoding': 'gzip, deflate, br',
  'DNT': '1',
  'Connection': 'keep-alive',
  'Upgrade-Insecure-Requests': '1',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'none',
  'Sec-Fetch-User': '?1',
  'Cache-Control': 'max-age=0'
};

/**
 * Detect hidden API endpoints by analyzing HTML patterns
 */
async function detectHiddenAPI(url, html) {
  // Look for JSON data in script tags
  const scriptMatches = html.matchAll(/<script[^>]*type=["']application\/(ld\+json|json)["'][^>]*>(.*?)<\/script>/gs);

  for (const match of scriptMatches) {
    try {
      const data = JSON.parse(match[2]);
      if (data.articleBody || data.content || data.description) {
        return data;
      }
    } catch {}
  }

  // Look for data-* attributes with JSON
  const dataMatches = html.matchAll(/data-([a-z-]+)=(["'])([^"']*?)\2/gi);
  for (const match of dataMatches) {
    try {
      const value = match[3];
      if (value.startsWith('{') || value.startsWith('[')) {
        const data = JSON.parse(value);
        if (data.content || data.text) {
          return data;
        }
      }
    } catch {}
  }

  return null;
}

/**
 * Check for RSS/Atom feeds
 */
async function checkForFeeds(url) {
  const feedPaths = ['/feed', '/rss', '/atom.xml', '/feed.xml', '/rss.xml'];

  for (const path of feedPaths) {
    try {
      const feedUrl = new URL(path, url).toString();
      const response = await fetch(feedUrl, {
        headers: SMART_HEADERS,
        signal: AbortSignal.timeout(5000)
      });

      if (response.ok) {
        const text = await response.text();
        if (text.includes('<rss') || text.includes('<feed') || text.includes('<entry')) {
          return { type: 'feed', content: text, url: feedUrl };
        }
      }
    } catch {}
  }

  return null;
}

/**
 * Main smart fetch function
 */
async function smartFetch(url, options = {}) {
  const {
    timeout = 20000,
    usePlaywright = false,
    debug = false
  } = options;

  const log = (...args) => {
    if (debug) console.error('[SmartFetcher]', ...args);
  };

  // Step 1: Check domain-specific extractors
  const hostname = new URL(url).hostname.replace('www.', '');

  for (const [domain, extractor] of Object.entries(DOMAIN_EXTRACTORS)) {
    if (hostname.includes(domain)) {
      log(`Trying domain-specific extractor for ${domain}`);
      try {
        const result = await extractor(url);
        if (result) {
          log(`✓ Domain extractor succeeded for ${domain}`);
          return {
            content: result,
            method: 'domain-extractor',
            domain
          };
        }
      } catch (error) {
        log(`✗ Domain extractor failed:`, error.message);
      }
    }
  }

  // Step 2: Check for RSS/Atom feeds
  log('Checking for RSS/Atom feeds');
  try {
    const feed = await checkForFeeds(url);
    if (feed) {
      log('✓ Feed found');
      return {
        content: feed.content,
        method: 'feed',
        feedUrl: feed.url
      };
    }
  } catch (error) {
    log('✗ Feed check failed:', error.message);
  }

  // Step 3: Try smart HTTP fetch first
  log('Trying smart HTTP fetch');
  try {
    const response = await fetch(url, {
      headers: SMART_HEADERS,
      signal: AbortSignal.timeout(timeout)
    });

    if (response.ok) {
      const html = await response.text();

      // Check for hidden JSON data
      const hiddenData = await detectHiddenAPI(url, html);
      if (hiddenData) {
        log('✓ Hidden API data found');
        return {
          content: JSON.stringify(hiddenData),
          method: 'hidden-api'
        };
      }

      log('✓ HTTP fetch succeeded');
      return {
        content: html,
        method: 'http-fetch'
      };
    }
  } catch (error) {
    log('✗ HTTP fetch failed:', error.message);
    // Continue to Playwright fallback
  }

  // Step 4: Playwright fallback (only if requested or as last resort)
  if (usePlaywright) {
    log('Using Playwright fallback');
    try {
      const browser = await chromium.launch({ headless: true });
      const page = await browser.newPage();

      await page.goto(url, {
        waitUntil: 'networkidle',
        timeout: timeout
      });

      // GitHub-specific wait
      if (url.includes('github.com')) {
        await page.waitForSelector('markdown-body, .markdown-body, [data-testid="markdown-content"], .file-content', {
          timeout: 10000
        }).catch(() => page.waitForTimeout(2000));
      }

      const html = await page.content();
      await browser.close();

      log('✓ Playwright succeeded');
      return {
        content: html,
        method: 'playwright'
      };
    } catch (error) {
      log('✗ Playwright failed:', error.message);
      throw error;
    }
  }

  throw new Error('All fetch methods failed');
}

export { smartFetch, DOMAIN_EXTRACTORS, SMART_HEADERS };