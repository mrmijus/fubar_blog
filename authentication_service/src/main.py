from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
async def root():
    return {"message": "HEALTH OK"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
