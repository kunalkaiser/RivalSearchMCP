# Plugins

This directory contains installable agent plugin packages published from this repository.

The repository root is the marketplace for both supported clients:

- Claude Code reads `.claude-plugin/marketplace.json`
- OpenAI Codex reads `.agents/plugins/marketplace.json`

The marketplace catalogs expose two plugin packages:

- `plugins/rival-search-mcp` registers the hosted MCP server.
- `plugins/rival-search-mcp-skills` ships the standalone agent skill and CLI helpers.

## Install

Claude Code:

```bash
claude plugin marketplace add damionrashford/RivalSearchMCP --scope user
claude plugin install rival-search-mcp@rivalsearchmcp --scope user
claude plugin install rival-search-mcp-skills@rivalsearchmcp --scope user
```

OpenAI Codex:

```bash
codex plugin marketplace add damionrashford/RivalSearchMCP --ref main
codex plugin add rival-search-mcp@rival-search-mcp-marketplace
codex plugin add rival-search-mcp-skills@rival-search-mcp-marketplace
```

The MCP plugin registers the hosted RivalSearchMCP server at `https://RivalSearchMCP.fastmcp.app/mcp`.
The skills plugin installs agent instructions and CLI helpers. Users do not need to clone this repository or run the server locally.
