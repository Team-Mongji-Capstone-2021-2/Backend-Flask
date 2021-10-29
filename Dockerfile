FROM python:3.9
MAINTAINER boyung <boyung1021@gmail.com>

USER root
WORKDIR /root

# bse
RUN apt-get -y update
RUN apt-get -y install python3-pip

# flask
RUN git clone https://github.com/Team-Mongji-Capstone-2021-2/Backend-Flask.git
WORKDIR /root/flask
RUN pip install virtualenv
RUN virtualenv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt

CMD python manage.py runserver

EXPOSE 80