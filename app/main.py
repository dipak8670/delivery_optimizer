from fastapi import FastAPI

app = FastAPI(title="Delivery Optimizer")


@app.get("/health")
def health_check():
    return {"status": "ok"}
