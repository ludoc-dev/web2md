#!/usr/bin/env node
/**
 * API Detector - Automatically discovers hidden JSON APIs in web pages
 *
 * This module analyzes HTML to find:
 * - JSON data in script tags (application/ld+json, application/json)
 * - Data attributes with JSON content
 * - Inline JavaScript with JSON objects
 * - XHR/Fetch requests in network (requires browser)
 */

/**
 * Extract all JSON data from HTML
 */
export function extractJSONData(html) {
  const results = {
    scripts: [],
    dataAttributes: [],
    inline: [],
    metadata: {}
  };

  // 1. Script tags with JSON
  const scriptRegex = /<script[^>]*type=["']application\/(ld\+json|json)["'][^>]*>(.*?)<\/script>/gs;
  let match;

  while ((match = scriptRegex.exec(html)) !== null) {
    try {
      const data = JSON.parse(match[2]);
      results.scripts.push({
        type: match[1],
        data: sanitizeData(data)
      });
    } catch (error) {
      // Invalid JSON, skip
    }
  }

  // 2. Data attributes with JSON
  const dataAttrRegex = /data-([a-z-]+)=(["'])((?:\\.|[^"\\\2])*?)\2/gi;
  while ((match = dataAttrRegex.exec(html)) !== null) {
    try {
      const value = unescapeHtml(match[3]);
      if ((value.startsWith('{') && value.endsWith('}')) ||
          (value.startsWith('[') && value.endsWith(']'))) {
        const data = JSON.parse(value);
        results.dataAttributes.push({
          attribute: match[1],
          data: sanitizeData(data)
        });
      }
    } catch (error) {
      // Invalid JSON, skip
    }
  }

  // 3. Inline JavaScript with JSON objects
  const inlineRegex = /(?:const|let|var)\s+(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\[(?:[^\[\]]|\[[^\[\]]*\])*\])/g;
  while ((match = inlineRegex.exec(html)) !== null) {
    try {
      const data = JSON.parse(match[2]);
      results.inline.push({
        variable: match[1],
        data: sanitizeData(data)
      });
    } catch (error) {
      // Invalid JSON, skip
    }
  }

  // 4. Look for common metadata patterns
  const metadataPatterns = {
    'title': /<title>(.*?)<\/title>/i,
    'description': /<meta[^>]*name=["']description["'][^>]*content=["'](.*?)["']/i,
    'og:title': /<meta[^>]*property=["']og:title["'][^>]*content=["'](.*?)["']/i,
    'og:description': /<meta[^>]*property=["']og:description["'][^>]*content=["'](.*?)["']/i,
    'article:published_time': /<meta[^>]*property=["']article:published_time["'][^>]*content=["'](.*?)["']/i,
    'author': /<meta[^>]*name=["']author["'][^>]*content=["'](.*?)["']/i
  };

  for (const [key, pattern] of Object.entries(metadataPatterns)) {
    const metaMatch = html.match(pattern);
    if (metaMatch) {
      results.metadata[key] = metaMatch[1];
    }
  }

  return results;
}

/**
 * Sanitize JSON data to avoid circular references and huge objects
 */
function sanitizeData(data, maxDepth = 10, currentDepth = 0) {
  if (currentDepth >= maxDepth) {
    return '[Max depth reached]';
  }

  if (data === null || typeof data !== 'object') {
    return data;
  }

  if (Array.isArray(data)) {
    return data.slice(0, 100).map(item =>
      sanitizeData(item, maxDepth, currentDepth + 1)
    );
  }

  const sanitized = {};
  for (const [key, value] of Object.entries(data)) {
    if (typeof value === 'object' && value !== null) {
      try {
        JSON.stringify(value);
        sanitized[key] = sanitizeData(value, maxDepth, currentDepth + 1);
      } catch {
        sanitized[key] = '[Circular or complex object]';
      }
    } else {
      sanitized[key] = value;
    }
  }

  return sanitized;
}

/**
 * Unescape HTML entities
 */
function unescapeHtml(str) {
  return str
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&');
}

/**
 * Extract main content from JSON data
 */
export function extractMainContent(jsonData) {
  const allData = [
    ...jsonData.scripts,
    ...jsonData.dataAttributes,
    ...jsonData.inline
  ];

  // Priority fields for content extraction
  const contentFields = [
    'articleBody',
    'content',
    'text',
    'description',
    'body',
    'html',
    'markdown',
    'articleBody',
    'mainContent'
  ];

  for (const item of allData) {
    const data = item.data;

    // Check direct fields
    for (const field of contentFields) {
      if (data[field]) {
        return {
          content: data[field],
          source: `${item.type || item.variable || 'unknown'}.${field}`,
          metadata: jsonData.metadata
        };
      }
    }

    // Check nested objects
    for (const field of contentFields) {
      if (data.props?.[field]) {
        return {
          content: data.props[field],
          source: `${item.type || item.variable || 'unknown'}.props.${field}`,
          metadata: jsonData.metadata
        };
      }
    }

    // Check arrays of objects
    if (Array.isArray(data)) {
      for (const obj of data) {
        for (const field of contentFields) {
          if (obj[field]) {
            return {
              content: obj[field],
              source: `array.${field}`,
              metadata: jsonData.metadata
            };
          }
        }
      }
    }
  }

  return null;
}

/**
 * Detect if URL might have an API endpoint
 */
export function detectApiPatterns(url) {
  const patterns = {
    rest: /\/api\/v?\d*\//i,
    graphql: /\/graphql\?/i,
    json: /\.json(?:\?|$)/i,
    rpc: /\/rpc\//i,
    wp: /\/wp-json\//i
  };

  const detected = [];

  for (const [name, pattern] of Object.entries(patterns)) {
    if (pattern.test(url)) {
      detected.push(name);
    }
  }

  return detected;
}

/**
 * Generate API URLs from a given URL
 */
export function generateApiUrls(url) {
  const urls = [];
  const parsedUrl = new URL(url);

  // Common API patterns
  const patterns = [
    '/api/v1/',
    '/api/v2/',
    '/api/',
    '/wp-json/wp/v2/posts',
    '/_api/',
    '/__api__'
  ];

  for (const pattern of patterns) {
    const apiUrl = `${parsedUrl.origin}${pattern}${parsedUrl.pathname}`;
    urls.push(apiUrl);
  }

  // Try adding .json
  urls.push(url.replace(/\/$/, '') + '.json');
  urls.push(url + '?format=json');

  return urls;
}

export default {
  extractJSONData,
  extractMainContent,
  detectApiPatterns,
  generateApiUrls
};