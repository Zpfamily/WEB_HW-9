from datetime import datetime

from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField, ReferenceField
import connect


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    description = StringField()
    born_location = StringField()


class Quote(Document):
    quote = StringField(required=True)
    tags = ListField(StringField())
    author = ReferenceField(Author)



