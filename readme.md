# 记忆曲线ICS生成器
## 1. 介绍
### 1.1 项目背景
基于艾宾浩斯曲线生成复习时间日程表，帮助用户更好的复习。
### 1.2 项目使用
通过配置yml文件，自动生成复习日程表。通过run.sh一键配置，需要安装python3.7及以上版本，
需要sudo权限（配置systemd服务，可不使用），需要配置好pip3环境。
#### 使用方法一
```shell
vim conf/your_ics.yml
/bin/bash run.sh
```
#### 使用方法二
```shell
vim conf/your_ics.yml
pip3 install -r requirements.txt
python3 main.py
```
## 2. 项目结构
```
├── conf
│   ├── ics.yml
│   └── readme.md
├── main.py
├── README.md
├── requirements.txt
├── run.sh
```

## 3. 项目配置
### 3.1 项目配置文件
```yaml
# 项目配置文件
tasks:
  # 日程名
  - name: "测试一"
    # 学习完成时间
    begin: "2024-01-15"
    # 日程备注，可选
    description: "测试一"

  - name: "测试二"
    begin: "2024-01-17"
```
## 4. 日历配置
项目会创建一个http服务，需要手机能够正确访问到，链接为http://ip:4270/your_ics.ics。
以小米手机为例，打开日历 -> 设置 -> 日程导入 -> URL导入 -> 输入链接 -> 添加。

更新策略：打开日历 -> 设置 -> 账号管理 -> 订阅日历 -> 立即同步/设置同步频率。
