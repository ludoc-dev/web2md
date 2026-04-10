#!/usr/bin/env node
import { JSDOM } from "jsdom";
import { Readability } from "@mozilla/readability";
import TurndownService from "turndown";
import { chromium } from "playwright";

const args = process.argv.slice(2);
const url = args[0];
const flags = {
  js: args.includes("--js"),
  out: args[args.indexOf("--out") + 1] || null,
};

if (!url) {
  console.error("Usage: web2md <URL> [--js] [--out <file>]");
  process.exit(1);
}

async function fetchHTML(targetUrl) {
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

function parseToMarkdown(html) {
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
    const html = await fetchHTML(url);
    const markdown = parseToMarkdown(html);

    if (flags.out) {
      const fs = await import("fs");
      fs.writeFileSync(flags.out, markdown);
    } else {
      console.log(markdown);
    }
  } catch (error) {
    console.error(String(error));
    process.exit(1);
  }
}

main();
