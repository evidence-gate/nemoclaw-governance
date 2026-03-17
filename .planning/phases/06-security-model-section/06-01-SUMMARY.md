---
phase: 06-security-model-section
plan: 01
subsystem: ui
tags: [html, css, security, landlock, seccomp, network-namespace, inference-control]

# Dependency graph
requires:
  - phase: 05-architecture-diagrams-and-technical-foundation
    provides: arch-subsection CSS pattern, routing card icon pattern, color palette, HTML structure for nemoclaw-architecture section
provides:
  - Security Guarantees subsection inside #nemoclaw-architecture with four isolation layer cards
  - Filesystem constraint box (/sandbox, /tmp writable)
  - Network constraint box (deny-by-default policy)
  - .security-grid and .security-constraints responsive CSS classes
affects: [07-any-phase-referencing-security, future EN copy phases]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "security-card follows routing-card layout pattern: icon circle + h4 + p"
    - "security-constraint-box uses border-left accent color matching layer color"

key-files:
  created: []
  modified:
    - evidence-gate.github.io/index.html

key-decisions:
  - "Security Guarantees placed as arch-subsection inside #nemoclaw-architecture (not a standalone top-level section) — consistent with lifecycle and routing subsections"
  - "Content framed from Evidence Gate visitor perspective: 'Evidence Gate validates that all four isolation layers are correctly configured' — not a NemoClaw tutorial"
  - "Constraint boxes use border-left accent with #f8fafc background — consistent with section-alt color palette"

patterns-established:
  - "Pattern: Security subsection arch-subsection follows same CSS class hierarchy as lifecycle and routing subsections"
  - "Pattern: Constraint boxes with colored left-border used for specification tables (filesystem, network)"

requirements-completed: [SEC-01, SEC-02]

# Metrics
duration: 5min
completed: 2026-03-17
---

# Phase 06 Plan 01: Security Model Section Summary

**Security Guarantees subsection added to #nemoclaw-architecture — four isolation layer cards (Landlock LSM, seccomp, netns, inference control) plus filesystem (/sandbox, /tmp) and network (deny-by-default) constraint boxes**

## Performance

- **Duration:** ~5 min
- **Started:** 2026-03-17T05:06:06Z
- **Completed:** 2026-03-17T05:11:00Z
- **Tasks:** 2 of 2 (complete)
- **Files modified:** 1

## Accomplishments
- Added Security Guarantees arch-subsection inside the existing #nemoclaw-architecture section (after Inference Routing subsection)
- Four isolation layer cards rendered in a 2x2 grid: Landlock LSM (green), seccomp Filtering (blue), Network Namespace Isolation (purple), Inference Control (slate)
- Filesystem constraint box explicitly names /sandbox and /tmp as writable, all other paths read-only or inaccessible
- Network constraint box explicitly states deny-by-default egress policy with blueprint.yaml-approved endpoints
- Responsive CSS: .security-grid and .security-constraints collapse to single column at max-width 768px
- All copy framed from Evidence Gate visitor perspective (validates layers, gates pipeline on misconfiguration)

## Task Commits

Each task was committed atomically:

1. **Task 1: Add CSS and HTML for security guarantees subsection** - `7b92412` (feat) — committed in evidence-gate.github.io nested repo
2. **Task 2: Visual verification** — approved by human (checkpoint passed)

## Files Created/Modified
- `evidence-gate.github.io/index.html` - Added ~100 lines of CSS (security-grid, security-card, security-constraint-box classes + responsive rules) and ~110 lines of HTML (Security Guarantees arch-subsection with four cards and two constraint boxes)

## Decisions Made
- Security Guarantees placed as arch-subsection inside #nemoclaw-architecture (not a standalone top-level section) — consistent with lifecycle and routing subsections
- Content framed from Evidence Gate visitor perspective: "Evidence Gate validates that all four isolation layers are correctly configured" — not a NemoClaw tutorial
- No nav link added — security is a subsection, not its own section
- Used inline SVG icons: shield for Landlock, filter/funnel for seccomp, globe/meridian for netns, CPU chip for inference control

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Security Guarantees subsection is complete and verified — both tasks complete
- Human visual verification passed (Task 2 checkpoint approved)
- Phase 6 Plan 01 fully complete; Phase 7 or further Phase 6 plans can proceed

---
*Phase: 06-security-model-section*
*Completed: 2026-03-17*
