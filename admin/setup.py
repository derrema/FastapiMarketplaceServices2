from sqladmin import Admin
from database.connection import async_engine
from admin.views import *
from fastapi import FastAPI

def admin_setup(app: FastAPI):
    admin = Admin(app, async_engine)
    admin.add_view(CartAdmin)
    admin.add_view(CartItemAdmin)