# coding: utf-8

from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date, DateTime
)
import datetime

meta = MetaData()

history = Table('history', meta, 
                Column('id', Integer, primary_key=True),
                Column('gmt_create', DateTime, default=datetime.datetime.now),
                Column('gmt_modified', DateTime, default=datetime.datetime.now),
                Column('trigger', String, default='manual'))