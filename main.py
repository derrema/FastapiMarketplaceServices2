from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import cart, cart_item
import uvicorn
from admin.setup import admin_setup

app = FastAPI()
app.include_router(cart.router)
app.include_router(cart_item.router)

admin_setup(app)

origins = [
    'http://localhost',
    'http://localhost:3000',
    'http://frontend'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)