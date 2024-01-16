#!venv/Scripts/python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/15 13:16
# @File    : main.py
# @Software: IntelliJ IDEA

import http.server
import os
import socketserver
import sys
import time
import warnings
from datetime import datetime, timedelta

import pytz
import yaml
from ics import Calendar, Event, DisplayAlarm
from loguru import logger
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

warnings.filterwarnings("ignore")
cur_path = os.path.dirname(os.path.abspath(__file__))
last_path = os.path.dirname(cur_path)
result_path = os.path.join(cur_path, 'result')
os.makedirs(result_path, exist_ok=True)
# 配置日志文件，保存在log目录下，当日志达到20M时，自动分割，最长保留30天
logger.add(
    os.path.join(cur_path, 'log', 'runserver.log'), rotation="20 MB", retention="30 days", encoding='utf-8', enqueue=True
)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=result_path, **kwargs)


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path, callback):
        super().__init__()
        self.file_path = file_path
        self.callback = callback

    def on_modified(self, event):
        if event.src_path == self.file_path:
            self.callback()


class MyTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class Reminder:
    def __init__(self):
        self.c = Calendar()
        # http端口
        self.port = 4270
        self.httpd = None

    @staticmethod
    def yaml_load(yaml_path):
        # 通过yaml读取配置文件
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return yaml.load(f.read(), Loader=yaml.FullLoader)

    def add_event(self):

        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            logger.info('服务已关闭')
        # 通过http服务提供下载
        self.httpd = MyTCPServer(("", self.port), Handler)
        logger.info(f'服务已启动，端口：{self.port}')
        self.httpd.serve_forever()

    def memory_line(self, yaml_path):
        # 结果ics的名称
        ics_name = os.path.basename(yaml_path).split('.')[0] + '.ics'
        config = self.yaml_load(yaml_path)
        for task in config['tasks']:
            # 复习时间，半天、1天、3天、1周、2周、1月、3月、6月、1年
            time_gap = [12, 24, 72, 168, 336, 720, 2160, 4320, 8640]
            for gap in time_gap:
                e = Event()
                e.name = task['name']
                begin = datetime.strptime(task['begin'], "%Y-%m-%d")
                # 时间设置为22点
                begin = begin.replace(hour=22, minute=0, second=0)
                e.begin = begin + timedelta(hours=gap)
                e.begin = e.begin.replace(tzinfo=pytz.timezone('Asia/Shanghai'))

                e.duration = timedelta(hours=1)
                e.description = task['description'] if 'description' in task else ''
                alarm = DisplayAlarm(trigger=timedelta(minutes=0))
                e.alarms.append(alarm)
                self.c.events.add(e)

        with open(os.path.join(cur_path, 'result', ics_name), 'w') as f:
            f.writelines(self.c.serialize())


def main():
    r = Reminder()
    # 遍历conf目录下的所有yaml文件
    conf_path = os.path.join(cur_path, 'conf')
    for root, dirs, files in os.walk(conf_path):
        for file in files:
            if file.endswith('.yml'):
                r.memory_line(os.path.join(root, file))

    def restart_program():
        os.execl(sys.executable, sys.executable, *sys.argv)

    event_handler = FileChangeHandler(conf_path, restart_program)
    observer = Observer()
    observer.schedule(event_handler, path=conf_path, recursive=True)
    observer.start()

    try:
        r.add_event()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
