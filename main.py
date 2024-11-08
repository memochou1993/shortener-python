import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from nanoid import generate

from schema.link import LinkCreateRequest, LinkCreateResponse

app = FastAPI()


links = dict()


@app.get("/", tags=["Static"], response_class=HTMLResponse)
def read_root():
    with open(os.path.join("static", "index.html"), "r") as file:
        return HTMLResponse(content=file.read())


@app.post("/api/links", tags=["Link"], response_model=LinkCreateResponse)
def create_link(body: LinkCreateRequest):
    code = generate(size=8)
    links[code] = body.link

    return LinkCreateResponse(code=code)


@app.get("/{code}", tags=["Link"])
def redirect(code: str):
    link = links.get(code)
    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")

    return RedirectResponse(url=link)
