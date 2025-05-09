from pydantic import BaseModel

class Product(BaseModel):
    ID: str
    Name: str
    Category: str
    Price: float
    Stock: str
