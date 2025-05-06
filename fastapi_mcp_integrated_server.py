import uvicorn
from fastapi_mcp import FastApiMCP

# 既存のFastAPIアプリケーションをインポート
from fastapi_rest_server import app

# たったこれだけでMCPサーバー化完了
mcp = FastApiMCP(app)
mcp.mount()

# サーバーを起動
if __name__ == "__main__":
    uvicorn.run(
        "fastapi_mcp_integrated_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
