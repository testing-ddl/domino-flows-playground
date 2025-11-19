from datetime import datetime
import time
import random


# current_time = datetime.now().strftime('%M:%S')
# while True:
#     if current_time.endswith("0:00") or current_time.endswith("5:00"):
#         break
#     time.sleep(0.01)

with open("/mnt/artifacts/f_"+str(random.random())+"txt", "w") as f:
    f.write(str(random.random()))
