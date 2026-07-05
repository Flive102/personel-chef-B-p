from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from config import get_settings
from middleware import limiter, setup_logging
from api.endpoints import mood, recommendations, users
from database import engine
from models import Base

settings = get_settings()
setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mood-to-Meal Butler API",
    description="AI-powered food recommendations based on emotions",
    version="1.0.0"
)

app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(SlowAPIMiddleware)

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return {"detail": "Rate limit exceeded"}

app.include_router(mood.router, prefix="/api/mood", tags=["mood"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])
app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
