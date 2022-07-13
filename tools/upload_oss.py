import os
import time
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler

logging.basicConfig(level=logging.INFO, filename='./upload_log.log', filemode='a+', format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
maxThread = 64

class LogHandler(LoggingEventHandler):
    def on_created(self, event):
        path = event.src_path
        if event.is_directory:
            pass
        else:
            logging.info(path + "文件新增")
            # pass

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        path = event.src_path
        file_name = os.path.basename(path)
        if file_name.endswith("jpg") or file_name.endswith("png") or file_name.endswith("jpeg"):
            for i in range(maxThread):
                t1 = threading.Thread(target=upload,args=(path, file_name, i,))
                t1.start()
            # print(path)
            # print(path.split('/')[-1])
        else:
            pass
        # print(event)


def simpleHash(path):
	value = 0
	for ch in path:
		value += ord(ch)
	return value

def upload(abs_file, file, index):
    thread_index =  simpleHash(file) % maxThread
    if thread_index == index:
        cmd_f = "aws --endpoint-url=http://oss.hh-b.brainpp.cn s3 cp {} s3://juqiaodan/vis/ganet/ori/v3/tusimple/{}"
        cmd = cmd_f.format(abs_file, file)
        print("....Thread---" + str(index))
        os.system(cmd)

def loadDir(abs_dir):
    filePath = abs_dir
    file_list = os.listdir(filePath)
    for file in file_list:
        upload(filePath + file, file)

   
def main():
    event_handler = MyHandler()
    observer = Observer()
    watch = observer.schedule(event_handler, path='/data/vis/ganet/ori/tusimple', recursive=False)

    log_handler = LogHandler()
    observer.add_handler_for_watch(log_handler, watch)  # 写入日志
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    main()