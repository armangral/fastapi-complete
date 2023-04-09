from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from . import models
from . database import engine
from . routers import post,user,auth
from fastapi.middleware.cors import CORSMiddleware



"""Create a FastAPI application instance"""
app = FastAPI()

"""Create a Jinja2Templates instance to manage the HTML templates"""
templates = Jinja2Templates(directory="templates")

"""Set up Cross-Origin Resource Sharing (CORS) middleware to allow communication with other domains"""
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""Include the routers for the different API endpoints"""    
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


    
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    'Renders HTML template with request'
    """
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
