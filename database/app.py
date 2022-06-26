# app.py

from database.models.models import Data
from datetime import datetime
from database import session


def upload_data_file_db(data: list, user_id: int):
    all_data_file = []
    for value in data:
        new_data = Data(name=value['Наименование'],
                        order_date=datetime.strptime(value['Дата'], "%m/%d/%Y"),
                        price_1=value['Цена_1'],
                        price_2=value['Цена_2'],
                        price_3=value['Цена_3'],
                        price_4=value['Цена_4'],
                        user_id=user_id)
        all_data_file.append(new_data)
        # add the new data to the database
        session.add_all(all_data_file)
        session.commit()


def get_unique_name_db():
    data_unique_name = []
    for data_name in session.query(Data.name).distinct():
        data_unique_name.append(data_name.name)

    return data_unique_name


def get_data_with_filter_name_and_data(unique_name: str, period_from, period_to):
    all_data_with_filter = session.query(Data).filter(Data.order_date >= period_from). \
        filter(Data.order_date <= period_to).filter(Data.name == unique_name).all()
    return all_data_with_filter
