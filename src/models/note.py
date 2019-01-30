import datetime
import uuid

from src.common.database import Database


class Note(object):

    def __init__(self, title, content, due_date, class_id, date=datetime.datetime.utcnow(), _id=None):
        self.title = title
        self.content = content
        self.due_date = due_date
        self.class_id = class_id
        self.date = date
        self._id = uuid.uuid4().hex if _id is None else _id
        # this id is the note id




    # saving to database methods
    def json(self):
        """Returns a json representation of the Note object"""
        return {
            'title': self.get_title(),
            'content': self.get_content(),
            'due_date': self.get_due_date(),
            'class_id': self.get_class_id(),
            'date': self.get_date(),
            '_id': self.get_id()
        }
    def save_note_to_mongo(self):
        """Saves the Note object into the database's 'notes' collection"""
        Database.insert(collection='notes',
                        data=self.json())




    # retrieving note from database methods
    @classmethod
    def get_note_by_id(cls, id):
        """Returns a single Note object by its _id attribute"""
        note = Database.find_one(collection='notes',
                                 query={'_id': id})
        return cls(**note)
    @classmethod
    def get_notes_by_date(cls, date):
        """Returns a list of Note objects by their date"""
        notes = Database.find(collection='notes',
                              query={'date':date})
        return [cls(**note) for note in notes]
    @classmethod
    def get_notes_by_due_date(cls, due_date):
        """Returns a list of Note objects by their due_date"""
        notes = Database.find(collection='notes',
                              query={'due_date':due_date})
        return [cls(**note) for note in notes]




    # deleting Note from database methods
    def delete_note(self):
        """Removes the note from the database"""
        Database.remove(collection='notes',
                        query={'_id': self.get_id()})

    # deleting note in database
    def update_note(self, updated_note):
        """Removes the note from database"""
        Database.update(collection='notes',
                        query={'_id': self.get_id()},
                        update=updated_note)



    # the get methods
    def get_title(self):
        return self.title

    def get_content(self):
        return self.content

    def get_due_date(self):
        return self.due_date

    def get_date(self):
        return self.date

    def get_class_id(self):
        return self.class_id

    def get_id(self):
        return self._id

    # the set methods
    def set_title(self, new_title):
        self.title = new_title

    def set_content(self, new_content):
        self.content = new_content

    def set_due_date(self, new_due_date):
        self.due_date = new_due_date

    def set_date(self, new_date):
        self.date = new_date

    def set_class_id(self, new_class_id):
        self.class_id = new_class_id

    def set__id(self, new__id):
        self._id = new__id
