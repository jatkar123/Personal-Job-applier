from fastapi import FastAPI

app = FastAPI(title="Personal Job Applier API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
