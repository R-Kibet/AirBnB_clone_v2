#!/usr/bin/python3

"""THe base lass for the project"""

import uuid
from models import storage
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """parent class
   class Atributes:
        id: uuid
        created_at: datetime
	updated_at: datetime

    methods:
        __str__: prints naem,id, and creates dict
        save(self): save updated intance class attribute 
        to_dict: value f dctionary
    """
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))

    def __init__(self, *args, **kwargs):
        """initialize attributes"""

        FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

        if len(kwargs) == 0:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
        else:
            """ we check the key word arguents"""
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                                        kwargs["created_at"], FORMAT)
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                                        kwargs["updated_at"], FORMAT)
                else:
                    self.__dict__[key] = kwargs[key]

    """METHODS"""
    def __str__(self):
        """ Return string format"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
			             self.id, self.__dict__)
    def save(self):
        """updates attribute update_at"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """dictionary containing all key and values"""
        dic = self.__dict__.copy()
        dic["__class__"] = self.__class__.__name__
        dic["created_at"] = self.created_at.isoformat()
        dic["updated_at"] = self.updated_at.isoformat()
        return dic

    def delete(self):
        """ delete object
        """
        storage.delete(self)
