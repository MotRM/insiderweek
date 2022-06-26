# dramamtiq_worker.py

import dramatiq
from dramatiq.brokers.redis import RedisBroker

from database.app import upload_data_file_db
from utils.csv_reader import csv_reader

redis_broker = RedisBroker()
dramatiq.set_broker(redis_broker)


@dramatiq.actor(time_limit=100000000)
def upload_datafile_in_db(filepath: str, user_id: int):
    data = csv_reader(filepath)
    upload_data_file_db(data, user_id)
