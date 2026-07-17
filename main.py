from fastapi import FastAPI
from api import cart, cart_item
import uvicorn
from admin.setup import admin_setup

app = FastAPI()
app.include_router(cart.router)
app.include_router(cart_item.router)

admin_setup(app)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)