# Requirements — evidence-gate.dev Full Renewal v2.0

**Defined:** 2026-03-17
**Core Value:** NemoClaw公式ドキュメントの正確なアーキテクチャ情報をevidence-gate.devに反映し、3層ガバナンスの技術的信頼性を向上させる

## v2.0 Requirements

### Architecture

- [ ] **ARCH-01**: NemoClaw Plugin+Blueprint構成を正確に表現した新アーキテクチャダイアグラム（SVG）をサイトに追加する
- [ ] **ARCH-02**: サンドボックスライフサイクル（Resolve→Verify→Plan→Apply→Status）の説明をサイトに掲載する
- [ ] **ARCH-03**: 推論ルーティング3プロファイル（NVIDIA Cloud, Local NIM, Local vLLM）の説明をサイトに掲載する

### Security

- [ ] **SEC-01**: セキュリティ4層モデル（Landlock LSM + seccomp + netns + 推論制御）の詳細セクションをサイトに追加する
- [ ] **SEC-02**: ファイルシステム制限（/sandbox, /tmpのみ書込可）とネットワークポリシー（deny-by-default）を具体的に説明する

### Ecosystem

- [ ] **ECO-01**: 3層ダイアグラムをNemoClaw公式ドキュメントの正確な情報で刷新する
- [ ] **ECO-02**: ツールカードの説明文をNemoClaw公式情報に基づいて更新する
- [ ] **ECO-03**: evidence-gate-action + agentgov + NemoClaw統合のクイックスタートガイドを専用セクションとして追加する

### Content

- [ ] **CONT-01**: Heroセクションのコピーとコード例をNemoClaw統合を反映して更新する
- [ ] **CONT-02**: Pricing表を最新の機能セットで更新する
- [ ] **CONT-03**: SEO meta description, OGPタグ, 構造化データをNemoClaw統合情報で更新する

### i18n

- [ ] **I18N-01**: EN版の全変更を/ja/index.htmlに同期する

## Future Requirements

### Extended Content

- **EXT-01**: /nemoclaw/ 専用ランディングページ（NemoClaw統合の深い技術ガイド）
- **EXT-02**: ブログ記事セクション（NemoClaw + evidence-gate統合のユースケース解説）
- **EXT-03**: インタラクティブデモ（NemoClaw blueprint検証のライブ体験）

## Out of Scope

| Feature | Reason |
|---------|--------|
| NemoClaw本体のコード変更 | 外部統合のみ、フォーク不要の設計 |
| バックエンドAPI変更 | フロントエンドのみのリニューアル |
| 新しいgate typeの追加 | v1.0で追加済み、このマイルストーンはサイトコンテンツのみ |
| モバイルアプリ/PWA対応 | 静的サイトで十分 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| ARCH-01 | Phase 5 | Pending |
| ARCH-02 | Phase 5 | Pending |
| ARCH-03 | Phase 5 | Pending |
| SEC-01 | Phase 6 | Pending |
| SEC-02 | Phase 6 | Pending |
| ECO-01 | Phase 7 | Pending |
| ECO-02 | Phase 7 | Pending |
| ECO-03 | Phase 7 | Pending |
| CONT-01 | Phase 8 | Pending |
| CONT-02 | Phase 8 | Pending |
| CONT-03 | Phase 8 | Pending |
| I18N-01 | Phase 9 | Pending |

**Coverage:**
- v2.0 requirements: 12 total
- Mapped to phases: 12
- Unmapped: 0

---
*Requirements defined: 2026-03-17*
*Last updated: 2026-03-17 — traceability mapped to Phases 5-9*
