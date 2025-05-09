
def generate_gl_type_code(type_number: int=0, last_id: int=0):
    last_id = last_id + 1
    return str(type_number) + str(last_id).zfill(8)

def generate_internal_account_number(product_type: int=0, last_id: int=0):
    last_id = last_id + 1
    return str(product_type) + str(last_id).zfill(9)

def generate_internal_gl_number(type_code: str=None, last_id: int=0):
    last_id = last_id + 1
    return str(type_code).zfill(8) + str(last_id).zfill(5)

def generate_account_type_code(product_type: int=0, last_id: int=0):
    last_id = last_id + 1
    return str(product_type) + str(last_id).zfill(6)