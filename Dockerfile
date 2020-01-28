FROM python:3.6

MAINTAINER maicius
WORKDIR /ncov_robot
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak

RUN echo "deb http://mirrors.ustc.edu.cn/ubuntu/ trusty main restricted universe multiverse\n\
deb http://mirrors.ustc.edu.cn/ubuntu/ trusty-security main restricted universe multiverse\n\
deb http://mirrors.ustc.edu.cn/ubuntu/ trusty-updates main restricted universe multiverse\n\
deb http://mirrors.ustc.edu.cn/ubuntu/ trusty-proposed main restricted universe multiverse\n\
deb http://mirrors.ustc.edu.cn/ubuntu/ trusty-backports main restricted universe multiverse\n\
deb-src http://mirrors.ustc.edu.cn/ubuntu/ trusty main restricted universe multiverse\n\
deb-src http://mirrors.ustc.edu.cn/ubuntu/ trusty-security main restricted universe multiverse\n\
deb-src http://mirrors.ustc.edu.cn/ubuntu/ trusty-updates main restricted universe multiverse\n\
deb-src http://mirrors.ustc.edu.cn/ubuntu/ trusty-proposed main restricted universe multiverse\n\
deb-src http://mirrors.ustc.edu.cn/ubuntu/ trusty-backports main restricted universe multiverse\n\
" > /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 40976EAF437D05B5
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32
RUN apt-get update --allow-unauthenticated
RUN apt-get -q -y --force-yes install libleptonica-dev
RUN apt-get -q -y --force-yes install libtesseract3 libtesseract-dev
RUN apt-get -q -y --force-yes install tesseract-ocr
RUN apt-get -q -y --force-yes install tesseract-ocr-eng tesseract-ocr-ara tesseract-ocr-bel tesseract-ocr-ben tesseract-ocr-bul tesseract-ocr-ces tesseract-ocr-dan tesseract-ocr-deu tesseract-ocr-ell tesseract-ocr-fin tesseract-ocr-fra tesseract-ocr-heb tesseract-ocr-hin tesseract-ocr-ind tesseract-ocr-isl tesseract-ocr-ita tesseract-ocr-jpn tesseract-ocr-kor tesseract-ocr-nld tesseract-ocr-nor tesseract-ocr-pol tesseract-ocr-por tesseract-ocr-ron tesseract-ocr-rus tesseract-ocr-spa tesseract-ocr-swe tesseract-ocr-tha tesseract-ocr-tur tesseract-ocr-ukr tesseract-ocr-vie tesseract-ocr-chi-sim tesseract-ocr-chi-tra
RUN apt-get -q -y --force-yes install gcc
RUN mkdir -p /usr/local/share/tessdata/
RUN cp -R /usr/share/tesseract-ocr/tessdata/* /usr/local/share/tessdata/
COPY chi_sim.traineddata /usr/local/share/tessdata/

COPY requirements.txt /ncov_robot
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
COPY . /ncov_robot
CMD python src/robot/NcovWeRobotServer.py
