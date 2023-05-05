# coding: utf-8
#

from .models import History, get_session

def add_history(trigger: str, ip_address: str) -> int:
    session = get_session()
    new_record = History()
    new_record.trigger = trigger
    new_record.ip_address = ip_address
    session.add(new_record)
    session.commit()

    all_records = session.query(History).all()
    for record in all_records:
        print(record)
        print(record.id, record.ip_address, record.trigger, record.created_at, record.updated_at)

    return new_record.id