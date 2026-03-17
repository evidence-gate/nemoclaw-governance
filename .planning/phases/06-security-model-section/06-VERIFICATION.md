---
phase: 06-security-model-section
verified: 2026-03-17T05:30:00Z
status: human_needed
score: 4/4 must-haves verified
re_verification: false
human_verification:
  - test: "Open index.html in a browser, scroll to 'What Evidence Gate Protects' and verify the Security Guarantees subsection renders with four cards and two constraint boxes visually consistent with the lifecycle and routing subsections above it"
    expected: "Four isolation layer cards (Landlock LSM, seccomp Filtering, Network Namespace Isolation, Inference Control) displayed in a 2x2 grid, followed by Filesystem and Network constraint boxes in a 2-column layout, all styled consistently with existing arch-subsection pattern"
    why_human: "CSS layout rendering, color accuracy, icon display, and visual consistency with adjacent subsections cannot be verified by grep"
  - test: "Resize browser to mobile width (< 768px) and verify cards and constraint boxes collapse to single column"
    expected: ".security-grid and .security-constraints both switch to grid-template-columns: 1fr"
    why_human: "Responsive layout rendering requires a real browser; CSS rules exist but display behaviour must be confirmed visually"
---

# Phase 06: Security Model Section Verification Report

**Phase Goal:** セキュリティ4層モデル（Landlock + seccomp + netns + 推論制御）とファイルシステム制限の具体的な技術詳細をEN版サイトに追加し、エンタープライズ採用者が信頼できるセキュリティ保証を確認できるようにする
**Verified:** 2026-03-17T05:30:00Z
**Status:** human_needed — all automated checks pass; visual rendering requires human confirmation
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Visitor can read a dedicated security section that names and explains all four isolation layers (Landlock LSM, seccomp, netns, inference control) | VERIFIED | `index.html` lines 1489–1550: four `.security-card` elements with h4 titles "Landlock LSM", "seccomp Filtering", "Network Namespace Isolation", "Inference Control" and substantive descriptive text for each |
| 2 | Visitor can see the specific filesystem constraint (writes limited to /sandbox and /tmp only) stated explicitly | VERIFIED | Lines 1558–1561: `<code>/sandbox</code>` and `<code>/tmp</code>` listed as read+write; "All other paths — read-only or inaccessible" and "System binaries, configs, and host mounts are never writable" follow immediately |
| 3 | Visitor can read that network policy is deny-by-default and understand what egress is permitted | VERIFIED | Line 1527: "deny-by-default egress policy" in the Network Namespace card; lines 1569–1572: Network constraint box lists "Deny-by-default — no egress until explicitly allowed", "Approved endpoints listed in blueprint.yaml", unapproved requests blocked |
| 4 | Security content is framed from Evidence Gate perspective — what Evidence Gate validates, not a NemoClaw tutorial | VERIFIED | Line 1486: "Evidence Gate validates that every sandbox deploys with four mandatory isolation layers"; line 1499: "Evidence Gate validates that Landlock rules are correctly configured before deployment"; line 1578: "Evidence Gate's blueprint and policy gates validate that all four isolation layers are correctly configured before any sandbox is deployed to production" |

**Score:** 4/4 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `evidence-gate.github.io/index.html` | Security model subsection with CSS and HTML | VERIFIED | File exists (1906 lines). Contains `.security-grid`, `.security-card`, `.security-constraint-box` CSS classes (lines 705–799). HTML subsection at lines 1483–1580. Committed as `7b92412`. |

Artifact check — all three levels:

