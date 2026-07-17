from database.models import *
from sqladmin import ModelView

class CartAdmin(ModelView, model=Cart):
    column_list = [i.key for i in Cart.__mapper__.columns]

class CartItemAdmin(ModelView, model=CartItem):
    column_list = [i.key for i in CartItem.__mapper__.columns]