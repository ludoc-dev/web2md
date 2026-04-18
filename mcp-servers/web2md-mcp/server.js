#!/usr/bin/env node
/**
 * web2md MCP Server
 *
 * Model Context Protocol server for web2md functionality
 * Converts web content to clean Markdown with advanced features
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { JSDOM } from "jsdom";
import { Readability } from "@mozilla/readability";
import TurndownService from "turndown";
import { chromium } from "playwright";

// Cache with TTL management
const cache = new Map();
const CACHE_TTL = 3600000; // 1 hour default

// MCP Server instance
const server = new Server(
  {
    name: "web2md-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

/**
 * Fetch HTML from URL or file with timeout and JS rendering support
 */
async function fetchHTML(targetUrl, useJS = false, timeoutMs = 20000) {
  // Support local files (file://)
  if (targetUrl.startsWith("file://")) {
    const filePath = targetUrl.replace("file://", "");
    const fs = await import("fs");
    return fs.readFileSync(filePath, "utf-8");
  }

  // Support local paths (without file://)
  if (!targetUrl.startsWith("http")) {
    const fs = await import("fs");
    return fs.readFileSync(targetUrl, "utf-8");
  }

  // Check cache first for HTTP URLs
  const cacheKey = `${targetUrl}-${useJS}`;
  if (cache.has(cacheKey)) {
    const cached = cache.get(cacheKey);
    if (Date.now() - cached.timestamp < CACHE_TTL) {
      return cached.data;
    } else {
      cache.delete(cacheKey);
    }
  }

  let html;

  // Support HTTP/HTTPS URLs
  if (useJS) {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    try {
      await page.goto(targetUrl, {
        waitUntil: "networkidle",
        timeout: timeoutMs
      });
      html = await page.content();
    } finally {
      await browser.close();
    }
  } else {
    // Simple HTTP fetch
    const response = await fetch(targetUrl, { signal: AbortSignal.timeout(timeoutMs) });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    html = await response.text();
  }

  // Cache the result
  cache.set(cacheKey, {
    data: html,
    timestamp: Date.now()
  });

  return html;
}

/**
 * Parse HTML to clean Markdown using Readability + Turndown
 */
function parseToMarkdown(html, baseUrl) {
  // Create valid URL for JSDOM
  let jsdomUrl = baseUrl;
  if (!baseUrl.startsWith("http")) {
    jsdomUrl = `file://${baseUrl}`;
  }

  const dom = new JSDOM(html, { url: jsdomUrl });
  const document = dom.window.document;

  const article = new Readability(document).parse();
  if (!article?.content) {
    throw new Error("No content found - page might be JavaScript-heavy or blocked");
  }

  const turndown = new TurndownService({
    headingStyle: "atx",
    codeBlockStyle: "fenced",
  });

  return turndown.turndown(article.content);
}

/**
 * Convert URL or file to clean Markdown
 */
async function convertToMarkdown(url, options = {}) {
  const startTime = Date.now();
  const { js = false, timeout = 20 } = options;

  const html = await fetchHTML(url, js, timeout * 1000);
  const markdown = parseToMarkdown(html, url);
  const processingTime = Date.now() - startTime;

  return {
    content: markdown,
    url,
    length: markdown.length,
    processingTime,
    jsRendering: js,
    timestamp: new Date().toISOString()
  };
}

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "web2md_convert",
        description: "Convert a URL or file to clean Markdown. Removes ads, navbars, and noise while preserving article structure.",
        inputSchema: {
          type: "object",
          properties: {
            url: {
              type: "string",
              description: "HTTP/HTTPS URL or local file path to convert"
            },
            js: {
              type: "boolean",
              description: "Enable JavaScript rendering for SPAs (slower, uses Playwright)",
              default: false
            },
            timeout: {
              type: "number",
              description: "Timeout in seconds (default: 20)",
              default: 20
            }
          },
          required: ["url"]
        }
      },
      {
        name: "web2md_batch",
        description: "Convert multiple URLs to Markdown in batch. Returns array of conversion results.",
        inputSchema: {
          type: "object",
          properties: {
            urls: {
              type: "array",
              items: {
                type: "string"
              },
              description: "Array of URLs to convert"
            },
            js: {
              type: "boolean",
              description: "Enable JavaScript rendering for all URLs",
              default: false
            },
            timeout: {
              type: "number",
              description: "Timeout in seconds per URL (default: 20)",
              default: 20
            }
          },
          required: ["urls"]
        }
      },
      {
        name: "web2md_status",
        description: "Check cache status and performance metrics",
        inputSchema: {
          type: "object",
          properties: {
            clearCache: {
              type: "boolean",
              description: "Clear the cache before returning status",
              default: false
            }
          }
        }
      },
      {
        name: "web2md_convert_file",
        description: "Convert a local file to Markdown. Supports HTML files and text files.",
        inputSchema: {
          type: "object",
          properties: {
            filePath: {
              type: "string",
              description: "Local file path to convert"
            }
          },
          required: ["filePath"]
        }
      }
    ]
  };
});

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "web2md_convert": {
        const result = await convertToMarkdown(args.url, {
          js: args.js || false,
          timeout: args.timeout || 20
        });
        return {
          content: [{
            type: "text",
            text: JSON.stringify(result, null, 2)
          }]
        };
      }

      case "web2md_batch": {
        const results = [];
        for (const url of args.urls) {
          try {
            const result = await convertToMarkdown(url, {
              js: args.js || false,
              timeout: args.timeout || 20
            });
            results.push(result);
          } catch (error) {
            results.push({
              url,
              error: error.message,
              length: 0,
              processingTime: 0,
              jsRendering: args.js || false,
              timestamp: new Date().toISOString()
            });
          }
        }
        return {
          content: [{
            type: "text",
            text: JSON.stringify(results, null, 2)
          }]
        };
      }

      case "web2md_status": {
        if (args.clearCache) {
          cache.clear();
        }

        const status = {
          cacheSize: cache.size,
          cacheEntries: Array.from(cache.keys()).map(key => ({
            key,
            timestamp: cache.get(key).timestamp,
            age: Date.now() - cache.get(key).timestamp
          })),
          totalCacheSize: JSON.stringify(Array.from(cache.values())).length,
          cacheTTL: CACHE_TTL,
          serverInfo: {
            name: "web2md-mcp",
            version: "1.0.0",
            uptime: process.uptime()
          }
        };

        return {
          content: [{
            type: "text",
            text: JSON.stringify(status, null, 2)
          }]
        };
      }

      case "web2md_convert_file": {
        const result = await convertToMarkdown(args.filePath, {
          js: false,
          timeout: 60
        });
        return {
          content: [{
            type: "text",
            text: JSON.stringify(result, null, 2)
          }]
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          error: error.message,
          tool: name,
          arguments: args
        }, null, 2)
      }],
      isError: true
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);

  // Log startup (will go to stderr, not stdout)
  console.error("web2md MCP server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
});
