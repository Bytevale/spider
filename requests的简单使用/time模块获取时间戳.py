import time
t = time.time()
print("秒级单位的时间戳", int(t))
print("毫秒级单位的时间戳", int(t*1000))
# 简写一步到位
t2 = int(time.time()*1000)
print(t2)




