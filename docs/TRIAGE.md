# Triage Guide

How issues and PRs flow through the RivalSearchMCP repository.

## Label taxonomy

The canonical source is `.github/labels.yml`. Four namespaces:

| Namespace | Purpose | Pick |
|---|---|---|
| `type:*` | What kind of work it is | one |
| `P0..P3` | Priority | one |
| `tool:*` | Which MCP tool it touches | zero or more |
| `status:*` | Where it is in the workflow | one |

### Type

- **`type:bug`** — Documented behavior doesn't match actual behavior.
- **`type:feature`** — Wholly new capability that didn't exist before.
- **`type:enhancement`** — Improvement to existing functionality.
- **`type:docs`** — Documentation-only changes.
- **`type:chore`** — Repo plumbing, deps, config, CI.
- **`type:refactor`** — Restructure without behavior change.

### Priority

- **`P0-critical`** — Production-breaking or a default tool returns zero useful results. Drop everything.
- **`P1-high`** — Significant functionality degraded; should fix this iteration.
- **`P2-medium`** — Should fix soon but workarounds exist.
- **`P3-low`** — Nice-to-have, no clear timeline.

### Tool / area

One label per MCP tool the change touches. A PR that updates two tools gets two `tool:*` labels. Pull from the list in `.github/labels.yml`.

### Status

- **`status:needs-triage`** — Default for fresh issues.
- **`status:in-progress`** — Someone is actively working on it.
- **`status:blocked`** — Cannot proceed until another issue is resolved.

## Workflow

1. **Issue opened** → bot (or maintainer) applies `type:*`, `tool:*`, and either `status:needs-triage` or a priority.
2. **Work begins** → assignee added, `status:in-progress` applied.
3. **PR opened** → references the issue with `Fixes #N`, inherits `tool:*` labels via the path-based auto-labeler.
4. **PR merged** → issue auto-closes via the `Fixes #N` link.

## Quick triage rules of thumb

- A MCP tool returning **0 results** when documented to work → `P0-critical` or `P1-high` depending on how many users hit it.
- Schema/contract change visible to clients → must include `type:feature` or `type:enhancement` and updated docs.
- Anything touching `src/core/<area>/` should get `tool:<area>` automatically once the path-based labeler is wired up.
