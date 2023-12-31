from fastapi import FastAPI, APIRouter
from api_public import router as api_router
from api_internal import router as internal_router

app = FastAPI()
monitoring_router = APIRouter()


@monitoring_router.get("/healthcheck")
def healthcheck():
    return {"message": "HEALTH OK"}


app.include_router(internal_router)
app.include_router(monitoring_router)
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
