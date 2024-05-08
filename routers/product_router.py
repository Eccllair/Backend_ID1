import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from starlette.responses import FileResponse

from ..models import Product
from ..database import get_async_session

product_router = APIRouter()
product_download_router = APIRouter()

@product_router.post("/")
async def create_product(name: str, price: int,  description:str | None = None, session: AsyncSession = Depends(get_async_session)):
    await session.execute(insert(Product).values(name=name, price=price, description=description))
    await session.commit()


@product_router.get("/{product_id}")
async def get_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        return (await session.execute(select(Product).where(Product.id == product_id))).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"продукта с id[{product_id}] не существует")
        

@product_download_router.get("/")
async def download_product_list(session: AsyncSession = Depends(get_async_session)):
    result = ()
    products = (await session.execute(select(Product))).scalars().all()
    for product in products:
        result += (product.to_dict(),)
        
    with open('idz/tmp_product_lists/list.txt', 'w') as file:
        file.write(json.dumps(result))
    return FileResponse('idz/tmp_product_lists/list.txt', media_type='application/octet-stream',filename='list.txt')
    
