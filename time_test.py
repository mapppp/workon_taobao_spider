import time

print(time.time())
print(time.strftime("%m-%d-%H-%M", time.localtime(time.time())))