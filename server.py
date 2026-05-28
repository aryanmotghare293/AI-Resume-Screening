"""Compatibility entrypoint for the FastAPI backend.

The backend now lives in app.py so the React frontend connects to
`uvicorn app:app`. This module keeps older `uvicorn server:app` commands
working during transition.
"""

from app import app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
