import sys
from fastapi import FastAPI, Response, status
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from model import Product, Category, Feedback, Distrbutor, Order

app = FastAPI()

class ProductModel(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    how_to: Optional[str] = None
    distributor: str
    category: Optional[str] = None

class DistributorModel(BaseModel):
    name: str
    parent: Optional[str] = None
    company_name: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    pincode: int
    number: Optional[str] = None

class CategoryModel(BaseModel):
    name: str
    description: Optional[str] = None

class FeedbackModel(BaseModel):
    project_id: str
    comment: Optional[str] = None

class ItemModel(BaseModel):
    project_id: str
    distrbutor_id: str
    count: int

@app.get("/")
async def read_root():
    return "Hello world!!"

@app.post("/product/")
async def create_product(product: ProductModel, response: Response):
    try:
        p = Product(product)
        p.register()
        res = {'Product registered': True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Product registered': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.put("/product/")
async def update_product(product: ProductModel, response: Response):
    try:
        p = Product(product)
        p.update()
        res = {'Product Update': True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Product Update': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.get("/product/{prod_id}")
async def get_product(prod_id: str, response: Response):
    try:
        p = Product()
        res = p.get(prod_id)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e)}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.put("/product/archive/{prod_id}")
async def archive_product(prod_id: str, response: Response):
    try:
        p = Product()
        p.archive(prod_id)
        res = {'Product Archive': True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Product Archive': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.put("/product/unarchive/{prod_id}")
async def unarchive_product(prod_id: str, response: Response):
    try:
        p = Product()
        p.unarchive(prod_id)
        res = {'Product UnArchive': True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Product UnArchive': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.delete("/product/{prod_id}")
async def delete_product(prod_id: str, response: Response):
    try:
        p = Product()
        p.delete(prod_id)
        res = {'Product Deleted': True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Product Deleted': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.put("/feedback/")
async def delete_product(feedback: FeedbackModel, response: Response):
    try:
        f = Feedback(feedback)
        f.register()
        res = {'Feedback Registered': True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Feedback Registered': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.post("/category/")
async def create_category(category: CategoryModel, response: Response):
    try:
        c = Category(category)
        c.register()
        res = {"Category Added": True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Category Added': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.put("/category/")
async def update_category(category: CategoryModel, response: Response):
    try:
        c = Category(category)
        c.update()
        res = {'Category Update': True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Category Update': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.get("/category/{cat_id}")
async def get_category(cat_id: str, response: Response):
    try:
        c = Category()
        res = c.get(cat_id)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e)}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.put("/category/archive/{cat_id}")
async def archive_category(cat_id: str, response: Response):
    try:
        c = Category()
        c.archive(cat_id)
        res = {'Category Archive': True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Category Archive': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.put("/category/unarchive/{prod_id}")
async def unarchive_category(cat_id: str, response: Response):
    try:
        c = Category()
        c.unarchive(cat_id)
        res = {'Category UnArchive': True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Category UnArchive': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.delete("/category/{cat_id}")
async def delete_category(cat_id: str , response: Response):
    try:
        c = Category()
        c.delete(cat_id)
        res = {'Category Deleted': True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Category Deleted': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.get("/category/count/{cat_id}")
async def category_count(cat_id: str , response: Response):
    try:
        c = Category()
        res = c.get_product_count(cat_id)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e)}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.post("/distributor/")
async def create_distributor(distributor: DistributorModel, response: Response):
    try:
        c = Distrbutor(distributor)
        c.register()
        res = {"Distrbutor Added": True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Distrbutor Added': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.put("/distributor/")
async def update_distributor(distributor: DistributorModel, response: Response):
    try:
        c = Distrbutor(distributor)
        c.update()
        res = {'Distrbutor Update': True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Distrbutor Update': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.get("/distributor/{dis_id}")
async def get_distributor(dis_id: str, response: Response):
    try:
        c = Distrbutor()
        res = c.get(dis_id)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e)}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.get("/distributor/family/{dis_id}")
async def family_distributor(dis_id: str, response: Response):
    try:
        c = Distrbutor()
        res = c.make_family_tree(dis_id)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e)}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.delete("/distributor/{dis_id}")
async def delete_distributor(dis_id: str , response: Response):
    try:
        c = Distrbutor()
        c.delete(dis_id)
        res = {'Distrbutor Deleted': True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Distrbutor Deleted': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.post("/items/")
async def create_items(item: ItemModel, response: Response):
    try:
        o = Order(item)
        o.register(item.count)
        res = {'Items Added': True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Items Added': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.get("/items/{prod_id}/{dis_id}")
async def get_items(prod_id: str, dis_id: str, response: Response):
    try:
        o = Order()
        val = o.get(prod_id, dis_id)
        res = {'Unregistered Item ids': val}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Items Added': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.put("/items/{item_id}")
async def print_items(item_id: str, response: Response):
    try:
        o = Order()
        o.print(item_id)
        res = {'Item tag printed': True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Item tag printed': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)

@app.put("/items/buyer/{item_id}/{hnumber}")
async def print_items(item_id: str, hnumber: str, response: Response):
    try:
        o = Order()
        o.authenticate_buyer(item_id, hnumber)
        res = {'buyer Added': True}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e), 'Item tag printed': False}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)


@app.get("/items/auth/{item_id}")
async def get_items(item_id: str, response: Response):
    try:
        o = Order()
        val = o.authenticate_buyer(item_id)
        res = {'Product Authentic': val}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        res = {'error': str(e)}
    finally:
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)