# fastmcp-server-quickstart
お試しMCPサーバ入門

## 概要

このプロジェクトは、FastMCPライブラリを使用したModel Context Protocol (MCP)サーバーの実装例です。MCPは、LLM（大規模言語モデル）アプリケーションにデータと機能を公開するための標準化されたプロトコルです。

## 環境セットアップ

### 前提条件

- Python 3.12以上
- pyenv（Pythonバージョン管理用）
- uv（パッケージ管理用）

### セットアップ手順

1. リポジトリをクローン
2. Pythonバージョンを設定（pyenv local 3.12.x）
3. uvでプロジェクトを初期化し、依存パッケージをインストール（uv init、uv add -r requirements.txt）

## サーバーの実装方法

このプロジェクトでは、同じ機能を提供する3つの異なるアプローチを用意しています：

### 1. mcp_native_server.py

**概要**: FastMCPライブラリを使用したネイティブMCPサーバー

**特徴**:
- `fastmcp`ライブラリを直接使用
- SSEトランスポートモードでMCPプロトコルを実装
- Claude Desktopなどの専用MCPクライアント向け

**役割**: ビジネスロジック（ツール、リソース、プロンプト）の定義と、MCPプロトコルでの公開

### 2. fastapi_rest_server.py

**概要**: FastAPIを使用したRESTful APIサーバー

**特徴**:
- 標準的なRESTful APIエンドポイントを提供
- 通常のHTTPクライアント（curl、ブラウザなど）向け
- Swagger UIによるAPI仕様の自動生成

**役割**: mcp_native_server.pyで定義されたビジネスロジックをRESTful APIとして再公開

### 3. fastapi_mcp_integrated_server.py

**概要**: fastapi_mcpライブラリを使用したハイブリッドサーバー

**特徴**:
- わずか数行のコードでMCPサーバー機能を追加
- RESTful APIとMCPプロトコルの両方をサポート
- 最小限の変更で既存のFastAPIアプリをMCP対応に

**役割**: fastapi_rest_server.pyで定義されたRESTful APIをMCPプロトコルでも利用可能にする

## 実装の依存関係

```
mcp_native_server.py  ←  fastapi_rest_server.py  ←  fastapi_mcp_integrated_server.py
   (ビジネスロジック)      (RESTful APIレイヤー)       (MCPプロトコル統合レイヤー)
```

### 実装方法の比較

| 特徴 | mcp_native_server.py | fastapi_rest_server.py | fastapi_mcp_integrated_server.py |
|------|---------------------|------------------------|----------------------|
| 使用ライブラリ | fastmcp | fastapi | fastapi_mcp |
| プロトコル | MCP (SSE) | HTTP (REST) | HTTP (REST) + MCP |
| クライアント | Claude Desktop, MCP CLI | curl, ブラウザ | 両方対応 |
| 依存関係 | なし | mcp_native_server.py | fastapi_rest_server.py |

### 使い分け

- **MCPクライアントのみ対応**: mcp_native_server.pyを使用
- **RESTful APIのみ対応**: fastapi_rest_server.pyを使用
- **両方対応**: fastapi_mcp_integrated_server.pyを使用（推奨）

## サーバーの起動

### uvを使った起動方法（推奨）

```
# ネイティブMCPサーバー
uv run mcp_native_server.py

# RESTful APIサーバー
uv run fastapi_rest_server.py

# ハイブリッドサーバー
uv run fastapi_mcp_integrated_server.py
```

### エンドポイント

| サーバー実装 | MCPエンドポイント |
|---|---|
| ネイティブMCPサーバー | `http://localhost:8000` |
| RESTful APIサーバー | なし |
| ハイブリッドサーバー | `http://localhost:8000/mcp` |

**注意**: Claude Desktopの設定ファイルでは、使用するサーバーに合わせて正しいエンドポイントを指定してください。

## FastMCPのコンポーネント

FastMCPでは、以下の主要なコンポーネントをデコレータを使用して定義できます：

- **ツール（Tools）**: LLMがアクションを実行するための機能（計算や外部API呼び出しなど）
- **リソース（Resources）**: LLMが参照できるデータ（テキスト、画像、ファイルなど）
- **プロンプト（Prompts）**: LLMの動作を制御するためのテキスト

## Claude Desktopでの使用方法

1. Claude Desktopの設定ファイル（`claude_desktop_config.json`）を開く
2. `mcp_servers`セクションに新しいサーバー設定を追加
3. Claude Desktopの「MCP」タブでサーバーを追加

## MCP CLIでの使用方法

MCPサーバーをコマンドラインから操作するには、MCP CLIを使用できます：

1. インストール: `pip install mcp-cli`
2. 接続: `mcp connect http://localhost:8000`
3. ツール一覧: `mcp tools list`
4. ツール実行: `mcp tools run add --a 5 --b 3`

## ライセンス

MIT

## 貢献

バグ報告、機能リクエスト、プルリクエストなどの貢献を歓迎します。
    tools = await client.list_tools()
    print(f"Available tools: {', '.join([t for t in tools])}")
    return tools

# addツールを実行
async def run_add():
    result = await client.call_tool("add", {"a": 5, "b": 3})
    print(f"5 + 3 = {result}")
    return result

# 非同期関数を実行
async def main():
    await list_tools()
    await run_add()

# メインルーチンを実行
import asyncio
asyncio.run(main())
```

## 使用例とトラブルシューティング

### ネイティブMCPモード（SSEトランスポート）の場合

1. サーバーを起動します：

```bash
source .venv/bin/activate
python server.py
```

2. Claude Desktopで接続します：
   - Claude Desktopの設定で「MCPサーバー」を追加
   - URLに `http://localhost:8000` を入力
   - 会話内でツールを使用する（例：「5と5を足し算してください」）

3. トラブルシューティング：
   - 通常のcurlコマンドではアクセスできません。「Not Found」エラーが表示されるのは正常です。
   - サーバーのログを確認して、正常に起動しているか確認してください。
   - Claude Desktopが接続できない場合は、ファイアウォール設定やネットワーク設定を確認してください。

### FastAPI統合モードの場合

1. サーバーを起動します：

```bash
source .venv/bin/activate
python run.py
```

2. curlでツールを実行できます：

```bash
# 加算ツールの実行
curl -X POST http://localhost:8000/tools/add \
  -H "Content-Type: application/json" \
  -d '{"a": 5, "b": 3}'

# エコーツールの実行
curl -X POST http://localhost:8000/tools/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, FastMCP!"}'
```

3. トラブルシューティング：
   - エンドポイントが見つからない場合は、サーバーのログを確認してください。
   - デバッグ情報を確認するには、`/docs`エンドポイントにアクセスしてSwagger UIを確認してください。

## モードの切り替え方法

現在のプロジェクトでは、両方のモードをサポートしています。モードの切り替えは、単に起動スクリプトを変更するだけです：

- ネイティブMCPモード（Claude Desktop用）: `python server.py`
- FastAPI統合モード（curlやブラウザ用）: `python run.py`

## 注意事項

- 両方のモードを同時に実行することはできません。ポートの競合が発生します。
- SSEトランスポートモードでは、Claude DesktopやMCP CLIなどのMCP互換クライアントが必要です。
- FastAPI統合モードでは、通常のHTTPリクエスト（curlやブラウザ）でアクセスできます。
- プロジェクトの拡張やカスタマイズについては、[FastMCP公式ドキュメント](https://gofastmcp.com/)を参照してください。
