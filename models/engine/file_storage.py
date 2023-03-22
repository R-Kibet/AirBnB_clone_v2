#!/usr/bin/python3
""" storage file """

import json
import datetime
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """ instance of the file storage 
	serialization and decerialiation
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ returns the dictionary object"""
        return self.__objects

    def new(self, obj):
        """ sets in __objects the obj with key 
	    self.__objects[object.__class__.__name__ + '.' + str(object)] = obj
	"""
        st1 = obj.__class__.__name__
        st2 = st1 + "." + obj.id
        self.__objects.setdefault(st2, obj)

    def save(self):
        """ serialization to json file 
	
	requirements

	path: __file_path
	w:  write
	"""
	
        with open(self.__file_path, "w", encoding="utf-8") as f:
            a = {k: v.to_dict() for k, v in self.__objects.items()}
            json.dump(a, f)
            
    def classes(self):
        """Returns a dictionary of valid classes and their references"""
       
        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes
        
    def attributes(self):
        """Returns the valid attributes and their types for classname"""
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return attributes

    def reload(self):
        """ deserializes the JSON file to __objects
             only if the JSON file (__file_path) exists
        """	

        try:
            d1 = {}
            d2 = {}

            with open(self.__file_path, "r", encoding="utf-8") as f:
                d1 = json.load(f)

            for key in d1:
                i = d1[key]["__class__"]
                for idx, item in enumerate(self.classes):
                    if i in str(item):
                        a = self.classes[idx](**d1[key])
                d2.setdefault(key, a)
            self.__objects = d2
        except:
                pass

    def delete(self, obj=None):
        ''' deletes the object obj from the attribute
            __objects if it's inside it
        '''
        if obj is None:
            return
        obj_key = obj.to_dict()['__class__'] + '.' + obj.id
        if obj_key in self.__objects.keys():
            del self.__objects[obj_key]

    def close(self):
        """Call the reload method"""
        self.reload()
