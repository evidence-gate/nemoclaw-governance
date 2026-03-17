# Roadmap: NemoClaw Governance Integration

## Milestones

- [x] **v1.0 NemoClaw Integration** - Phases 1-4 (shipped 2026-03-17)
- [ ] **v2.0 evidence-gate.dev Full Renewal** - Phases 5-9 (in progress)

## Phases

<details>
<summary>v1.0 NemoClaw Integration (Phases 1-4) - SHIPPED 2026-03-17</summary>

### Phase 1: evidence-gate-action NemoClaw Gates
**Goal**: evidence-gate-actionに3つのNemoClaw専用ゲートタイプを追加し、CI品質ゲートを実現する
**Plans**: 2 plans

Plans:
- [x] 01-01: blueprint+policy gates
- [x] 01-02: preset+recommendations+schema

### Phase 2: agentgov NemoClaw Policy & Provider
**Goal**: NemoClawサンドボックスからagentgov経由で推論ルーティングするためのポリシープリセットを提供する
**Plans**: 1 plan

Plans:
- [x] 02-01: policy preset + provider registration + onboard docs

### Phase 3: Integration Examples & Testing
**Goal**: 3層ガバナンスアーキテクチャの動作するリファレンス実装を提供する
**Plans**: 2 plans

Plans:
- [x] 03-01: examples + tests
- [x] 03-02: documentation + README

### Phase 4: HITL Bridge
**Goal**: agentgov webhook/Slack HITLとNemoClawのTUI HITLを統合する
**Plans**: 1 plan

Plans:
- [x] 04-01: HITL bridge prototype

</details>

---

### v2.0 evidence-gate.dev Full Renewal (In Progress)

**Milestone Goal:** NemoClaw公式ドキュメントの正確なアーキテクチャ情報をevidence-gate.devに反映し、3層ガバナンスの技術的信頼性を向上させる。EN+JA両対応。

## Phase Details

### Phase 5: Architecture Diagrams and Technical Foundation
**Goal**: NemoClaw公式ドキュメントに基づく正確なアーキテクチャ情報（Plugin+Blueprint構成、サンドボックスライフサイクル、推論ルーティング3プロファイル）をEN版サイトに反映し、技術的信頼性の基盤を確立する
**Depends on**: Phase 4 (v1.0 complete)
**Requirements**: ARCH-01, ARCH-02, ARCH-03
**Success Criteria** (what must be TRUE):
  1. Visitor can see a new architecture diagram accurately depicting Plugin+Blueprint composition and their relationship
  2. Visitor can read a step-by-step explanation of the sandbox lifecycle (Resolve → Verify → Plan → Apply → Status) on the site
  3. Visitor can identify all three inference routing profiles (NVIDIA Cloud, Local NIM, Local vLLM) and understand when each applies
**Plans**: 2 plans

Plans:
- [x] 05-01-PLAN.md — SVG architecture diagram + section structure + nav link (ARCH-01)
- [x] 05-02-PLAN.md — Sandbox lifecycle + inference routing content (ARCH-02, ARCH-03)

### Phase 6: Security Model Section
**Goal**: セキュリティ4層モデル（Landlock + seccomp + netns + 推論制御）とファイルシステム制限の具体的な技術詳細をEN版サイトに追加し、エンタープライズ採用者が信頼できるセキュリティ保証を確認できるようにする
**Depends on**: Phase 5
**Requirements**: SEC-01, SEC-02
**Success Criteria** (what must be TRUE):
  1. Visitor can read a dedicated security section that names and explains all four isolation layers (Landlock LSM, seccomp, netns, inference control)
  2. Visitor can see the specific filesystem constraint (writes limited to /sandbox and /tmp only) stated explicitly
  3. Visitor can read that network policy is deny-by-default and understand what egress is permitted
**Plans**: TBD

Plans:
- [ ] 06-01: TBD

### Phase 7: Ecosystem Section and Quick Start
**Goal**: Ecosystemセクションをリニューアルし、正確なPlugin+Blueprint構成図と更新されたツールカード説明、および3ツール統合のコピー&ペーストで導入できるクイックスタートガイドを提供する
**Depends on**: Phase 5
**Requirements**: ECO-01, ECO-02, ECO-03
**Success Criteria** (what must be TRUE):
  1. Visitor can view a refreshed 3-layer ecosystem diagram that reflects current NemoClaw official documentation accurately
  2. Visitor can read tool card descriptions for NemoClaw, agentgov, and evidence-gate-action that match official positioning
  3. Visitor can follow a dedicated Quick Start section and set up the evidence-gate-action + agentgov + NemoClaw integration using only the instructions on the page
  4. The Quick Start section exists as its own named section, not buried in another section
**Plans**: TBD

Plans:
- [ ] 07-01: TBD

### Phase 8: Content, Pricing, and SEO
**Goal**: Heroセクション、Pricingテーブル、SEO/OGPメタデータをNemoClaw統合情報で更新し、新規訪問者がサイトから正確な製品概要を受け取れるようにする
**Depends on**: Phase 5
**Requirements**: CONT-01, CONT-02, CONT-03
**Success Criteria** (what must be TRUE):
  1. Visitor landing on the Hero section sees copy and a code example that explicitly reflects NemoClaw integration (not generic governance messaging)
  2. Visitor viewing the Pricing table sees feature entries that reflect the current v2.0 feature set
  3. Sharing the site URL on social platforms renders an OGP card with NemoClaw integration messaging in the title and description
  4. The page meta description and structured data reference NemoClaw integration when inspected
**Plans**: TBD

Plans:
- [ ] 08-01: TBD

### Phase 9: Japanese Sync (I18N)
**Goal**: EN版（Phase 5-8）の全変更を/ja/index.htmlに忠実に同期し、JA訪問者がEN訪問者と同等の正確な技術情報を得られるようにする
**Depends on**: Phase 8 (all EN changes complete)
**Requirements**: I18N-01
**Success Criteria** (what must be TRUE):
  1. JA visitor can read all architecture, security, ecosystem, and hero content that was added or changed in Phases 5-8 in Japanese
  2. JA page contains the new architecture diagram, security section, quick start section, and updated pricing with Japanese copy
  3. No section visible in the EN page is missing from the JA page
**Plans**: TBD

Plans:
- [ ] 09-01: TBD

## Progress

**Execution Order:** 5 → 6 → 7 → 8 → 9 (Phase 6/7/8 can proceed in parallel after Phase 5)

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. evidence-gate-action Gates | v1.0 | 2/2 | Complete | 2026-03-17 |
| 2. agentgov Policy & Provider | v1.0 | 1/1 | Complete | 2026-03-17 |
| 3. Integration Examples | v1.0 | 2/2 | Complete | 2026-03-17 |
| 4. HITL Bridge | v1.0 | 1/1 | Complete | 2026-03-17 |
| 5. Architecture Foundation | v2.0 | 2/2 | Complete | 2026-03-17 |
| 6. Security Model Section | v2.0 | 0/TBD | Not started | - |
| 7. Ecosystem + Quick Start | v2.0 | 0/TBD | Not started | - |
| 8. Content, Pricing, SEO | v2.0 | 0/TBD | Not started | - |
| 9. Japanese Sync | v2.0 | 0/TBD | Not started | - |
