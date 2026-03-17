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
  - "Renamed section heading to 'What Evidence Gate Protects' — frames NemoClaw architecture from visitor perspective rather than as a standalone NemoClaw tutorial"
  - "Added .arch-narrative-bridge paragraph connecting Evidence Gate CI gate to NemoClaw sandbox runtime before the diagram"

patterns-established:
  - "arch-subsection: margin-top 3rem block pattern for adding content blocks below SVG diagrams"
  - "routing-badge: inline-block pill badge with border, consistent with .eco-badge pattern on ecosystem section"
  - "arch-narrative-bridge: centered body-copy paragraph establishing visitor context before technical diagrams"
  - "Section headings and intros written from Evidence Gate visitor perspective, not from subsystem (NemoClaw) perspective"

requirements-completed: [ARCH-02, ARCH-03]

# Metrics
duration: 15min
completed: 2026-03-17
---

# Phase 5 Plan 02: Sandbox Lifecycle and Inference Routing Summary

**Five-stage sandbox lifecycle pipeline and three inference routing profile cards added, with narrative bridge reframing the section as "What Evidence Gate Protects" to fix broken narrative flow**

## Performance

- **Duration:** ~15 min (including feedback loop)
- **Started:** 2026-03-17T02:59:33Z
- **Completed:** 2026-03-17T03:30:00Z
- **Tasks:** 2 (Task 1 auto, Task 2 checkpoint with feedback addressed)
- **Files modified:** 1

## Accomplishments

- Sandbox Lifecycle subsection with 5 numbered stages in horizontal pipeline: Resolve, Verify (green/Plugin) then Plan, Apply, Status (blue/Blueprint)
- Inference Routing subsection with 3 provider cards: NVIDIA Cloud (Production badge, green), Local NIM (Testing/Air-gapped badge, blue), Local vLLM (Offline Dev badge, purple)
- Each routing card has feather-icon SVG, model/endpoint name in monospace, use-case description, and color-matched badge
- Runtime switching note displayed below routing grid
- CSS: arch-subsection, lifecycle-pipeline (flex horizontal scroll), routing-grid (3-col responsive grid), routing-card/routing-badge, arch-narrative-bridge
- Mobile responsive: lifecycle scrolls horizontally, routing cards stack to 1-column
- Addressed user feedback: renamed section to "What Evidence Gate Protects", added narrative bridge paragraph connecting CI gates to NemoClaw runtime

## Task Commits

Each task was committed atomically:

1. **Task 1: Add CSS and HTML for sandbox lifecycle and inference routing** - `7640b04` (feat)
2. **Task 2: Reframe section heading and add narrative bridge (user feedback)** - `d6d2934` (fix)

## Files Created/Modified

- `evidence-gate.github.io/index.html` - Added CSS classes (.arch-subsection, .lifecycle-pipeline, .lifecycle-stage, .lifecycle-stage-num, .lifecycle-arrow, .routing-grid, .routing-card, .routing-card-icon, .routing-badge, .arch-narrative-bridge) and HTML for both subsections and narrative bridge inside #nemoclaw-architecture; renamed section heading to "What Evidence Gate Protects"

## Decisions Made

- Used &#8250; character for pipeline arrows — avoids SVG overhead for a decorative separator
- Stages 1-2 green, 3-5 blue to explicitly map Plugin (TypeScript) vs Blueprint (Python) responsibility as shown in the SVG diagram
- Routing card colors reuse the exact same hex palette as the SVG diagram and ecosystem section badges
- Renamed section heading to "What Evidence Gate Protects" and rewrote subtitle to bridge CI gates to runtime governance — visitors arrive for Evidence Gate, not NemoClaw

## Deviations from Plan

### Feedback-driven changes

**1. [User Feedback] Narrative bridge and section heading reframe**
- **Found during:** Task 2 (human-verify checkpoint — user provided feedback instead of approval)
- **Issue:** Narrative flow broken — Evidence Gate context dropped when "NemoClaw Architecture" section appeared without explaining its relevance to Evidence Gate visitors
- **Fix:** Changed h2 to "What Evidence Gate Protects", updated subtitle, added .arch-narrative-bridge paragraph connecting Evidence Gate CI gates to NemoClaw sandbox deployments
- **Files modified:** evidence-gate.github.io/index.html
- **Committed in:** d6d2934

---

**Total deviations:** 1 (user feedback addressed — narrative flow improvement)
**Impact on plan:** No scope change. ARCH-02 and ARCH-03 content unchanged. Only heading and introductory framing modified.

## Issues Encountered

- User checkpoint feedback: narrative flow broken — "NemoClaw Architecture" appeared without context connecting it to Evidence Gate. Addressed by reframing the section.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- ARCH-02 (sandbox lifecycle) and ARCH-03 (inference routing) requirements satisfied
- NemoClaw Architecture section now contains: SVG diagram + legend + lifecycle pipeline + routing cards + narrative bridge
- Japanese translation (Phase 9) will need to translate the narrative bridge paragraph and updated heading/subtitle
- Pattern established: Evidence Gate sections should frame technical content from visitor perspective — section headings should say what it means to the user, not just what the subsystem is

---
*Phase: 05-architecture-diagrams-and-technical-foundation*
*Completed: 2026-03-17*
