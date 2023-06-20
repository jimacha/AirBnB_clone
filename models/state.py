#!/usr/bin/python3
"""The state class"""
import models
from models.city import City
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import environ


class State(BaseModel, Base):
    """
    Attributes:
        name: inputs the name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    cities = relationship("City",
                          backref="state",
                          cascade="all, delete-orphan",
                          passive_deletes=True)

    
    if environ.get('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            return [city for city in models.storage.all(
                City).values() if city.state_id == self.id]
