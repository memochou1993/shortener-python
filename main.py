import os

import supabase
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from nanoid import generate

from schema.link import LinkCreateRequest, LinkCreateResponse

load_dotenv()


app = FastAPI()


supabase_client = supabase.create_client(
    os.getenv("SUPABASE_API_URL"),
    os.getenv("SUPABASE_API_KEY"),
)


@app.get("/", tags=["Static"], response_class=HTMLResponse)
def read_root():
    with open(os.path.join("static", "index.html"), "r") as file:
        return HTMLResponse(content=file.read())


@app.post("/api/links", tags=["Link"], response_model=LinkCreateResponse)
def create_link(body: LinkCreateRequest):
    code = generate(size=8)

    result = (
        supabase_client.from_("links")
        .insert(
            {
                "code": code,
                "link": str(body.link),
            }
        )
        .execute()
    )

    return LinkCreateResponse(**result.data[0])


@app.get("/{code}", tags=["Link"])
def redirect(code: str):
    result = supabase_client.from_("links").select("*").eq("code", code).execute()

    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")

    url = result.data[0]["link"]

    return RedirectResponse(url=url)
