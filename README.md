# fastmcp-server-quickstart
お試しMCPサーバ入門

## 概要

このプロジェクトは、FastMCPライブラリを使用したModel Context Protocol (MCP)サーバーの実装です。MCPは、LLM（大規模言語モデル）アプリケーションにデータと機能を公開するための標準化されたプロトコルです。

FastMCPは、MCPサーバーを簡単に構築するためのPythonライブラリで、デコレータベースのAPIを提供しています。これにより、ツール、リソース、プロンプトなどのMCPコンポーネントを簡単に定義できます。

## 環境セットアップ

### 前提条件

- Python 3.12以上
- pyenv（Pythonバージョン管理用）
- uv（パッケージ管理用）

### セットアップ手順

1. リポジトリをクローン
```bash
git clone https://github.com/gon9/fastmcp-server-quickstart.git
cd fastmcp-server-quickstart
```

2. Pythonバージョンを設定
```bash
pyenv local 3.12.4  # または他の3.12系バージョン
```

3. 仮想環境を作成
```bash
uv venv
source .venv/bin/activate
```

4. 依存パッケージをインストール
```bash
uv pip install -r requirements.txt
```

## サーバーの実装方法と関係性

このプロジェクトでは、同じ機能（ツール、リソース、プロンプト）を提供する3つの異なるアプローチを用意しています。それぞれの特徴と関係性を以下に示します。

### 1. mcp_native_server.py

**概要**: FastMCPライブラリを使用したネイティブMCPサーバー

**特徴**:
- `fastmcp`ライブラリを直接使用
- SSEトランスポートモードでMCPプロトコルを実装
- Claude Desktopなどの専用MCPクライアント向け

**コアコンポーネント**:
```python
mcp = FastMCP("FastMCP-Server-Quickstart")

@mcp.tool()
def add(a: float, b: float) -> float:
    """2つの数値を足し算する"""
    return a + b

# 実行方法
if __name__ == "__main__":
    mcp.run(transport='sse')
```

**役割**: ビジネスロジック（ツール、リソース、プロンプト）の定義と、MCPプロトコルでの公開

### 2. fastapi_rest_server.py

**概要**: FastAPIを使用したRESTful APIサーバー

**特徴**:
- 標準的なRESTful APIエンドポイントを提供
- 通常のHTTPクライアント（curl、ブラウザなど）向け
- Swagger UIによるAPI仕様の自動生成

**コアコンポーネント**:
```python
# mcp_native_server.pyからロジックをインポート
from mcp_native_server import add, multiply, echo, server_info, user_info, greeting

# RESTful APIエンドポイントを定義
@tools_router.post("/add")
def add_endpoint(request: AddRequest):
    return add(request.a, request.b)
```

**役割**: mcp_native_server.pyで定義されたビジネスロジックをRESTful APIとして再公開

### 3. fastapi_mcp_integrated_server.py

**概要**: fastapi_mcpライブラリを使用したハイブリッドサーバー

**特徴**:
- わずか数行のコードでMCPサーバー機能を追加
- fastapi_rest_server.pyのRESTful APIとMCPプロトコルの両方をサポート
- 最小限の変更で既存のFastAPIアプリをMCP対応に

**コアコンポーネント**:
```python
# 既存のFastAPIアプリケーションをインポート
from fastapi_rest_server import app

# たったこれだけでMCPサーバー化完了
mcp = FastApiMCP(app)
mcp.mount()
```

**役割**: fastapi_rest_server.pyで定義されたRESTful APIをMCPプロトコルでも利用可能にする

### 3つのファイルの依存関係

```
mcp_native_server.py  ←  fastapi_rest_server.py  ←  fastapi_mcp_integrated_server.py
   (ビジネスロジック)      (RESTful APIレイヤー)       (MCPプロトコル統合レイヤー)
```

1. mcp_native_server.py: 基本となるビジネスロジック（ツール、リソース、プロンプト）を定義
2. fastapi_rest_server.py: mcp_native_server.pyのロジックをインポートしてRESTful APIとして公開
3. fastapi_mcp_integrated_server.py: fastapi_rest_server.pyのFastAPIアプリをインポートし、MCPプロトコルでも公開

### 実装方法の比較

| 特徴 | mcp_native_server.py | fastapi_rest_server.py | fastapi_mcp_integrated_server.py |
|------|---------------------|------------------------|----------------------|
| 使用ライブラリ | fastmcp | fastapi | fastapi_mcp |
| プロトコル | MCP (SSE) | HTTP (REST) | HTTP (REST) + MCP |
| クライアント | Claude Desktop, MCP CLI | curl, ブラウザ | 両方対応 |
| 依存関係 | なし | mcp_native_server.py | fastapi_rest_server.py |
| コード量 | 中程度 | 中程度 | 最小 |

