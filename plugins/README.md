# Plugins

This directory contains installable agent plugin packages published from this repository.

The repository root is the marketplace for both supported clients:

- Claude Code reads `.claude-plugin/marketplace.json`
- OpenAI Codex reads `.agents/plugins/marketplace.json`

Both marketplace catalogs point to `plugins/rival-search-mcp`, which is the actual plugin package users install.

## Install

Claude Code:

```bash
claude plugin marketplace add damionrashford/RivalSearchMCP --scope user
claude plugin install rival-search-mcp@rivalsearchmcp --scope user
```

OpenAI Codex:

```bash
codex plugin marketplace add damionrashford/RivalSearchMCP --ref main
codex plugin add rival-search-mcp@rival-search-mcp-marketplace
```

The plugin registers the hosted RivalSearchMCP server at `https://RivalSearchMCP.fastmcp.app/mcp`.
Users do not need to clone this repository or run the server locally.
