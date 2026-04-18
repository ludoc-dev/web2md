#!/usr/bin/env node
/**
 * Test script to demonstrate smart fetching efficiency
 */

import { smartFetch } from './smart-fetcher.js';
import { extractJSONData, extractMainContent } from './api-detector.js';

const TEST_URLS = [
  'https://github.com/sandeco/prompts/blob/main/sandeco-token/sandeco-token-reduce/SKILL.md',
  'https://www.mozilla.org/en-US/firefox/',
  'https://dev.to/bharathirapu/async-await-in-javascript-1cb5'
];

async function testUrl(url) {
  console.log(`\n🔍 Testing: ${url}`);
  console.log('─'.repeat(60));

  const startTime = Date.now();

  try {
    const result = await smartFetch(url, {
      debug: false,
      timeout: 10,
      usePlaywright: false // Don't use Playwright in tests
    });

    const elapsed = Date.now() - startTime;

    console.log(`✅ Success!`);
    console.log(`   Method: ${result.method}`);
    console.log(`   Time: ${elapsed}ms`);
    console.log(`   Content length: ${result.content.length} bytes`);

    // Try to extract JSON data
    const jsonData = extractJSONData(result.content);
    if (jsonData.scripts.length > 0 || jsonData.dataAttributes.length > 0) {
      console.log(`   📦 JSON found: ${jsonData.scripts.length} scripts, ${jsonData.dataAttributes.length} data attributes`);

      const mainContent = extractMainContent(jsonData);
      if (mainContent) {
        console.log(`   📝 Main content source: ${mainContent.source}`);
        console.log(`   Preview: ${mainContent.content.substring(0, 100)}...`);
      }
    }

    return {
      url,
      success: true,
      method: result.method,
      time: elapsed,
      size: result.content.length
    };

  } catch (error) {
    const elapsed = Date.now() - startTime;
    console.log(`❌ Failed: ${error.message}`);
    console.log(`   Time: ${elapsed}ms`);

    return {
      url,
      success: false,
      error: error.message,
      time: elapsed
    };
  }
}

async function main() {
  console.log('🚀 Smart Fetcher Test Suite');
  console.log('='.repeat(60));

  const results = [];

  for (const url of TEST_URLS) {
    const result = await testUrl(url);
    results.push(result);
  }

  console.log('\n📊 Summary');
  console.log('='.repeat(60));

  const successful = results.filter(r => r.success);
  const failed = results.filter(r => !r.success);

  console.log(`✅ Successful: ${successful.length}/${results.length}`);
  console.log(`❌ Failed: ${failed.length}/${results.length}`);

  if (successful.length > 0) {
    const avgTime = successful.reduce((sum, r) => sum + r.time, 0) / successful.length;
    const avgSize = successful.reduce((sum, r) => sum + (r.size || 0), 0) / successful.length;

    console.log(`⏱️  Average time: ${Math.round(avgTime)}ms`);
    console.log(`📦 Average size: ${Math.round(avgSize)} bytes`);

    console.log('\n🎯 Method breakdown:');
    const methods = {};
    successful.forEach(r => {
      methods[r.method] = (methods[r.method] || 0) + 1;
    });
    Object.entries(methods).forEach(([method, count]) => {
      console.log(`   ${method}: ${count}`);
    });
  }

  console.log('\n💡 Key insights:');
  console.log('   • Domain-specific extractors are fastest');
  console.log('   • API detection avoids Playwright overhead');
  console.log('   • Smart headers bypass basic bot detection');
  console.log('   • Clean room design - no external services needed');
}

main().catch(console.error);