- **Level 1 (Exists):** File present at `/Users/masa/nemoclaw-workspace/evidence-gate.github.io/index.html`
- **Level 2 (Substantive):** ~100 lines of CSS (lines 703–803) and ~100 lines of HTML (lines 1483–1580) added — not a stub
- **Level 3 (Wired):** Security subsection is inside `<section id="nemoclaw-architecture">` (section opens line 1316, subsection at 1483–1580, section closes line 1582). CSS classes are used directly in the HTML. No orphaned styles.

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| nav or section scroll | `#nemoclaw-architecture` | Security Guarantees subsection is a `.arch-subsection` inside the section | WIRED | Lines 1483–1580 are between the `<section id="nemoclaw-architecture">` open tag (1316) and its `</section>` (1582); the existing nav link at line 1109 routes to `#nemoclaw-architecture` and includes the security content automatically |
| `.security-grid` CSS | HTML `.security-grid` element | Class applied to `<div class="security-grid">` at line 1488 | WIRED | CSS defined at lines 705–712; used in HTML at line 1488 |
| `.security-constraints` CSS | HTML `.security-constraints` element | Class applied at line 1553 | WIRED | CSS defined at lines 757–764; used in HTML at line 1553 |
| Responsive breakpoint | `.security-grid`, `.security-constraints` | `@media (max-width: 768px)` at line 1075 | WIRED | Both classes reset to `grid-template-columns: 1fr` inside the existing responsive block |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| SEC-01 | 06-01-PLAN.md | セキュリティ4層モデル（Landlock LSM + seccomp + netns + 推論制御）の詳細セクションをサイトに追加する | SATISFIED | All four layers named, explained, and rendered in `.security-grid` inside `#nemoclaw-architecture` |
| SEC-02 | 06-01-PLAN.md | ファイルシステム制限（/sandbox, /tmpのみ書込可）とネットワークポリシー（deny-by-default）を具体的に説明する | SATISFIED | Filesystem constraint box explicitly lists `/sandbox` and `/tmp` as writable; network constraint box explicitly states "Deny-by-default"; REQUIREMENTS.md traceability table marks both as Complete for Phase 6 |

No orphaned requirements: REQUIREMENTS.md maps only SEC-01 and SEC-02 to Phase 6, both claimed and satisfied by 06-01-PLAN.md.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| — | — | No TODO/FIXME/placeholder comments | — | None |
| — | — | No empty implementations or stub returns | — | None |
| — | — | No console.log-only handlers | — | None |

No anti-patterns detected in the modified content.

### Human Verification Required

#### 1. Visual layout and styling of security subsection

**Test:** Open `/Users/masa/nemoclaw-workspace/evidence-gate.github.io/index.html` in a browser. Scroll to "What Evidence Gate Protects". Below the Inference Routing cards, verify the "Security Guarantees" subsection renders with four cards in a 2x2 grid and two constraint boxes in a 2-column layout.
**Expected:** Cards show colored icon circles (green for Landlock, blue for seccomp, purple for netns, slate for inference control), h4 titles, and descriptive paragraphs. Constraint boxes show green left-border (Filesystem) and purple left-border (Network). Visual consistency with the lifecycle and routing subsections above.
**Why human:** CSS grid rendering, SVG icon display, and color accuracy cannot be verified by static analysis.

#### 2. Mobile responsive layout

**Test:** Resize browser to under 768px width. Verify the four security cards collapse to a single-column stack, and the two constraint boxes also collapse to single column.
**Expected:** `.security-grid` and `.security-constraints` both display as one-column layout at mobile width.
**Why human:** CSS media query behavior requires real browser rendering to confirm.

#### 3. Evidence Gate framing tone check

**Test:** Read the security subsection copy. Confirm the framing is "Evidence Gate validates X" throughout, not "NemoClaw does X" or a general security tutorial.
**Expected:** Section is clearly positioned as a verification contract (what Evidence Gate certifies), not product documentation for NemoClaw.
**Why human:** Tone and framing quality is a human judgement call; grep confirms the presence of "Evidence Gate validates" phrases but not whether the overall reading experience achieves the intended perspective.

### Gaps Summary

No gaps found. All four success criteria from ROADMAP.md are satisfied by the actual HTML content in `index.html`:

1. All four isolation layers are named and explained — Landlock LSM (line 1497), seccomp Filtering (line 1510), Network Namespace Isolation (line 1525), Inference Control (line 1547)
2. Filesystem constraint explicitly states `/sandbox` and `/tmp` as writable, all other paths read-only (lines 1558–1561)
3. Network policy states deny-by-default (line 1527 and 1569), identifies approved endpoints via `blueprint.yaml` (line 1570)

The only open items are visual verification tasks that require human review of browser rendering and responsive behavior.

---

_Verified: 2026-03-17T05:30:00Z_
_Verifier: Claude (gsd-verifier)_
