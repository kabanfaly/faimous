import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from backend directory
_env = Path(__file__).resolve().parent / ".env"
load_dotenv(_env)

from app import create_app

app = create_app()

if __name__ == "__main__":
    env = os.environ.get("FLASK_ENV", "development")
    debug = env == "development"
    port = int(os.environ.get("FLASK_PORT", "5001"))
    app.logger.info("Starting server on 0.0.0.0:%s (debug=%s)", port, debug)
    app.run(host="0.0.0.0", port=port, debug=debug)
