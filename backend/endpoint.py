from core.app import app


@app.get("/")
async def root():
    return {
        "message": "L'application tourne !",
        "status": "ok",
        "version": "1.0.0",
    }
