# polls/init_db.py
from sqlalchemy import create_engine, MetaData

from settings import config
from db import history


DSN = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"

def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[history])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(history.insert(), [
        {'trigger': 'manual'}
    ])
    # conn.execute(choice.insert(), [
    #     {'choice_text': 'Not much', 'votes': 0, 'question_id': 1},
    #     {'choice_text': 'The sky', 'votes': 0, 'question_id': 1},
    #     {'choice_text': 'Just hacking again', 'votes': 0, 'question_id': 1},
    # ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['mysql'])
    engine = create_engine(db_url)

    # create_tables(engine)
    sample_data(engine)