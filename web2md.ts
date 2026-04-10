#!/usr/bin/env bun
import { JSDOM } from "jsdom";
import { Readability } from "@mozilla/readability";
import TurndownService from "turndown";
import { chromium } from "playwright";

const args = process.argv.slice(2);
const url = args[0];
const outIndex = args.indexOf("--out");
const flags = {
  js: args.includes("--js"),
  out: outIndex !== -1 ? args[outIndex + 1] : null,
};

if (!url) {
  console.error("Usage: web2md <URL> [--js] [--out <file>]");
  process.exit(1);
}

async function fetchHTML(targetUrl: string): Promise<string> {
  if (flags.js) {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto(targetUrl, { waitUntil: "networkidle" });
    const html = await page.content();
    await browser.close();
    return html;
  }
  const response = await fetch(targetUrl);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return await response.text();
}

function parseToMarkdown(html: string): string {
  const dom = new JSDOM(html, { url });
  const document = dom.window.document;
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
  } catch (error) {
    console.error(String(error));
    process.exit(1);
  }
}

main();
