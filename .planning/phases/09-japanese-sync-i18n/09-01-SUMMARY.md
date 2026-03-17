---
phase: 09-japanese-sync-i18n
plan: 01
subsystem: i18n
tags: [html, css, seo, ogp, i18n, japanese, nemoclaw, architecture, security]

# Dependency graph
requires:
  - phase: 08-content-pricing-and-seo
    provides: "Final EN content (hero, pricing, SEO) that JA must mirror"
  - phase: 05-architecture-diagrams-and-technical-foundation
    provides: "Architecture SVG diagram, lifecycle pipeline, inference routing HTML/CSS"
  - phase: 06-security-model-section
    provides: "Security Guarantees subsection HTML/CSS"
provides:
  - "JA page CSS synchronized with EN (architecture, lifecycle, routing, security components)"
  - "JA head/meta/OGP updated with NemoClaw governance messaging in Japanese"
  - "JA nav with Architecture and NemoClaw Quick Start links"
  - "JA hero with full-stack governance copy and nemoclaw_blueprint code example"
  - "JA NemoClaw Architecture section with SVG diagram, lifecycle, routing, and security subsections"
affects: [09-02-PLAN]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "JA translations keep technical terms (NemoClaw, Plugin, Blueprint, Landlock, seccomp, etc.) in English"
    - "CSS copied verbatim from EN — language-neutral, must stay identical"
    - "SVG diagrams language-neutral — copied as-is from EN source"

key-files:
  created: []
  modified:
    - "evidence-gate.github.io/ja/index.html"

key-decisions:
  - "All CSS blocks copied exactly from EN — no JA-specific CSS overrides needed"
  - "Technical terms kept in English per established pattern from EN phases"
  - "Architecture section inserted between AI Governance and Ecosystem sections matching EN structure"

patterns-established:
  - "JA sync pattern: copy CSS verbatim, copy SVG verbatim, translate only text content"
  - "JA meta/OGP pattern: Japanese description with English product names and technical terms"

requirements-completed: []

# Metrics
duration: 15min
completed: 2026-03-17
---

# Phase 9 Plan 01: Japanese Sync — Architecture Foundation Summary

**JA page synchronized with EN Phases 5-8 foundation: CSS for all new components, NemoClaw-updated meta/OGP/nav/hero in Japanese, and complete Architecture section (SVG diagram, sandbox lifecycle, inference routing, security guarantees) with Japanese translations**

## Performance

- **Duration:** 15 min
- **Started:** 2026-03-17T07:45:00Z
- **Completed:** 2026-03-17T08:01:00Z
- **Tasks:** 3 (2 auto + 1 human-verify checkpoint)
- **Files modified:** 1

## Accomplishments
- JA page CSS now includes all architecture, lifecycle, routing, and security component styles matching EN
- Head/meta/OGP tags updated with NemoClaw governance messaging in Japanese
- Nav updated with Architecture and NemoClaw Quick Start anchor links
- Hero section rewritten with full-stack AI governance copy and nemoclaw_blueprint code example
- Complete NemoClaw Architecture section added with SVG diagram, 5-stage sandbox lifecycle pipeline, 3 inference routing profile cards, and Security Guarantees subsection (4 isolation layers + filesystem/network constraint boxes) — all in Japanese
- Human visual verification passed — page renders correctly with all new sections

## Task Commits

Each task was committed atomically:

1. **Task 1: Update CSS, Head/Meta, Nav, and Hero for NemoClaw Governance** - `58a0e3e` (feat)
2. **Task 2: Add NemoClaw Architecture Section with Security Subsection** - `5856aba` (feat)
3. **Task 3: Visual Verification** - checkpoint approved by user (no commit)

## Files Created/Modified
- `evidence-gate.github.io/ja/index.html` - Updated CSS, head/meta/OGP, nav, hero, and added complete NemoClaw Architecture section with all subsections in Japanese

## Decisions Made
- All CSS blocks copied exactly from EN — CSS is language-neutral and must remain identical
- Technical terms (NemoClaw, Plugin, Blueprint, Landlock LSM, seccomp, OpenShell, etc.) kept in English per established project convention
- Architecture section placed between AI Governance and Ecosystem sections, matching EN page structure

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- CSS foundation for all new component types is now in place in JA
- Architecture section complete — 09-02 can proceed with Ecosystem refresh, Pricing table update, and NemoClaw Quick Start section
- 09-02 depends on this plan's CSS additions (routing-grid, security-grid, lifecycle-pipeline styles already present)

## Self-Check: PASSED

- FOUND: evidence-gate.github.io/ja/index.html
- FOUND: 58a0e3e (Task 1 commit)
- FOUND: 5856aba (Task 2 commit)
- FOUND: 09-01-SUMMARY.md

---
*Phase: 09-japanese-sync-i18n*
*Completed: 2026-03-17*
