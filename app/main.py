from fastapi import FastAPI, Request
import logging
import uuid
from contextvars import ContextVar

from app.api.routes import router

app = FastAPI(title="AI PDF Agent")

# -----------------------------
# 1. Request ID context
# -----------------------------
request_id_var: ContextVar[str] = ContextVar("request_id", default="startup")


def get_request_id():
    return request_id_var.get()


# -----------------------------
# 2. Middleware to inject request_id
# -----------------------------
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    request_id_var.set(request_id)

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# -----------------------------
# 3. Logging setup (centralized)
# -----------------------------
class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = get_request_id()
        return True


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | req=%(request_id)s | %(name)s | %(message)s",
)

logging.getLogger().addFilter(RequestIdFilter())

# Reduce noisy uvicorn logs
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.INFO)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


# -----------------------------
# 4. Routes
# -----------------------------
app.include_router(router)


@app.get("/")
def home():
    return {"message": "AI PDF Agent is running 🚀"}


@app.get("/health")
def health():
    logging.info("Health check endpoint hit")
    return {"status": "ok"}