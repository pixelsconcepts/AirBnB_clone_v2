#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import models
from models.city import City
import shlex


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        """
        returns the list of City instances with
        state_id equals to the current State.id
        """
        all_obj = models.storage.all()
        list_all_cities = []
        list_state_cities = []

        for key in all_obj:
            obj = key.replace('.', ' ')
            obj = shlex.split(obj)

            if obj[0] == 'City':
                list_all_cities.append(all_obj[key])

        for element in list_all_cities:
            if element.state_id == self.id:
                list_state_cities.append(element)

        return (list_state_cities)
