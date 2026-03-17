---
phase: 05-architecture-diagrams-and-technical-foundation
plan: 02
subsystem: ui
tags: [html, css, lifecycle-diagram, inference-routing, nemoclaw, responsive]

# Dependency graph
requires:
  - phase: 05-01
    provides: "NemoClaw Architecture section with SVG diagram and id=nemoclaw-architecture"
provides:
  - Sandbox Lifecycle 5-stage horizontal pipeline inside #nemoclaw-architecture section
  - Inference Routing 3-card grid (NVIDIA Cloud, Local NIM, Local vLLM) inside #nemoclaw-architecture section
  - CSS classes: .arch-subsection, .lifecycle-pipeline, .lifecycle-stage, .lifecycle-stage-num, .lifecycle-arrow, .routing-grid, .routing-card, .routing-card-icon, .routing-badge
affects: [phase-9-i18n]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Horizontal pipeline layout with flex + relative-positioned arrow spans
    - 3-column routing card grid with inline badge styling per color theme
    - CSS color coding consistent with diagram: green=Plugin (stages 1-2), blue=Blueprint (stages 3-5)

key-files:
  created: []
  modified:
    - evidence-gate.github.io/index.html

key-decisions:
  - "Used &#8250; (single right angle quotation) character for lifecycle arrows — avoids SVG overhead for a simple separator"
  - "Stages 1-2 green, 3-5 blue matches the diagram color coding (Plugin vs Blueprint responsibility)"
  - "Routing card colors use the same palette as the ecosystem diagram (green/blue/purple per provider)"

patterns-established:
  - "arch-subsection: margin-top 3rem block pattern for adding content blocks below SVG diagrams"
  - "routing-badge: inline-block pill badge with border, consistent with .eco-badge pattern on ecosystem section"

requirements-completed: [ARCH-02, ARCH-03]

# Metrics
duration: 2min
completed: 2026-03-17
---

# Phase 5 Plan 02: Sandbox Lifecycle and Inference Routing Summary

**Five-stage sandbox lifecycle pipeline and three inference routing profile cards added to the NemoClaw Architecture section, color-coded to match the SVG diagram (green=Plugin, blue=Blueprint)**

## Performance

- **Duration:** 2 min
- **Started:** 2026-03-17T02:59:33Z
- **Completed:** 2026-03-17T03:01:12Z
- **Tasks:** 1 (+ 1 checkpoint awaiting human verify)
- **Files modified:** 1

## Accomplishments

- Sandbox Lifecycle subsection with 5 numbered stages in horizontal pipeline: Resolve, Verify (green/Plugin) then Plan, Apply, Status (blue/Blueprint)
- Inference Routing subsection with 3 provider cards: NVIDIA Cloud (Production badge, green), Local NIM (Testing/Air-gapped badge, blue), Local vLLM (Offline Dev badge, purple)
- Each routing card has feather-icon SVG, model/endpoint name in monospace, use-case description, and color-matched badge
- Runtime switching note displayed below routing grid
- CSS: arch-subsection, lifecycle-pipeline (flex horizontal scroll), routing-grid (3-col responsive grid), routing-card/routing-badge
- Mobile responsive: lifecycle scrolls horizontally, routing cards stack to 1-column

## Task Commits

Each task was committed atomically:

1. **Task 1: Add CSS and HTML for sandbox lifecycle and inference routing** - `7640b04` (feat)

## Files Created/Modified

- `evidence-gate.github.io/index.html` - Added CSS classes (.arch-subsection, .lifecycle-pipeline, .lifecycle-stage, .lifecycle-stage-num, .lifecycle-arrow, .routing-grid, .routing-card, .routing-card-icon, .routing-badge) and HTML for both subsections inside #nemoclaw-architecture

## Decisions Made

- Used &#8250; character for pipeline arrows — avoids SVG overhead for a decorative separator
- Stages 1-2 green, 3-5 blue to explicitly map Plugin (TypeScript) vs Blueprint (Python) responsibility as shown in the SVG diagram
- Routing card colors reuse the exact same hex palette as the SVG diagram and ecosystem section badges

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- ARCH-02 (sandbox lifecycle) and ARCH-03 (inference routing) requirements satisfied
- NemoClaw Architecture section now contains: SVG diagram + legend + lifecycle pipeline + routing cards
- Japanese translation (Phase 9) will need to translate both subsections' text content
- Local server running at http://localhost:8081 for human verification (Task 2 checkpoint)

---
*Phase: 05-architecture-diagrams-and-technical-foundation*
*Completed: 2026-03-17*
