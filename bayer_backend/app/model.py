import json
import uuid
import pymongo
import hashlib

MONGO_URL = "localhost"
MONGO_PORT = 27017
LINK = ''

class Product:
    def __init__(self, obj=None):
        self.__name = obj.name if obj else None
        self.__description = obj.description if obj else None
        self.__price = obj.price if obj else None
        self.__how_to = json.loads(obj.how_to) if obj else None
        self.__distributor = obj.distributor if obj else None
        self.__category = obj.category if obj else None
        self.__archive = False

    def get_description(self):
        return self.__description

    def get_price(self):
        return self.__price
    
    def get_how_to(self):
        return self.__how_to

    def get_distributor(self):
        return self.__distributor

    def get_category(self):
        return self.__category

    def get_archive_status(self):
        return self.__archive

    def get_info(self):
        return {
            '_id': self.__name,
            'description': self.get_description(),
            'price': self.get_price(),
            'how_to': self.get_how_to(),
            'distributor': self.get_distributor(),
            'category': self.get_category(),
            'archive': self.get_archive_status()
        }

    def register(self):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            p_col = db.product
            c_col = db.category

            val = self.get_info()
            p_col.insert_one(val)
            c_col.update_one({'_id':val['category']}, {'$inc': {'count':1}})
        except Exception as e:
            raise e

    def update(self):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            p_col = db.product
            c_col = db.category

            val = self.get_info()
            old_category = p_col.find_one({'_id':self.__name}, {'category':1})['category']
            if old_category != self.__category:
                c_col.update_one({'_id':old_category}, {'$inc':{'count': -1}})
                c_col.update_one({'_id':self.__category}, {'$inc':{'category':1}})

            prod_id = val['_id']
            del val['_id']
            p_col.update_one({'_id':prod_id}, {'$set': val})
        except Exception as e:
            raise e

    def get(self, prod_id):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.product
        
            return col.find_one({"_id": prod_id})
        except Exception as e:
            raise e

    def delete(self, prod_id):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            p_col = db.product
            c_col = db.category
        
            p_col.delete_one({"_id": prod_id})
            c_col.update_one({'_id':prod_id}, {'$inc':{'count': -1}})
        except Exception as e:
            raise e

    def archive(self, prod_id):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.product
        
            col.update_one({"_id": prod_id}, {'$set':{'archive':True}})
        except Exception as e:
            raise e

    def unarchive(self, prod_id):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.product
        
            col.update_one({"_id": prod_id}, {'$set':{'archive':False}})
        except Exception as e:
            raise e

class Category:
    def __init__(self, obj=None):
        self.__name = obj.name if obj else None
        self.__description = obj.description if obj else None
        self.__archive = False
        self.__product_count = 0

    def get_description(self):
        return self.__description

    def get_archive_status(self):
        return self.__archive

    def get_info(self):
        return {
            '_id': self.__name,
            'description': self.get_description(),
            'archive': self.get_archive_status(),
            'count': self.__product_count
        }

    def register(self):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.category
            
            val = self.get_info()
            col.insert_one(val)
        except Exception as e:
            raise e

    def update(self):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.category

            val = self.get_info()
            prod_id = val['_id']
            del val['_id']
            col.update_one({'_id':prod_id}, {'$set': val})
        except Exception as e:
            raise e

    def get(self, category_id):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.category
        
            return col.find_one({"_id": category_id})
        except Exception as e:
            raise e
    
    def delete(self, category_id):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            p_col = db.product
            c_col = db.category

            c_col.delete_one({"_id": category_id})
            p_col.delete_many({'category': category_id})
        except Exception as e:
            raise e

    def get_product_count(self, category_id):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.category
        
            return col.find_one({"_id": category_id}, {'count': 1})
        except Exception as e:
            raise e

    def archive(self, category_id):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.category

            col.update_one({"_id": category_id}, {'$set': {'archive': True}})
        except Exception as e:
            raise e

    def unarchive(self, category_id):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.category

            col.update_one({"_id": category_id}, {'$set': {'archive': False}})
        except Exception as e:
            raise e

class Feedback:
    def __init__(self, obj):
        self.__prodect_id = obj.project_id
        self.__comment = obj.comment

    def register(self):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.feedback
            
            col.insert_one({'project_id': self.__prodect_id, 'comment': self.__comment})
        except Exception as e:
            raise e

class Distrbutor:
    def __init__(self, obj):
        self.__name = obj.name
        self.__parent = obj.parent
        self.__company_name = obj.company_name
        self.__country = obj.counter
        self.__state = obj.state
        self.__pincode = obj.pincode
        self.__number = obj.number

    def get_parent(self):
        return self.__parent

    def get_name(self):
        return self.__name

    def get_company_name(self):
        return self.__company_name

    def get_country(self):
        return self.__country

    def get_state(self):
        return self.__state

    def get_pincode(self):
        return self.__pincode

    def get_number(self):
        return self.__number

    def get_info(self):
        val = {
            '_id': self.get_name(),
            'company name': self.get_company_name(),
            'country': self.get_country(),
            'state': self.get_state(),
            'pincode': self.get_pincode(),
            'number': self.get_number()
        }

        return val

    def register(self):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            d_col = db.distributor
            
            val = self.get_info()
            d_col.insert_one(val)
        except Exception as e:
            raise e

    def update(self):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            d_col = db.distributor

            val = self.get_info()
            d_col.update_one({'_id':self.__name}, {'$set': val})
        except Exception as e:
            raise e

    def get(self, dis_id):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            d_col = db.distributor
        
            return d_col.find_one({"_id": dis_id})
        except Exception as e:
            raise e

    def delete(self, dis_id):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            d_col = db.distributor
        
            d_col.delete_one({"_id": dis_id})
        except Exception as e:
            raise e

    def find_parent(self, dis_id):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.distributor

            return col.find_one({'_id': col.find_one({'_id':dis_id}, {'parent':1})['parent']})
        except Exception as e:
            raise e

    def make_family_tree(self, dis_id):
        try:
            tree = [self.get(dis_id)]
            parent = self.find_parent(dis_id)
            while  parent:
                tree.append(self.get(dis_id))
                parent = self.find_parent(parent)
            
            return tree
        except Exception as e:
            raise e

class Order:
    def __init__(self, obj):
        self.__product_id = obj.product_id
        self.__distributor_id = obj.distributor_id
        self.__buyer = None
        self.__sold = False
        self.__printed = False

    def register(self):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.order
            
            order_id = uuid.uuid4()
            val = {
                '_id': order_id,
                'product_id': self.__product_id,
                'distributor_id': self.__distributor_id,
                'buyer': self.__buyer,
                'sold': self.__sold,
                'printed': self.__printed
            }

            col.insert_one(val)
        except Exception as e:
            raise e

    def register_buyer(self, item_id, hash_number):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.order
            
            col.update_one({'_id': item_id}, {'$set': {'buyer': hash_number, 'sold': True}})
        except Exception as e:
            raise e
    
    def authenticate_buyer(self, item_id, hash_number):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.order
            
            return col.find_one({'_id': item_id}, {'buyer': 1}) == hash_number
        except Exception as e:
            raise e

    def get(self, prod_id, dis_id):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.order
            
            return col.find_one({'product_id': prod_id, "distributor_id": dis_id, 'printed':False}, {'_id': 1})
        except Exception as e:
            raise e

    def print(self, item_id):
        try:
            client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
            db = client.stock
            col = db.order
            
            col.update_one({'_id': item_id}, {'$set': {'printed': True}})
        except Exception as e:
            raise e