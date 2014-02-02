__author__ = 'mandrake'
from oldforum.database import MySQLModel
from peewee import *


class ForumModel(MySQLModel):
    forum_id = IntegerField(primary_key=True)
    cat_id = IntegerField()
    forum_name = TextField()
    forum_desc = TextField()

    class Meta:
        db_table = 'phpbb_forums'


class ForumCategoryModel(MySQLModel):
    cat_id = IntegerField(primary_key=True)
    cat_title = TextField()

    class Meta:
        db_table = 'phpbb_categories'