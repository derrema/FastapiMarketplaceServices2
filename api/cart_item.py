from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from database.models import CartItem
from database.schemas import CartItemOutSchema, CartItemInputSchema
from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy import select

router = APIRouter(prefix='/cart_item', tags=['CartItem'])

@router.post('/', response_model=CartItemOutSchema, tags=['CartItem'])
async def post(schema: CartItemInputSchema, db: AsyncSession = Depends(get_db)):
    query = select(CartItem).where(CartItem.cart_id==schema.cart)
    result = await db.execute(query)
    scal = result.scalar_one_or_none()

    if not scal:
        raise HTTPException(detail=f'No cart with id {schema.cart}', status_code=status.HTTP_404_NOT_FOUND)

    cart_item = CartItem(**schema.model_dump())

    db.add(cart_item)
    await db.commit()
    await db.refresh(cart_item)
    return cart_item

@router.get('/', response_model=CartItemOutSchema, tags=['CartItem'])
async def get(cart_item: int, db: AsyncSession = Depends(get_db)):
    query = select(CartItem).where(CartItem.id==cart_item)
    result = await db.execute(query)
    scal = result.scalar_one_or_none()

    if not scal:
        raise HTTPException(detail=f'No cart with id {cart_item}', status_code=status.HTTP_404_NOT_FOUND)

    return scal

@router.put('/', response_model=CartItemOutSchema, tags=['CartItem'])
async def put(
        cart_item: int,
        schema: CartItemInputSchema,
        db: AsyncSession = Depends(get_db)
):
    query = select(CartItem).where(CartItem.id==cart_item)
    result = await db.execute(query)
    scal = result.scalar_one_or_none()

    if not scal:
        raise HTTPException(detail=f'No cart with id {cart_item}', status_code=status.HTTP_404_NOT_FOUND)

    update_data = schema.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(scal, key, value)

    await db.commit()
    await db.refresh(scal)
    return scal

@router.delete('/', response_model=dict, tags=['CartItem'])
async def delete(cart_item: int, db: AsyncSession = Depends(get_db)):
    query = select(CartItem).where(CartItem.id==cart_item)
    result = await db.execute(query)
    scal = result.scalar_one_or_none()

    if not scal:
        raise HTTPException(detail=f'No carts items with id {cart_item}', status_code=status.HTTP_404_NOT_FOUND)

    await db.delete(scal)
    await db.commit()
    return {'detail': 'Carts items has been deleted'}