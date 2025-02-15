#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User,
           "BaseModel": BaseModel}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        save_objects = models.storage.all()
        for key in save_objects:
            self.assertIs(type(save_objects[key]),
                          classes[save_objects[key].__class__.__name__])

    def test_new(self):
        """test that new adds an object to the database"""
        save_objects = models.storage.all()
        save_count = len(save_objects)
        BaseModel().save()
        self.assertEqual(save_count + 1, len(models.storage.all()))

    def test_save(self):
        """Test that save properly saves objects to file.json"""
        my_model = BaseModel()
        my_model.save()
        self.assertEqual(type(my_model), BaseModel)

    def test_get_file_storage(self):
        """Test that get returns the object based on class and its ID"""
        my_model = BaseModel()
        my_model.save()
        self.assertIs(type(my_model), BaseModel)
        self.assertEqual(my_model.id, models.storage.get(BaseModel,
                                                         my_model.id).id)

    def test_count_file_storage(self):
        """Test that count returns the number of objects in storage"""
        save_objects = models.storage.all()
        self.assertEqual(len(save_objects), models.storage.count())
        self.assertIs(type(models.storage.count()), int)

    def test_get_obj_nonexistent_id(self):
        """Test that get returns None if no object with that ID exists"""
        self.assertIsNone(models.storage.get(self.__class__.__name__, "123"))

    def test_get_nonexistent_class(self):
        """Test that get returns None if no object with that class exists"""
        self.assertIsNone(models.storage.get("123", "123"))

    def test_count_no_class(self):
        """Test that count returns 0 if no object with that class exists"""
        self.assertIs(models.storage.count("Some Class"), len(classes))
