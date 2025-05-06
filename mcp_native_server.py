from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("FastMCP-Server-Quickstart")

# Add an addition tool
@mcp.tool()
def add(a: float, b: float) -> float:
    """2つの数値を足し算する"""
    return a + b

# Add a multiplication tool
@mcp.tool()
def multiply(a: float, b: float) -> float:
    """2つの数値を掛け算する"""
    return a * b

# Add an echo tool
@mcp.tool()
def echo(message: str) -> dict:
    """メッセージをそのまま返す"""
    return {"message": message}

# Add a static resource
@mcp.resource("info://server")
def server_info() -> dict:
    """サーバー情報を返す"""
    return {
        "name": "FastMCP-Server-Quickstart",
        "version": "0.1.0",
        "description": "A simple MCP server implementation"
    }

# Add a dynamic resource
@mcp.resource("user://{user_id}/info")
def user_info(user_id: str) -> dict:
    """ユーザー情報を返す"""
    # サンプルデータ
    users = {
        "1": {"name": "Alice", "email": "alice@example.com"},
        "2": {"name": "Bob", "email": "bob@example.com"},
    }
    return users.get(user_id, {"error": "User not found"})

# Add a prompt
@mcp.prompt()
def greeting() -> str:
    """挨拶用のプロンプト"""
    import datetime
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""
    こんにちは、私はFastMCPを使ったサーバーです。
    現在の時刻は{current_time}です。
    
    何かお手伝いできることはありますか？
    """

# FastMCP v2では、MCPサーバーを直接実行するか、FastAPIアプリケーションからMCPサーバーを生成することができる

# If running this file directly
if __name__ == "__main__":
    import sys
    
    # コマンドライン引数でトランスポートモードを指定できるようにする
    transport_mode = 'sse'  # デフォルトはSSE
    
    # コマンドライン引数をチェック
    if len(sys.argv) > 1 and sys.argv[1] == '--stdio':
        transport_mode = 'stdio'
    
    if transport_mode == 'stdio':
        # stdioトランスポートモード
        # Claude Desktopから直接実行される場合に使用
        # 標準入出力を使用してJSON-RPCメッセージを送受信
        sys.stderr.write("Starting FastMCP server with stdio transport...\n")
        sys.stderr.flush()
        mcp.run(transport='stdio')
    else:
        # SSEトランスポートモード
        # Server-Sent Eventsを使用してブラウザやClaude Desktopと通信
        print("Starting FastMCP server with SSE transport...")
        print("Server will be available at http://localhost:8000")
        mcp.run(transport='sse')
