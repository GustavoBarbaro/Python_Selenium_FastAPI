"""product.py.

This module contains the Product model.
"""

from pydantic import BaseModel


class Product(BaseModel):
    """Product model.

    This model represents a product with its attributes.
    """

    ID: str
    Name: str
    Category: str
    Price: float
    Stock: str
