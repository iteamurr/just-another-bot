from __future__ import annotations

import os

BACKEND_URL: str = os.getenv("APP_BACKEND_URL", "http://localhost:8000")
REQUEST_TIMEOUT: float = 120.0
