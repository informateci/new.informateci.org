__author__ = 'mandrake'

import secure
from peewee import *

mysql_db = MySQLDatabase('informateci', user=secure.SECURE['mysql_user'], passwd=secure.SECURE['mysql_password'])


class MySQLModel(Model):
    class Meta:
        database = mysql_db

mysql_db.connect()