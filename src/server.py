import asyncio
from aiohttp import web
import jwt
import sqlite3
from src.main import main  # Assuming main() is defined in src/main.py

# JWT secret key
SECRET_KEY = "your_secret_key"


# SQLite database setup
def init_db():
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


# JWT authentication middleware
@web.middleware
async def jwt_auth_middleware(request, handler):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return web.json_response({"error": "Missing or invalid token"}, status=401)

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("user")
        password = payload.get("password")

        conn = sqlite3.connect("credentials.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        user = cursor.fetchone()
        conn.close()

        if not user:
            return web.json_response(
                {"error": "Invalid username or password"}, status=401
            )
    except jwt.ExpiredSignatureError:
        return web.json_response({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return web.json_response({"error": "Invalid token"}, status=401)

    return await handler(request)


# Handler for /generate_report
async def generate_report(request):
    try:
        # Call the main() method from src/main.py
        main()
        return web.json_response({"message": "Report generated successfully"})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


# Add a new route to retrieve the report.pdf
async def download_report(request):
    try:
        return web.FileResponse("build/report.pdf")
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


# Main application setup
async def init_app():
    init_db()
    app = web.Application(middlewares=[jwt_auth_middleware])
    app.router.add_get("/generate_report", generate_report)
    app.router.add_get("/download_report", download_report)
    return app


if __name__ == "__main__":
    web.run_app(init_app())
