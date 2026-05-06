from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import uuid
from fastapi.middleware.cors import CORSMiddleware
from app.core.request_context import set_request_id, get_request_id
from app.api.routes import router

app = FastAPI(title="AI PDF Agent")

# -----------------------------
# 1. Middleware: request_id injection
# -----------------------------
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]

    # store in context
    set_request_id(request_id)

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    return response


# -----------------------------
# 2. Logging setup (centralized)
# -----------------------------
class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = get_request_id() or "no-request"
        return True


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logging.getLogger().addFilter(RequestIdFilter())

# Reduce noisy logs
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.INFO)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# 3. Routes
# -----------------------------
app.include_router(router)


@app.get("/")
def home():
    return {"message": "AI PDF Agent is running 🚀"}


@app.get("/health")
def health():
    logging.info("Health check endpoint hit")
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-pdf-agent.vercel.app",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)