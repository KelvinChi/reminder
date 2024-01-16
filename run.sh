#!/usr/bin/env bash

curPath=$(cd "$(dirname "$0")" || exit; pwd)
# pip3安装依赖
echo "pip3 install -r requirements.txt ..."
sudo pip3 install -r "$curPath/requirements.txt"
# 把service文件放入到/etc/systemd/system/目录下
echo "copy reminder.service to /etc/systemd/system/ ..."
sudo cp "$curPath/reminder.service" /etc/systemd/system/
# 重新加载配置文件
echo "reload daemon ..."
sudo systemctl daemon-reload
# 启动服务
echo "start reminder.service ..."
sudo systemctl start reminder.service
# 设置开机启动
echo "enable reminder.service ..."
sudo systemctl enable reminder.service
# 查看服务状态
echo -e "reminder.service status ...\n\033[01;33mpress q to exit\033[0m"
sudo systemctl status reminder.service