### 使い分け

- **MCPクライアントのみ対応**: mcp_native_server.pyを使用
- **RESTful APIのみ対応**: fastapi_rest_server.pyを使用
- **両方対応**: fastapi_mcp_integrated_server.pyを使用（推奨）

fastapi_mcp_integrated_server.pyは、最小限のコードで両方のプロトコルをサポートする最も効率的な方法です。既存のFastAPIアプリケーションをMCPサーバーとしても公開したい場合に最適です。

## サーバーの起動

各実装方法に対応するサーバーの起動方法は以下の通りです：

### 1. ネイティブMCPサーバー（mcp_native_server.py）

```bash
# 仮想環境の有効化
source .venv/bin/activate

# SSEトランスポートモードでサーバーを起動
python mcp_native_server.py
```

### 2. RESTful APIサーバー（fastapi_rest_server.py）

```bash
# 仮想環境の有効化
source .venv/bin/activate

# FastAPIサーバーを起動
python fastapi_rest_server.py
```

### 3. ハイブリッドサーバー（fastapi_mcp_integrated_server.py）

```bash
# 仮想環境の有効化
source .venv/bin/activate

# ハイブリッドサーバー（RESTful API + MCP）を起動
python fastapi_mcp_integrated_server.py
```

いずれのサーバーも `http://localhost:8000` で起動します。

## FastMCPのコンポーネント

FastMCPでは、以下の主要なコンポーネントをデコレータを使用して定義できます：

### ツール（Tools）

ツールは、LLMがアクションを実行するための機能です。計算や外部API呼び出しなどのタスクに適しています。

```python
@mcp.tool()
def add(a: float, b: float) -> float:
    """2つの数値を足し算する"""
    return a + b
```

### リソース（Resources）

リソースは、LLMにデータを提供するための機能です。主に情報の取得に使用されます。

```python
@mcp.resource("info://server")
def server_info() -> dict:
    """\u30b5\u30fc\u30d0\u30fc\u60c5\u5831\u3092\u8fd4\u3059"""
    return {
        "name": "FastMCP-Server-Quickstart",
        "version": "0.1.0"
    }
```

### プロンプト（Prompts）

プロンプトは、LLMの動作をガイドするためのテンプレートやパターンを定義します。

```python
@mcp.prompt()
def greeting() -> str:
    """\u6328\u62f6\u7528\u306e\u30d7\u30ed\u30f3\u30d7\u30c8"""
    return "\u3053\u3093\u306b\u3061\u306f\u3001\u79c1\u306fFastMCP\u3092\u4f7f\u3063\u305f\u30b5\u30fc\u30d0\u30fc\u3067\u3059\u3002"
```

## FastMCP v2の実行モード

FastMCP v2では、以下の2つの実行モードがあります：

1. **ネイティブMCPモード** - MCPプロトコルを直接サポートするモード（SSEまたはStdioトランスポートを使用）
   - 起動方法: `python server.py`
   - 特徴: Claude Desktopや他のMCP互換クライアントと直接連携できる
   - アクセス方法: MCPクライアントからのみアクセス可能（curlなどの通常のHTTPリクエストでは使用不可）

2. **FastAPI統合モード** - FastAPIアプリケーションと統合して、RESTful APIとして公開するモード
   - 起動方法: `python run.py`
   - 特徴: 通常のRESTful APIとして公開されるため、curlやブラウザから直接アクセス可能
   - アクセス方法: HTTPリクエスト（GET/POSTなど）でアクセス可能

このプロジェクトでは、両方のモードをサポートしています。用途に応じて適切なモードを選択してください。

## MCPクライアントとの接続

このサーバーは、Claude Desktopや他のMCP互換クライアントと直接接続することができます。

### Claude Desktopでの使用方法

1. Claude Desktopを起動します
2. 設定画面で、「MCPサーバー」セクションに移動します
3. 「新しいMCPサーバーを追加」をクリックします
4. URLに `http://localhost:8000` を入力します
5. 「追加」をクリックします

### MCP CLIでの使用方法

MCP CLIを使用して、コマンドラインからサーバーと対話することもできます：

```bash
# MCP CLIのインストール
pip install mcp-cli

# MCPサーバーとの対話
mcp chat http://localhost:8000
```

## FastMCPクライアントでのテスト

PythonスクリプトからFastMCPクライアントを使用してサーバーと通信することもできます：

```python
from fastmcp import Client
from fastmcp.client.transports import SseTransport

# SSEトランスポートを使用してクライアントを作成
client = Client(
    transport=SseTransport("http://localhost:8000")
)

# ツールの一覧を取得
async def list_tools():
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
