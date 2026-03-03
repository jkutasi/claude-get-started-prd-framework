# Persistence Patterns — 3-Layer Architecture

> How agents retain and share knowledge within a project, across sessions,
> and across projects. This document describes the architecture and presents
> implementation options with tradeoffs.

---

## The Three Layers

### Layer 1: Project-Level Learnings

**Location:** `learnings/` at the project root

Files:
- `QA_LEARNINGS.md` — Patterns discovered during QA phases
- `BUILD_LEARNINGS.md` — Implementation gotchas, what broke, what worked
- `REVIEW_LEARNINGS.md` — Common peer review findings across slices
- `UX_LEARNINGS.md` — Usability patterns, jargon issues, UI findings

**How it works:** Agents read the relevant learnings file at the start of each
phase. When they discover something reusable — a pattern, a gotcha, a
technique — they append it to the appropriate file. Knowledge accumulates
across slices.

### Layer 2: Agent Session State

**Location:** `reviews/` directory (in-progress files)

**How it works:** During active work, agents write incremental state to review
and working files. If context compacts (token window fills up) or a session
crashes, the agent reads its last state file and resumes from where it left
off. This is the "save game" layer.

### Layer 3: Cross-Project Learnings

**Location:** `~/.claude/memory/` (Claude Code's built-in memory system)

**How it works:** Insights that transcend a single project — general patterns,
tool preferences, workflow optimizations — persist in Claude Code's memory
layer. These are available across all projects.

---

## Implementation Options

Choose the option that fits your project's complexity and team preferences.
All options implement Layer 1 (project learnings). They differ in how
searchable and connected the knowledge becomes.

### Option A: Plain Markdown Files

**The simplest approach. Zero dependencies.**

- Write learnings as structured markdown in the `learnings/` folder
- Git-tracked, human-auditable, agents read and write natively
- No semantic search — the agent must know which file to look in

**Analogy:** A filing cabinet. Organized, labeled, you know where things are.
But you have to know which drawer to open. If you're looking for "that thing
about polling endpoints," you need to know it's in BUILD_LEARNINGS.md.

**Best for:** Most projects, especially when starting out. Start here and
upgrade only if you hit limitations.

### Option B: Obsidian + Obsidian MCP

**Structured knowledge navigation with links and graphs.**

- Obsidian stores notes as plain markdown but adds: bidirectional linking,
  graph visualization, full-text and tag search, a rich plugin ecosystem
- With the Obsidian MCP server, agents can search notes semantically,
  follow links between concepts, and see the knowledge graph
- Notes remain human-readable markdown files on disk

**Analogy:** A research wiki with hyperlinks and a map. Everything is
connected, you can browse relationships, search by concept. It is a knowledge
graph — not just storage but structure.

**Best for:** Projects with complex domain knowledge. Teams that want to
visualize how learnings connect across slices, agents, and concepts.

### Option C: Mem0 (AI-Native Memory Layer)

**Purpose-built memory service for AI agents.**

- Automatically stores, retrieves, and ranks memories by relevance
- Agent says "remember this" and Mem0 handles embedding, indexing, retrieval
- Agent asks "what did we learn about X?" and gets the most relevant answer
  without needing to know which file contains it

**Analogy:** A personal assistant with perfect recall. You ask "what did we
learn about polling endpoints?" and it finds the most relevant answer from
across all stored memories.

**Best for:** Projects where agents need to recall specific past findings
without knowing which file to look in. High-volume projects that generate
many learnings across many slices.

**Tradeoff:** External dependency, API costs, another service to manage.

### Option D: Markdown + Mem0 or Obsidian (Belt and Suspenders)

**Dual-write for maximum coverage.**

- Write to markdown files (human audit trail + git tracking) AND sync to
  Mem0 or Obsidian (semantic retrieval + knowledge navigation)
- Humans and git get the structured files; agents get intelligent search
- Best of both worlds but more complex to maintain

**Best for:** High-stakes projects where both human auditability and agent
recall are critical.

---

## Key Insight

Obsidian and Mem0 serve **different purposes**. They are complementary, not
competitors:

- **Obsidian** = Structured knowledge navigation (links, graphs, relationships).
  You browse and explore. "Show me everything connected to authentication."
- **Mem0** = Automatic relevance retrieval (ask question, get best answer).
  You query and receive. "What went wrong last time we used WebSockets?"

Most projects should **start with Option A** (plain markdown) and upgrade to
B, C, or D only when the volume or complexity of learnings demands it.
