import datetime
import uuid

from src.common.database import Database
from src.models.note import Note


class Class(object):

    def __init__(self, title, description, active, _id=None):
        self.title = title
        self.description = description
        self.active = active # Can be one of two values: "active" / "inactive"
        self._id = uuid.uuid4().hex if _id is None else _id
        # this is the id for the class


    # saving to database methods
    def json(self):
        return {
            'title':self.get_title(),
            'description':self.get_description(),
            'active':self.get_active(),
            '_id':self.get_id()
        }
    def save_class_to_mongo(self):
        Database.insert(collection='classes',
                        data=self.json())



    # accessing class from database methods
    @classmethod
    def get_class_by_id(cls, id):
        class_ = Database.find_one(collection='classes',
                                   query={'_id':id})
        return Class(**class_)
    @classmethod
    def get_active_classes(cls, id):
        classes = Database.find(collection='classes',
                                query={'active':'active'})



    # accessing notes belonging to a certain class
    def get_notes_from_class(self):
        """Returns a list of Notes made for this Class"""
        notes = Database.find(collection='notes',
                              query={'class_id': self.get_id()})
        return [Note(note) for note in notes]




    # deleting class in database
    def delete_class(self):
        """Removes the class and its notes from database"""
        Database.remove(collection='classes',
                        query={'_id':self.get_id()})
        Database.remove(collection='notes',
                        query={'class_id':self.get_id()})





    # the get methods
    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_active(self):
        return self.active

    def get_id(self):
        return self._id

    # the set methods
    def set_title(self, new_title):
        self.title = new_title

    def set_description(self, new_description):
        self.description = new_description

    def set_active(self, new_active):
        self.active = new_active

    def set_id(self, new__id):
        self._id = new__id
