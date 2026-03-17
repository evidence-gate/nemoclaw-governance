# NemoClaw Governance Integration

## What This Is

NVIDIA NemoClaw（AIエージェントサンドボックス）と evidence-gate エコシステム（agentgov + evidence-gate-action）のネイティブ統合プロジェクト。NemoClawの4層保護（ネットワーク、ファイルシステム、プロセス、推論）に、agentgovのコスト制御・HITL承認・監査ログと、evidence-gate-actionのCI品質ゲートを組み合わせ、3層のAIエージェントガバナンスを実現する。

## Core Value

NemoClawはサンドボックス隔離に特化しているが、コスト制御が**完全に欠如**している。agentgovの予算強制（Hold/Settle）をNemoClawの推論層に統合し、evidence-gate-actionでブループリント/ポリシーのCI検証を追加することで、**インフラ隔離 + アプリケーションガバナンス + CI検証**の業界標準3層アーキテクチャを構築する。

## Current Milestone: v2.0 evidence-gate.dev Full Renewal

**Goal:** NemoClaw公式ドキュメント（docs.nvidia.com/nemoclaw）の詳細アーキテクチャ情報を反映し、evidence-gate.devサイト全体をリニューアル。Plugin+Blueprint構成、推論ルーティング3プロファイル、セキュリティ4層モデルなどの正確な技術情報を統合。EN+JA両対応。

**Target features:**
- NemoClaw公式docsベースのアーキテクチャ詳細反映
- Ecosystemセクション刷新（Plugin+Blueprint構成、推論ルーティング図）
- セキュリティモデル詳細（Landlock+seccomp+netns+推論制御）
- NemoClaw統合クイックスタートガイド
- ダイアグラム全面更新
- EN/JA同期更新

## Requirements

### Validated

- ✓ evidence-gate-action NemoClaw gates (v1.0)
- ✓ agentgov NemoClaw policy preset (v1.0)
- ✓ evidence-gate.dev 初版作成 (v1.0)
- ✓ 日本語対応（EN/JA言語切替、README.ja.md x3）(v1.0)
- ✓ AI agent threat model messaging (v1.0)

### Active

(Requirements definition follows — v2.0)

### Out of Scope

- NemoClaw本体の修正（外部からの統合のみ）
- OpenShellランタイムへの変更
- NIM/vLLMのローカルデプロイ手順
- evidence-gate-action Pro/Enterprise API側の変更
- agentgov Workers版のNemoClaw固有機能（Docker Compose版に集中）

## Current State

**v1.0 completed:** evidence-gate-action NemoClaw gates, agentgov policies, website, Japanese support
**v2.0 started:** 2026-03-17
**Related repos:**
- https://github.com/evidence-gate/agentgov (v1.2, Apache 2.0)
- https://github.com/evidence-gate/evidence-gate-action (v1.0.0, Apache 2.0)
- https://github.com/NVIDIA/NemoClaw (alpha, Apache 2.0)

**Research completed:** NemoClaw architecture, evidence-gate-action extension points, 2026 best practices

**Architecture target:**
```
CI/CD Layer (evidence-gate-action)
  │ validates: blueprint structure, policy security, budget config
  ▼
Infrastructure Layer (NemoClaw/OpenShell)
  │ enforces: filesystem, network, process isolation
  │ egress: only agentgov proxy allowed
  ▼
Application Layer (agentgov proxy)
  │ enforces: budget hold/settle, HITL approval, audit log
  ▼
LLM Provider (OpenAI / Anthropic / Nemotron)
```

## Context

### NemoClaw (NVIDIA, GTC 2026 発表)

OpenShellコンテナサンドボックス + OpenClawエージェントフレームワークのバンドル。4層保護（ネットワーク deny-by-default、Landlock FS、プロセス分離、推論ルーティング）。TypeScript CLI + Python blueprint。TUIベースのHITL（セッションスコープ、API/webhookなし）。ポリシーはYAML（9プリセット: discord, docker, huggingface, jira, npm, outlook, pypi, slack, telegram）。Alpha段階。

### 統合ポイント

**agentgov → NemoClaw:**
- カスタム推論プロバイダーとして登録（`openshell provider create --type openai-compatible`）
- ネットワークポリシーにagentgovプロキシを追加（唯一の推論エグレス先）
- onboardシステムの`custom`エンドポイントタイプで設定

**evidence-gate-action → NemoClaw:**
- `nemoclaw_blueprint`ゲートタイプ: blueprint.yaml構造検証（バージョン制約、プロファイル設定）
- `nemoclaw_policy`ゲートタイプ: OpenShellポリシーYAMLセキュリティ監査
- `nemoclaw-baseline`プリセット: 統合ゲートバンドル

### 業界動向（2026年3月）

Cisco + OpenShell統合がインフラ隔離 + アプリガバナンスの2層モデルを確立。Microsoft Agent Governance Toolkit、Gravitee MCP Proxy、NIST AI Agent Standards Initiative（2026年2月）。エンタープライズ採用: Adobe, IBM Red Hat, Box, Cadence, LangChain。

## Constraints

- **チーム**: 個人（agentgov/evidence-gate-actionの両方のメンテナー）
- **NemoClaw依存**: Alpha段階のため破壊的変更リスクあり — 外部統合のみ、フォーク不要の設計
- **互換性**: agentgov v1.2+ / evidence-gate-action v1.0.0+
- **ライセンス**: Apache 2.0（3プロジェクトすべて統一済み）
- **デプロイ**: agentgov Docker Compose版に集中（NemoClaw自体がDocker/K3s前提）
- **テスト**: NemoClaw実環境なしでもCI可能な設計（ポリシーYAML検証は静的解析）

## Key Decisions

(TBD after requirements definition)

---
*Last updated: 2026-03-17 — project initialized*
