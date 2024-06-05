from fastapi import FastAPI
import models
from database import engine
from router import to_do, user, authentication


app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(to_do.router)
app.include_router(user.router)













# templates = Jinja2Templates(directory="templates")

# @app.get("/", response_class=HTMLResponse)
# def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request":request, "short_url": None})

# @app.post("/", response_class=HTMLResponse)
# def create_short_url(request:Request, original_url: str = Form(...)):
#     short_url = "http://short.url/" + original_url[-6:]
#     return templates.TemplateResponse("index.html", {"request":request, "short_url": short_url})