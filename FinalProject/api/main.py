import uvicorn
from click import clear
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import model_loader
from .dependencies.config import conf

# Routers
from .routers import (
    index as indexRoute,
    sandwiches as sandwiches_router,
    recipes as recipes_router,
    resources as resources_router,
    reviews as reviews_router,
    orders as orders_router,
    order_details as order_details_router,
)

app = FastAPI()

# CORS configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load database models
model_loader.index()

# Load endpoints
indexRoute.load_routes(app)
sandwiches_router.load_routes(app)
recipes_router.load_routes(app)
resources_router.load_routes(app)
app.include_router(reviews_router.router)
app.include_router(orders_router.router)
app.include_router(order_details_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)
