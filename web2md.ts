#!/usr/bin/env bun
import { JSDOM } from "jsdom";
import { Readability } from "@mozilla/readability";
import TurndownService from "turndown";
import { chromium } from "playwright";

const args = process.argv.slice(2);

// Check for --version flag first
if (args.includes("--version") || args.includes("-v")) {
  console.log("web2md v1.0.0");
  process.exit(0);
}

const jsIndex = args.indexOf("--js");
const outIndex = args.indexOf("--out");
const flags = {
  js: jsIndex !== -1,
  out: outIndex !== -1 ? args[outIndex + 1] : null,
};

// URL is the first arg that's not a flag
const url = args.find(
  (arg) => arg !== "--js" && arg !== "--out" && !arg.startsWith("--out="),
);

if (!url) {
  console.error("Usage: web2md <URL> [--js] [--out <file>]");
  process.exit(1);
}

async function fetchHTML(targetUrl: string): Promise<string> {
  // Suporte a arquivos locais (file://)
  if (targetUrl.startsWith("file://")) {
    const filePath = targetUrl.replace("file://", "");
    const file = Bun.file(filePath);
    return await file.text();
  }

  // Suporte a caminhos locais (sem file://)
  if (!targetUrl.startsWith("http")) {
    const file = Bun.file(targetUrl);
    return await file.text();
  }

  // GitHub-specific: use raw.githubusercontent.com for better performance
  if (targetUrl.includes('github.com') && targetUrl.includes('/blob/')) {
    const rawUrl = targetUrl
      .replace('github.com', 'raw.githubusercontent.com')
      .replace('/blob/', '/');
    console.error(`[DEBUG] Using GitHub raw URL: ${rawUrl}`);
    const response = await fetch(rawUrl);
    if (response.ok) return await response.text();
    console.error(`[DEBUG] Raw URL failed, falling back to browser`);
  }

  // Suporte a URLs HTTP/HTTPS
  if (flags.js) {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    try {
      await page.goto(targetUrl, {
        waitUntil: "networkidle",
        timeout: 30000 // Increased timeout
      });

      // GitHub-specific: wait for dynamic content to load
      if (targetUrl.includes('github.com')) {
        await page.waitForSelector('markdown-body, .markdown-body, [data-testid="markdown-content"], .file-content', {
          timeout: 10000
        }).catch(() => {
          // Fallback: wait for any content
          return page.waitForTimeout(2000);
        });
      }

      const html = await page.content();
      await browser.close();
      return html;
    } catch (error) {
      await browser.close();
      throw error;
    }
  }
  const response = await fetch(targetUrl);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return await response.text();
}

function parseToMarkdown(html: string): string {
  // Criar URL válida para JSDOM (usar file:// para arquivos locais)
  let jsdomUrl = url;
  if (!url.startsWith("http")) {
    // Para arquivos locais, criar URL file:// válida
    const absolutePath = Bun.file(url).name || url;
    jsdomUrl = `file://${absolutePath}`;
  }

  const dom = new JSDOM(html, { url: jsdomUrl });
  const document = dom.window.document;

  // GitHub-specific: use custom selectors as Readability fails
  if (url.includes('github.com')) {
    const githubSelectors = [
      'markdown-body',
      '.markdown-body',
      '[data-testid="markdown-content"]',
      '.file-content',
      'article.markdown-body',
      '.Box-body .markdown-body'
    ];

    for (const selector of githubSelectors) {
      const element = document.querySelector(selector);
      if (element?.textContent) {
        const turndown = new TurndownService({
          headingStyle: "atx",
          codeBlockStyle: "fenced",
        });
        return turndown.turndown(element.innerHTML);
      }
    }
  }

  const article = new Readability(document).parse();
  if (!article?.content) throw new Error("No content found");
  const turndown = new TurndownService({
    headingStyle: "atx",
    codeBlockStyle: "fenced",
  });
  return turndown.turndown(article.content);
}

async function main() {
  try {
    console.error(`[DEBUG] Fetching: ${url}`);
    const html = await fetchHTML(url);
    console.error(`[DEBUG] HTML length: ${html.length}`);

    console.error(`[DEBUG] Parsing to markdown...`);
    const markdown = parseToMarkdown(html);
    console.error(`[DEBUG] Markdown length: ${markdown.length}`);

    if (flags.out) {
      await Bun.write(flags.out, markdown);
      console.error(`[DEBUG] Written to: ${flags.out}`);
    } else {
      console.log(markdown);
    }
  } catch (error: any) {
    // Specific error handling
    if (error.name === "TimeoutError") {
      console.error(`Timeout: ${url}`);
      process.exit(2);
    }
    if (error.code === "ENOTFOUND" || error.code === "ECONNREFUSED") {
      console.error(`Network error: ${url}`);
      process.exit(3);
    }
    if (error.message?.includes("HTTP")) {
      console.error(`HTTP error: ${error.message}`);
      process.exit(4);
    }
    // Generic fallback
    console.error(String(error));
    process.exit(1);
  }
}

main();
