[English](README.md) | **日本語**

# NemoClaw ガバナンス統合

AIエージェントのための3層ガバナンス：インフラ分離（NemoClaw）＋コスト制御（agentgov）＋ CI品質ゲート（evidence-gate-action）。

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![CI](https://github.com/evidence-gate/nemoclaw-governance/actions/workflows/ci.yml/badge.svg)](https://github.com/evidence-gate/nemoclaw-governance/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## モチベーション

NVIDIA NemoClaw は、ネットワーク・ファイルシステム・プロセスの分離によるサンドボックス実行環境をAIエージェントに提供します。本プロジェクトが想定するデプロイ構成では、**サンドボックス分離に加えて、予算制御と設定検証を別レイヤーで補完すること**が有用です。

本プロジェクトは以下の補完レイヤーを提供します：

- **agentgov** はサンドボックスとLLMプロバイダーの間に位置し、Hold/Settleパターンによるエージェントごとの予算制御を実現します
- **evidence-gate-action** はデプロイ前にCIでNemoClaw blueprintとpolicyをバリデーションします
- **nemoclaw-governance** はプリセット、CLIツール、サンプルを通じてこれらを統合します

## クイックスタート

### インストール

```bash
pip install nemoclaw-governance[yaml]
```

`nemoclaw-gov` CLIとPythonバリデーションライブラリがインストールされます。

### NemoClaw設定ファイルをバリデーションする

```bash
# Blueprintをバリデーション
nemoclaw-gov validate blueprint.yaml

# Policyをバリデーション
nemoclaw-gov validate openclaw-sandbox.yaml

# ディレクトリ内の全設定ファイルをバリデーション
nemoclaw-gov validate --all nemoclaw/
```

### Pythonライブラリとして使用する

```python
from nemoclaw_governance import validate_blueprint, validate_policy, validate_file

# ファイルタイプを自動検出してバリデーション
result = validate_file("blueprint.yaml")
print(result.passed)    # True/False
print(result.issues)    # 問題のリスト（合格時は空）
print(result.gate_type) # "nemoclaw_blueprint" または "nemoclaw_policy"

# パース済みデータを直接バリデーション
import yaml
with open("blueprint.yaml") as f:
    data = yaml.safe_load(f)
result = validate_blueprint(data)
```

### NemoClaw に agentgov を追加する

```bash
# 1. agentgov プロキシを起動
cd /path/to/agentgov
docker compose -f docker/compose.yml up -d

# 2. agentgov を推論プロバイダーとして登録し、ネットワークポリシーを適用
./scripts/setup-agentgov-provider.sh

# または手順ごとに実行:
openshell provider create --name agentgov --type openai-compatible \
  --endpoint-url http://localhost:8787/v1 --model gpt-4o
nemoclaw policy-add nemoclaw-presets/agentgov-proxy.yaml
openshell inference set --provider agentgov --model gpt-4o
```

### CIゲートを追加する

```yaml
# .github/workflows/nemoclaw-gate.yml
- name: Validate NemoClaw Blueprint
  uses: evidence-gate/evidence-gate-action@v1
  with:
    gate_type: nemoclaw_blueprint
    phase_id: deploy
    evidence_files: /tmp/blueprint.json

- name: Validate NemoClaw Policy
  uses: evidence-gate/evidence-gate-action@v1
  with:
    gate_type: nemoclaw_policy
    phase_id: deploy
    evidence_files: /tmp/policy.json
```

## アーキテクチャ

```
┌─────────────────────────────────────────────────┐
│  CI/CD レイヤー (evidence-gate-action)            │
│  デプロイ前にバリデーション:                        │
│  - Blueprint構造 (nemoclaw_blueprint ゲート)      │
│  - Policyセキュリティ (nemoclaw_policy ゲート)     │
│  - nemoclaw-baseline プリセット（主要な静的チェック） │
└─────────┬───────────────────────────────────────┘
          │ デプロイ
          ▼
┌─────────────────────────────────────────────────┐
│  インフラレイヤー (NemoClaw / OpenShell)           │
│  ランタイムで強制:                                 │
│  - ファイルシステム分離 (Landlock LSM)             │
│  - ネットワーク: デフォルト拒否、agentgovのみ許可   │
│  - プロセスサンドボックス (権限昇格なし)            │
└─────────┬───────────────────────────────────────┘
          │ 推論リクエスト → agentgov プロキシ
          ▼
┌─────────────────────────────────────────────────┐
│  アプリケーションレイヤー (agentgov プロキシ)       │
│  リクエストごとに強制:                             │
│  - 予算ゲート (Hold/Settle パターン)               │
│  - HITL承認 (Slack/webhook)                       │
│  - 監査ログ (SHA-256 ハッシュチェーン)              │
└─────────┬───────────────────────────────────────┘
          │ ガバナンス適用済みLLM呼び出し
          ▼
┌─────────────────────────────────────────────────┐
│  LLMプロバイダー (OpenAI / Anthropic / Gemini)     │
└─────────────────────────────────────────────────┘
```

この設計は、CiscoやNVIDIA/OpenShellのアーキテクチャに見られるレイヤード構成を参考にしています：インフラ分離（レイヤー1）＋アプリケーションガバナンス（レイヤー2）＋ CIバリデーション（レイヤー3）。

## 同梱内容

### Pythonパッケージ (`pip install nemoclaw-governance[yaml]`)

| 機能 | 説明 |
|------|------|
| `validate_blueprint()` | NemoClaw blueprint.yaml の構造をバリデーション |
| `validate_policy()` | OpenShell policy YAML のセキュリティ監査 |
| `validate_file()` | ファイルタイプを自動検出してバリデーション |
| `nemoclaw-gov` CLI | コマンドラインでのバリデーションとプリセット管理 |

### evidence-gate-action 用ゲートタイプ

| ゲートタイプ | バリデーション内容 |
|------------|------------------|
| `nemoclaw_blueprint` | version（semver）、profiles（modelが必須）、sandbox（image）、バージョン制約 |
| `nemoclaw_policy` | enforcement=enforce、ポート443でのTLS、ワイルドカードメソッド禁止、危険な書き込みパス禁止 |
| `nemoclaw-baseline` プリセット | 上記すべて ＋ `security` ＋ `build`（主要な静的チェック、網羅的ではない） |

### NemoClaw 用 Policy プリセット

| ファイル | 用途 |
|---------|------|
| `agentgov-proxy.yaml` | サンドボックスからagentgovプロキシへのエグレスのみを許可するネットワークポリシー |
| `agentgov-inference-profile.json` | `openshell provider create` 用のプロバイダー設定 |

## CLIリファレンス

### `nemoclaw-gov validate`

1つ以上のNemoClaw設定ファイルをバリデーションします：

```bash
# 単一ファイル
nemoclaw-gov validate blueprint.yaml

# 複数ファイル
nemoclaw-gov validate blueprint.yaml policy.yaml

# ディレクトリスキャン
nemoclaw-gov validate --all configs/
```

出力例：

```
NemoClaw Governance Validation (2 file(s))
==================================================
  [PASS] blueprint.yaml (nemoclaw_blueprint)
  [FAIL] policy.yaml (nemoclaw_policy)
    - POLICY_WEAK_ENFORCEMENT: test.endpoints[0] has enforcement='monitor', expected 'enforce'
    - POLICY_MISSING_TLS: test.endpoints[0] on port 443 should have tls='terminate'

1/2 file(s) failed with 2 issue(s).
```

終了コード：すべて合格の場合 `0`、いずれか不合格の場合 `1`。

### `nemoclaw-gov presets`

バンドルされたpolicyプリセットを管理します：

```bash
# 利用可能なプリセットを一覧表示
nemoclaw-gov presets list

# プリセットの内容を表示
nemoclaw-gov presets show agentgov-proxy

# ファイルパスを取得（コピーや適用用）
nemoclaw-gov presets path agentgov-proxy
```

### `nemoclaw-gov version`

```bash
nemoclaw-gov version
# nemoclaw-governance 0.1.0
```

## バリデーション詳細

### nemoclaw_blueprint

NemoClaw `blueprint.yaml` の構造をバリデーションします：

| チェック項目 | 問題コード | 説明 |
|------------|-----------|------|
| バージョンの存在 | `BLUEPRINT_MISSING_VERSION` | `version` フィールドが必須 |
| バージョン形式 | `BLUEPRINT_INVALID_VERSION` | 有効なsemver形式（X.Y.Z）が必須 |
| プロファイルの存在 | `BLUEPRINT_MISSING_PROFILES` | `profiles` セクションが必須 |
| プロファイルが空でないこと | `BLUEPRINT_EMPTY_PROFILES` | 1つ以上のプロファイルが必要 |
| プロファイルのモデル | `BLUEPRINT_PROFILE_MISSING_MODEL` | 各プロファイルに `model` フィールドが必要 |
| サンドボックスの存在 | `BLUEPRINT_MISSING_SANDBOX` | `sandbox` セクションが必須 |
| サンドボックスイメージ | `BLUEPRINT_MISSING_IMAGE` | `sandbox.image` が必須 |
| バージョン制約 | `BLUEPRINT_INVALID_MIN_*` | オプションの最小バージョンはsemver形式が必須 |

### nemoclaw_policy

NemoClaw `openclaw-sandbox.yaml` のセキュリティ監査：

| チェック項目 | 問題コード | 説明 |
|------------|-----------|------|
| バージョンの存在 | `POLICY_MISSING_VERSION` | `version` フィールドが必須 |
| ネットワークポリシー | `POLICY_MISSING_NETWORK` | `network_policies` セクションが必須 |
| 実行モード | `POLICY_WEAK_ENFORCEMENT` | すべてのエンドポイントで `enforcement: enforce` が必須 |
| 443番ポートのTLS | `POLICY_MISSING_TLS` | ポート443のエンドポイントは `tls: terminate` が必須 |
| ワイルドカード禁止 | `POLICY_WILDCARD_METHOD` | `method: "*"` ルールは使用不可 |
| 安全なファイルシステム | `POLICY_DANGEROUS_WRITABLE` | `/usr`、`/etc`、`/lib` などへの書き込みアクセス禁止 |

## ワークフローレシピ

### レシピ 1：プルリクエスト時にバリデーション

```yaml
name: NemoClaw Governance Gate
on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install validator
        run: pip install nemoclaw-governance[yaml]

      - name: Validate all NemoClaw configs
        run: nemoclaw-gov validate --all nemoclaw/
```

### レシピ 2：evidence-gate-action とプリセットの利用

```yaml
name: NemoClaw Quality Gates
on: [pull_request]

jobs:
  gates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Convert YAML to JSON
        run: |
          pip install pyyaml
          python -c "
          import yaml, json
          for src, dst in [
              ('nemoclaw/blueprint.yaml', '/tmp/blueprint.json'),
              ('policies/openclaw-sandbox.yaml', '/tmp/policy.json'),
          ]:
              with open(src) as f: data = yaml.safe_load(f)
              with open(dst, 'w') as f: json.dump(data, f)
          "

      - name: NemoClaw Governance Gate
        uses: evidence-gate/evidence-gate-action@v1
        with:
          gate_preset: nemoclaw-baseline
          phase_id: deploy
          evidence_files: /tmp/blueprint.json,/tmp/policy.json
          sticky_comment: true
```

### レシピ 3：バリデーション後にagentgovとともにデプロイ

```yaml
name: Deploy with Governance
on:
  push:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install validator
        run: pip install nemoclaw-governance[yaml]

      - name: Validate configs
        run: |
          nemoclaw-gov validate nemoclaw/blueprint.yaml
          nemoclaw-gov validate policies/openclaw-sandbox.yaml

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy NemoClaw sandbox
        run: |
          nemoclaw launch --profile agentgov
```

### レシピ 4：オブザーブモード（ドライラン）

```yaml
- name: NemoClaw Gate (Observe)
  uses: evidence-gate/evidence-gate-action@v1
  with:
    gate_preset: nemoclaw-baseline
    phase_id: deploy
    evidence_files: /tmp/blueprint.json,/tmp/policy.json
    mode: observe
```

## トラブルシューティング

### "YAML files require PyYAML"

YAML対応でインストールしてください：

```bash
pip install nemoclaw-governance[yaml]
```

または PyYAML を個別にインストール：`pip install pyyaml`

### "Cannot determine file type"

バリデーターはblueprint（`profiles`/`sandbox` を含む）とpolicy（`network_policies` を含む）を自動検出します。ファイルがどちらのパターンにも一致しない場合は、チェックを手動で指定してください：

```python
from nemoclaw_governance import validate_blueprint
import yaml

with open("my-config.yaml") as f:
    data = yaml.safe_load(f)
result = validate_blueprint(data)
```

### "File not found" — evidence-gate-action 使用時

evidence-gate-action はJSONエビデンスファイルを必要とします。先にYAMLを変換してください：

```bash
python -c "import yaml, json; data=yaml.safe_load(open('blueprint.yaml')); json.dump(data, open('/tmp/blueprint.json','w'))"
```

### CLIが終了コード1で終了する

終了コード1は、少なくとも1つのファイルがバリデーションに失敗したことを意味します。出力の問題コードを確認し、記載された問題を修正してください。

## プロジェクト構成

```
nemoclaw-governance/
  src/
    nemoclaw_governance/
      __init__.py          # 公開API: validate_*, ValidationResult
      validate.py          # Blueprint + policy バリデーションロジック
      presets.py           # バンドル済みプリセット管理
      cli.py               # nemoclaw-gov CLI
  nemoclaw-presets/
    agentgov-proxy.yaml    # NemoClaw ネットワークポリシープリセット
    agentgov-inference-profile.json
  examples/
    blueprint-with-agentgov.yaml
    policy-with-agentgov.yaml
    ci-workflow.yml
  scripts/
    setup-agentgov-provider.sh
  tests/                   # 55テスト
  .github/
    workflows/ci.yml       # Lint + テスト (3.11/3.12/3.13) + CLI スモークテスト
    dependabot.yml
```

## 関連プロジェクト

| プロジェクト | 役割 | リンク |
|------------|------|--------|
| **agentgov** | ランタイム予算制御プロキシ | [evidence-gate/agentgov](https://github.com/evidence-gate/agentgov) |
| **evidence-gate-action** | CI品質ゲートの実行 | [evidence-gate/evidence-gate-action](https://github.com/evidence-gate/evidence-gate-action) |
| **NemoClaw** | エージェントサンドボックス (NVIDIA) | [NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw) |

## リンク

- [変更履歴](CHANGELOG.md)
- [NemoClaw ドキュメント](https://github.com/NVIDIA/NemoClaw)
- [agentgov クイックスタート](https://github.com/evidence-gate/agentgov#quick-start)
- [evidence-gate-action マーケットプレイス](https://github.com/marketplace/actions/evidence-gate-action)

## ライセンス

Apache License 2.0。Copyright 2026 AllNew LLC。詳細は [LICENSE](LICENSE) を参照してください。
