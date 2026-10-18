import os

from waitress import serve

from app import app


def main():
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    serve(app, host=host, port=port)


if __name__ == "__main__":
    main()
