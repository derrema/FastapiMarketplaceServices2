from fastapi import HTTPException, APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from database.schemas import CartInputSchema, CartOutSchema
from database.models import Cart
from sqlalchemy import select

router = APIRouter(prefix='/cart', tags=['Cart'])

@router.post('/', response_model=CartOutSchema, tags=['Cart'])
async def post(schema: CartInputSchema, db: AsyncSession = Depends(get_db)):
    query = select(Cart).where(Cart.owner==schema.owner)
    result = await db.execute(query)
    scal = result.scalar_one_or_none()

    if scal:
        raise HTTPException(detail=f'Owner with id {schema.owner} already exists', status_code=status.HTTP_409_CONFLICT)

    cart = Cart(owner=schema.owner)
    db.add(cart)
    await db.commit()
    await db.refresh(cart)
    return cart

@router.get('/', response_model=CartOutSchema, tags=['Cart'])
async def get(owner_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Cart).where(Cart.owner==owner_id)
    result = await db.execute(query)
    scal = result.scalar_one_or_none()

    if not scal:
        raise HTTPException(detail=f'No owner with id {owner_id}', status_code=status.HTTP_404_NOT_FOUND)

    return scal

@router.delete('/', response_model=dict, tags=['Cart'])
async def delete(owner_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Cart).where(Cart.owner==owner_id)
    result = await db.execute(query)
    scal = result.scalar_one_or_none()

    if not scal:
        raise HTTPException(detail=f'No owner with id {owner_id}', status_code=status.HTTP_404_NOT_FOUND)

    await db.delete(scal)
    await db.commit()
    return {'detail': 'Cart has been deleted'}