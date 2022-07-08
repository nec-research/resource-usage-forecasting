from redis import Redis
import numpy as np
import time
from util import load_settings, decoder_to_ndarray


# load settings
settings = load_settings("settings.json")
hostname = settings["Redis_Hostname"]
port = settings["Redis_Port"]
result_channel = settings["Result_Channel_Name"]
tol = settings["Tolerance"]
time_interval = settings["Time_Interval_Check_Update"]

redis_connection = Redis(hostname, port, retry_on_timeout=True)
redis_subscribe = redis_connection.pubsub(ignore_subscribe_messages=True)
redis_subscribe.subscribe(result_channel)
while True:
    message = redis_subscribe.get_message()
    if message is not None:
        d = decoder_to_ndarray(message['data'])
        idx = d[0, 0]
        pm = d[0, 1]
        ub = pm + tol * d[0, 2]
        print('timestamp %d, prediction %.3f, 99.9%% confidence upper bound %.3f' % (idx, pm, ub))
    time.sleep(time_interval)