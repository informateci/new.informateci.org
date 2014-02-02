__author__ = 'mandrake'
from oldforum.database import MySQLModel
from peewee import *


class UserModel(MySQLModel):
    user_id = IntegerField(primary_key=True)
    username = TextField()

    class Meta:
        db_table = 'phpbb_users'