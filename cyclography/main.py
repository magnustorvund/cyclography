from fastapi import FastAPI
from routes import router


app = FastAPI(
    title="Cyclography",
    description="An overview of public bike availability",
    version="0.1.0",
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
