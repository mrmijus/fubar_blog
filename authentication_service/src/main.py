from fastapi import FastAPI, Depends

app = FastAPI()


@app.get("/healthcheck")
async def root():
    return {"message": "HEALTH OK"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
