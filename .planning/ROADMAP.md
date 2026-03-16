# Roadmap — NemoClaw Governance Integration v1.0

## Phase 1: evidence-gate-action NemoClaw Gates

**Goal:** evidence-gate-actionに3つのNemoClaw専用ゲートタイプ（blueprint検証、ポリシー監査、baselineプリセット）を追加し、NemoClawブループリント/ポリシーのCI品質ゲートを実現する。

**Requirements:** EGA-01, EGA-02, EGA-03, EGA-04, EGA-05

**Approach:**
- evidence-gate-actionリポジトリをクローン
- `local_evaluator.py`に`nemoclaw_blueprint`と`nemoclaw_policy`ゲートタイプを追加
- `presets.py`に`nemoclaw-baseline`プリセットを追加
- `entrypoint.py`にrecommendation tableエントリ追加
- NemoClaw evidence用JSONスキーマ定義
- pytest テストスイート

**Plans:** 2 (01-01: blueprint+policy gates, 01-02: preset+recommendations+schema)

**Depends on:** Nothing (independent)

---

## Phase 2: agentgov NemoClaw Policy & Provider

**Goal:** NemoClawサンドボックスからagentgovプロキシ経由で推論リクエストをルーティングするためのポリシープリセットとプロバイダー登録を提供する。

**Requirements:** AGV-01, AGV-02, AGV-03

**Approach:**
- NemoClaw互換の`agentgov-proxy.yaml`ポリシープリセット作成
- `openshell provider create`による推論プロバイダー登録手順
- NemoClaw onboard統合ドキュメント
- ポリシーYAMLのバリデーションテスト

**Plans:** 1 (02-01: policy preset + provider registration + onboard docs)

**Depends on:** Nothing (can parallel with Phase 1)

---

## Phase 3: Integration Examples & Testing

**Goal:** 3層ガバナンスアーキテクチャの動作するリファレンス実装（ブループリント、CI workflow、テストスイート）を提供し、copy-pasteで導入可能にする。

**Requirements:** INT-01, INT-02, INT-03, INT-04

**Approach:**
- agentgov統合済みのNemoClawブループリント例（blueprint.yaml + policy）
- evidence-gate-action NemoClawゲート使用のGitHub Actionsワークフロー例
- 統合テストスイート（静的解析のみ、NemoClawランタイム不要）
- READMEアーキテクチャドキュメント

**Plans:** 2 (03-01: examples + tests, 03-02: documentation + README)

**Depends on:** Phase 1, Phase 2

---

## Phase 4: HITL Bridge (Stretch)

**Goal:** agentgovのwebhook/Slack HITLとNemoClawのTUI HITLを統合し、単一の承認キューを実現する。

**Requirements:** AGV-04

**Approach:**
- OpenShellネットワークブロックイベントの検出
- agentgov HITL webhookへの変換
- 承認/拒否の伝播メカニズム

**Plans:** 1 (04-01: HITL bridge prototype)

**Depends on:** Phase 2

---

## Summary

| Phase | Name | Plans | Requirements | Priority |
|-------|------|-------|-------------|----------|
| 1 | evidence-gate-action NemoClaw Gates | 2 | EGA-01~05 | Must |
| 2 | agentgov NemoClaw Policy & Provider | 1 | AGV-01~03 | Must |
| 3 | Integration Examples & Testing | 2 | INT-01~04 | Must |
| 4 | HITL Bridge | 1 | AGV-04 | Stretch |

**Total:** 4 phases, 6 plans, 13 requirements
**Critical path:** Phase 1+2 (parallel) → Phase 3 → Phase 4 (optional)
