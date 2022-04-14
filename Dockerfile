FROM python:3.9-alpine

RUN mkdir -p /usr/modifier-server
WORKDIR /usr/modifier-server

COPY requirements.txt /usr/modifier-server/requirements.txt

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /usr/modifier-server

EXPOSE 7002

CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]