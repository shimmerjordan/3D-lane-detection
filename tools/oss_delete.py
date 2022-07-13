import os
import threading
import re

MAX_THREAD = 64
file_root = "s3://juqiaodan/vis/ganet/ori/v3/tusimple/"
cmd_f = "aws --endpoint-url=http://oss.hh-b.brainpp.cn s3 ls {}"
cmd_ls = cmd_f.format(file_root)


# 删除一个 object /visualization/ganet/
def delete(index, file):
    filepath = file_root + file
    cmd_del = "aws --endpoint-url=http://oss.hh-b.brainpp.cn s3 rm {}".format(filepath)
    thread_index =  simpleHash(file) % MAX_THREAD
    if thread_index == index:
        print("....Thread---" + str(index))
        os.system(cmd_del)

def simpleHash(path):
	value = 0
	for ch in path:
		value += ord(ch)
	return value

# filenames = os.system(cmd_ls)
# filenames = os.popen(cmd_ls)
res = os.popen(cmd_ls).readlines()
filenames = []
for i in range(0, len(res) - 1):  # 由于原始结果需要转换编码，所以循环转为utf8编码并且去除\n换行
    flag = res[i].strip('\n')
    flag = flag.split()
    filenames.append(flag[-1])

# print(filenames)

for file in filenames:
    for i in range(MAX_THREAD):
        t1 = threading.Thread(target=delete,args=(i, file, ))
        t1.start()

os.system("aws --endpoint-url=http://oss.hh-b.brainpp.cn s3 rm {} --recursive".format(file_root))