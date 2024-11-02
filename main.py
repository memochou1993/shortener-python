from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from nanoid import generate

from schema.link import LinkCreateRequest, LinkCreateResponse

app = FastAPI()


links = dict()


@app.post("/api/links", tags=["Link"], response_model=LinkCreateResponse)
def read_root(body: LinkCreateRequest):
    code = generate(size=8)
    links[code] = body.link

    return LinkCreateResponse(code=code)


@app.get("/{code}", tags=["Link"])
def read_item(code: str):
    link = links.get(code)
    if link:
        return RedirectResponse(url=link)

    raise HTTPException(status_code=404, detail="Link not found")
