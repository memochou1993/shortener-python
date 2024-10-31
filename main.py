from fastapi import FastAPI
from nanoid import generate

app = FastAPI()


code_dict = dict()

@app.get("/")
def read_root():
    return {"code": generate(size=8)}
