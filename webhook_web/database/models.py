# coding: utf-8

import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///web.db', echo=True)
Base = declarative_base()  #<-元类


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column('created_at', DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime,
                        default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)
    trigger = Column(String(30), default="manual", nullable=False)
    ip_address = Column(String(20))

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_session():
    session = Session()
    return session


def test():
    session = get_session()

    # 创建一条记录
    new_record = History()
    # new_record.updated_at = datetime.datetime.now()
    session.add(new_record)
    session.commit()

    # 查询所有记录
    all_records = session.query(History).all()
    for record in all_records:
        print(record.id, record.created_at, record.updated_at)

    # 更新一条记录
    record_to_update = session.query(History).first()
    # record_to_update.updated_at = datetime.datetime.now()
    session.commit()

    # 删除一条记录
    record_to_delete = session.query(History).first()
    session.delete(record_to_delete)
    session.commit()

    session.close()