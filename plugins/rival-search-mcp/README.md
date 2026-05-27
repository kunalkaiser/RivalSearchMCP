# RivalSearch MCP Plugin

This is the distributable plugin package for RivalSearchMCP.

It installs the hosted MCP server:

```text
https://RivalSearchMCP.fastmcp.app/mcp
```

The plugin exposes 9 research tools for web search, social search, news aggregation, GitHub search, website mapping, content operations, document analysis, topic research, and scientific research.

## Package Files

- `.claude-plugin/plugin.json` is the Claude Code plugin manifest.
- `.codex-plugin/plugin.json` is the OpenAI Codex plugin manifest.
- `.mcp.json` registers the hosted MCP server for Codex.

## Claude Code

Install from the repository marketplace:

```bash
claude plugin marketplace add damionrashford/RivalSearchMCP --scope user
claude plugin install rival-search-mcp@rivalsearchmcp --scope user
```

After installation, Claude Code exposes the tools as `mcp__RivalSearchMCP__*`.

## OpenAI Codex

Install from the repository marketplace:

```bash
codex plugin marketplace add damionrashford/RivalSearchMCP --ref main
codex plugin add rival-search-mcp@rival-search-mcp-marketplace
```

After installation, start or refresh a Codex session and ask Codex to use RivalSearchMCP.
