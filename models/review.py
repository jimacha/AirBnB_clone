#!/usr/bin/python3
"""Defines the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represent a review.

    Attributes:
        place_id : The Place id.
        user_id : The User id.
        text : The text of the review.
        all string
    """

    place_id = " "
    user_id = " "
    text = " "