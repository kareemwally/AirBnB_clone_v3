#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return FileStorage.__objects
        else:
            cls_objects = {}
            for key, value in FileStorage.__objects.items():
                if type(value) == cls:
                    cls_objects[key] = value
            return cls_objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it’s inside"""
        if obj is None:
            return
        key = obj.to_dict()['__class__'] + '.' + obj.id
        if key in FileStorage.__objects:
            del FileStorage.__objects[key]

    def close(self):
        """Call reload method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """Retrieve one object based on class and ID"""
        if cls is None or id is None:
            return None
        key = f"{cls.__name__}.{id}"
        return self.__objects.get(key, None)

    def count(self, cls=None):
        """Count the number of objects in storage matching the given class"""
        if cls is None:
            return len(self.__objects)
        return len(self.all(cls))
