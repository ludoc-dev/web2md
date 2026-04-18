# web2md MCP Server

Model Context Protocol server for web2md - convert web content to clean Markdown with advanced features.

## Features

- **Single URL Conversion**: Convert any URL to clean Markdown
- **Batch Processing**: Convert multiple URLs efficiently
- **File Support**: Convert local HTML/text files
- **Smart Caching**: TTL-based caching to avoid redundant fetches
- **JavaScript Rendering**: Optional Playwright support for SPAs
- **Status Monitoring**: Track cache metrics and performance

## Installation

```bash
cd /Users/lucascardoso/web2md/mcp-servers/web2md-mcp
npm install
```

## Configuration

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "web2md": {
      "command": "node",
      "args": ["/Users/lucascardoso/web2md/mcp-servers/web2md-mcp/server.js"]
    }
  }
}
```

## Tools

### web2md_convert
Convert a URL or file to clean Markdown.

**Parameters:**
- `url` (required): HTTP/HTTPS URL or local file path
- `js` (optional): Enable JavaScript rendering (default: false)
- `timeout` (optional): Timeout in seconds (default: 20)

**Example:**
```json
{
  "url": "https://example.com/article",
  "js": false,
  "timeout": 30
}
```

### web2md_batch
Convert multiple URLs to Markdown.

**Parameters:**
- `urls` (required): Array of URLs to convert
- `js` (optional): Enable JavaScript rendering for all (default: false)
- `timeout` (optional): Timeout per URL in seconds (default: 20)

**Example:**
```json
{
  "urls": [
    "https://example.com/page1",
    "https://example.com/page2"
  ],
  "js": false,
  "timeout": 20
}
```

### web2md_convert_file
Convert a local file to Markdown.

**Parameters:**
- `filePath` (required): Local file path

**Example:**
```json
{
  "filePath": "/path/to/file.html"
}
```

### web2md_status
Check cache status and performance metrics.

**Parameters:**
- `clearCache` (optional): Clear cache before returning status (default: false)

**Example:**
```json
{
  "clearCache": false
}
```

## Usage Examples

### Convert Single URL
```typescript
const result = await mcpClient.callTool("web2md_convert", {
  url: "https://example.com"
});
```

### Batch Convert Multiple URLs
```typescript
const results = await mcpClient.callTool("web2md_batch", {
  urls: [
    "https://docs.example.com/page1",
    "https://docs.example.com/page2",
    "https://docs.example.com/page3"
  ]
});
```

### Convert Local File
```typescript
const result = await mcpClient.callTool("web2md_convert_file", {
  filePath: "/path/to/document.html"
});
```

### Check Cache Status
```typescript
const status = await mcpClient.callTool("web2md_status", {
  clearCache: false
});
```

## Response Format

All tools return JSON with the following structure:

```json
{
  "content": "Clean Markdown content",
  "url": "Source URL",
  "length": 8156,
  "processingTime": 916,
  "jsRendering": false,
  "timestamp": "2026-04-14T12:00:00.000Z"
}
```

## Cache Behavior

- Cache entries expire after 1 hour (TTL)
- Cache is shared between all operations
- Cache key includes URL and JS rendering flag
- Use `web2md_status` to monitor cache

## Performance

- **Simple pages**: ~0.1-0.5 seconds
- **JavaScript pages**: ~2-5 seconds (with `js: true`)
- **Cached requests**: ~0.01 seconds
- **Token efficiency**: 90%+ reduction vs raw HTML

## Error Handling

All errors are returned in the response:

```json
{
  "error": "HTTP 404: Not Found",
  "tool": "web2md_convert",
  "arguments": {
    "url": "https://example.com"
  }
}
```

## Integration with web2md

This MCP server uses the same underlying logic as the web2md wrapper:
- Mozilla Readability for content extraction
- Turndown for HTML to Markdown conversion
- JSDOM for DOM parsing
- Playwright for JavaScript rendering

## Complementarity

This MCP server is designed to complement the MCP Web Reader:
- **web2md-mcp**: JavaScript rendering, local files, batch processing, caching
- **MCP Web Reader**: URLs only, cache control, images/links summary

Use both together for complete web content extraction coverage.
