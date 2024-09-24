from fastapi import FastAPI
from routes import router  # Adjust the import based on your project structure


app = FastAPI(
    title="Cyclography",
    description="An overview of public bikes",
    version="0.1.0",
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
