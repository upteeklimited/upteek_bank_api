from sqlalchemy.orm import Session
from sqlalchemy import text, inspect
from database.db import Base, engine
import string 
import random
from datetime import datetime
from typing import List, Dict
from settings.config import load_env_config
from database.model import get_last_transaction_type
import dateparser
import time
import re
import json
import os
import importlib
import pkgutil
import inspect
import models
import traceback
import re

config = load_env_config()

def rand_string_generator(size=10):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def rand_upper_string_generator(size=10):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))
    
def rand_lower_string_generator(size=10):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def generate_transaction_reference(tran_type: str = None, rand_type: int = 1, rand_size: int = 10):
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    ts = int(ts)
    if rand_type == 1:
        return str(tran_type).upper() + "_" + rand_string_generator(size=rand_size) + "_" + str(ts)
    elif rand_type == 2:
        return str(tran_type).upper() + "_" + rand_upper_string_generator(size=rand_size) + "_" + str(ts)
    elif rand_type == 3:
        return str(tran_type).upper() + "_" + rand_lower_string_generator(size=rand_size) + "_" + str(ts)

def generate_basic_reference(rand_size: int=10):
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    ts = int(ts)
    return rand_upper_string_generator(size=rand_size) + "_" + str(ts)

def generate_order_reference():
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    ts = int(ts)
    return "#UPORD_" + str(ts)

def generate_transaction_type_code(db: Session):
    last_trans_type = get_last_transaction_type(db=db)
    if last_trans_type is None:
        return "001"
    else:
        return str(last_trans_type.id).zfill(3)

def process_schema_dictionary(info: Dict={}):
    if bool(info) == False:
        return {}
    else:
        retval = {}
        for i in info:
            if info[i] != None:
                retval[i] = info[i]
        return retval
    
def generate_host_id(first_char: str=None, number: int=0):
    # return first_char + str(number).zfill(9)
    return first_char + rand_upper_string_generator(size=number)

def generate_battery_code(number: int=0, length: int=0):
    return "A87" + str(number).zfill(length) + "P"

def process_datetime_string(time_str: str = None):
    if time_str is None:
        return None
    else:
        return dateparser.parse(str(time_str), date_formats=['%d-%m-%Y %H:%M:%S'])
    
def slugify(input_string: str=None, strip: str='-'):
    if input_string is None:
        return None
    else:
        input_string = input_string.encode('ascii', 'ignore').decode('ascii').lower()
        slug = re.sub(r'[^a-z0-9]+', '-', input_string)
        slug = slug.strip(strip)
        return slug
    
def is_valid_json(data: str=None):
    try:
        json.loads(data)
        return True
    except Exception as e:
        return False
    
def truncate_table(table_name: str, db: Session):
    """Truncates a given table and resets identity."""
    try:
        db.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))
        db.commit()
        return {
            'status': True,
            "message": f"Table '{table_name}' truncated successfully!",
        }
    except Exception as e:
        db.rollback()
        return {
            'status': False,
            'message': str(e)
        }
    
# Function to get all table names
def get_all_tables(db: Session):
    inspector = inspect(db.bind)
    return inspector.get_table_names()

# Function to truncate all tables
def truncate_all_tables(db: Session):
    """Truncates all tables in the database."""
    try:
        tables = get_all_tables(db)
        if not tables:
            return {"message": "No tables found in the database!"}

        # Disable foreign key checks (for MySQL) to avoid constraint issues
        db.execute(text("SET session_replication_role = 'replica'"))  # PostgreSQL
        # db.execute(text("SET FOREIGN_KEY_CHECKS=0"))  # Uncomment for MySQL

        for table in tables:
            db.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))

        # Enable foreign key checks back
        db.execute(text("SET session_replication_role = 'origin'"))  # PostgreSQL
        # db.execute(text("SET FOREIGN_KEY_CHECKS=1"))  # Uncomment for MySQL

        db.commit()
        return {
            "status": True,
            "message": f"All tables truncated successfully: {tables}"
        }

    except Exception as e:
        db.rollback()
        err = "Stack Trace - %s \n" % (traceback.format_exc())
        return {"status": False, "message": err}

# def import_models_from_directory():
#     """
#     Dynamically import all models from the models directory
    
#     This function does the following:
#     1. Walks through the models directory
#     2. Imports all Python modules
#     3. Finds all SQLAlchemy model classes that inherit from Base
#     """
#     model_classes = []
    
#     # Iterate through all modules in the models package
#     for _, module_name, _ in pkgutil.iter_modules(models.__path__):
#         try:
#             # Import the module
#             module = importlib.import_module(f'models.{module_name}')
            
#             # Find all classes in the module that inherit from Base
#             for name, obj in inspect.getmembers(module):
#                 if (inspect.isclass(obj) and 
#                     issubclass(obj, Base) and 
#                     obj is not Base and 
#                     hasattr(obj, '__tablename__')):
#                     model_classes.append(obj)
#         except ImportError as e:
#             print(f"Error importing module {module_name}: {e}")
    
#     return model_classes

# def create_tables():
#     try:
#         # Import all model classes
#         models_to_create = import_models_from_directory()
        
#         # Create all tables
#         Base.metadata.create_all(bind=engine)
        
#         # Return the names of tables that were created
#         return {
#             "status": "success", 
#             "tables_created": [model.__tablename__ for model in models_to_create]
#         }
#     except Exception as e:
#         # Handle any errors during table creation
#         return {
#             "status": "error", 
#             "message": str(e)
#         }

def generate_product_sku(prefix: str=None, last_id: int=0):
    return f"{prefix.upper()}-{str(last_id + 1).zfill(10)}"

def generate_product_random_sku(length: int=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_slug(text: str=None):
    """
    Generate a slug from a string by converting to lowercase, replacing spaces and
    special characters with hyphens, and removing non-alphanumeric characters.
    
    Args:
        text (str): The input string to convert to a slug.
        
    Returns:
        str: The generated slug.
    """
    if text is None:
        return None
    else:
        # Convert to lowercase and strip whitespace
        text = text.lower().strip()
        # Replace spaces and special characters with hyphens
        text = re.sub(r'[\s+]', '-', text)
        # Remove all non-alphanumeric characters except hyphens
        text = re.sub(r'[^a-z0-9\-]', '', text)
        # Remove consecutive hyphens
        text = re.sub(r'-+', '-', text)
        # Remove leading/trailing hyphens
        text = text.strip('-')
        return text if text else 'slug'

def comma_to_list(text: str=None):
    """
    Convert a comma-separated string to a list, stripping whitespace from each item.
    
    Args:
        text (str): The comma-separated string to convert.
        
    Returns:
        list: A list of strings from the input.
    """
    # Split by comma and strip whitespace from each item
    if text is None:
        return []
    else:
        return [item.strip() for item in text.split(',') if item.strip()]


def parse_float(string_val: str=None):
    if string_val is None:
        return 0
    try:
        return float(string_val)
    except ValueError:
        return 0
    
def parse_int(string_val: str=None):
    if string_val is None:
        return 0
    try:
        return int(string_val)
    except ValueError:
        return 0

def format_date_for_smile_id(date_str: str=None):
    parsed_date = dateparser.parse(date_str)
    formatted_date = parsed_date.strftime("%Y-%m-%d") if parsed_date else None
    return formatted_date

def format_date_laravel_datetime(date_str: str=None):
    parsed_date = dateparser.parse(date_str)
    formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S") if parsed_date else None
    return formatted_date