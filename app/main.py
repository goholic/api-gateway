from fastapi import FastAPI
from app.middleware import RequestLogger, RateLimitMiddleware

app = FastAPI()

# adding middleware here 
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestLogger)

@app.get("/ping")
async def health_check():
    return {"status": "alive", "service": "api-gateway"}
