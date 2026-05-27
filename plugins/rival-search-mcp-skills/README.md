# RivalSearch MCP Skills Plugin

This is the standalone skill plugin for RivalSearchMCP.

It packages the `rival-search-mcp` agent skill, reference docs, and CLI helper scripts without registering an MCP server. Install this when you want workflow guidance and CLI access separately from the MCP plugin.

## Package Files

- `.claude-plugin/plugin.json` is the Claude Code plugin manifest.
- `.codex-plugin/plugin.json` is the OpenAI Codex plugin manifest.
- `skills/rival-search-mcp/` contains the skill, resources, and CLI.

## Install

Claude Code:

```bash
claude plugin marketplace add damionrashford/RivalSearchMCP --scope user
claude plugin install rival-search-mcp-skills@rivalsearchmcp --scope user
```

OpenAI Codex:

```bash
codex plugin marketplace add damionrashford/RivalSearchMCP --ref main
codex plugin add rival-search-mcp-skills@rival-search-mcp-marketplace
```

For MCP tool registration, install the separate `rival-search-mcp` plugin.
