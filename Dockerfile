FROM python:3.6

MAINTAINER maicius
WORKDIR /ncov_robot
COPY requirements.txt /ncov_robot
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
COPY . /ncov_robot
CMD python src/robot/NcovWeRobotServer.py
