import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
# server.pyからツール、リソース、プロンプトの定義をインポート
from mcp_native_server import add, multiply, echo, server_info, user_info, greeting

# FastAPIアプリケーションを作成
app = FastAPI(
    title="FastMCP Server",
    description="A Model Context Protocol (MCP) server implementation using FastMCP",
    version="0.1.0"
)

# ヘルスチェックエンドポイント
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# ツールのリクエストモデル
class AddRequest(BaseModel):
    a: float
    b: float

class MultiplyRequest(BaseModel):
    a: float
    b: float

class EchoRequest(BaseModel):
    message: str

# ツールのAPIルーター
tools_router = APIRouter(prefix="/tools", tags=["tools"])

@tools_router.post("/add")
def add_endpoint(request: AddRequest):
    """2つの数値を足し算する"""
    return add(request.a, request.b)

@tools_router.post("/multiply")
def multiply_endpoint(request: MultiplyRequest):
    """2つの数値を掛け算する"""
    return multiply(request.a, request.b)

@tools_router.post("/echo")
def echo_endpoint(request: EchoRequest):
    """メッセージをそのまま返す"""
    return echo(request.message)

# リソースのAPIルーター
resources_router = APIRouter(prefix="/resources", tags=["resources"])

@resources_router.get("/info/server")
def server_info_endpoint():
    """サーバー情報を返す"""
    return server_info()

@resources_router.get("/user/{user_id}/info")
def user_info_endpoint(user_id: str):
    """ユーザー情報を返す"""
    return user_info(user_id)

# プロンプトのAPIルーター
prompts_router = APIRouter(prefix="/prompts", tags=["prompts"])

@prompts_router.get("/greeting")
def greeting_endpoint():
    """挨拶用のプロンプト"""
    return {"prompt": greeting()}

# ルーターをアプリケーションに登録
app.include_router(tools_router)
app.include_router(resources_router)
app.include_router(prompts_router)

if __name__ == "__main__":
    # Uvicornを使用してFastAPIアプリケーションを起動
    uvicorn.run(
        "run:app",     # このファイル内のappオブジェクト（FastAPIアプリケーション）を使用
        host="0.0.0.0",  # すべてのネットワークインターフェースでリッスン
        port=8000,       # ポート8000でリッスン
        reload=True      # 開発中はコード変更時に自動リロード
    )
