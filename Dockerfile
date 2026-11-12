FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./test.py /code/
COPY ./01_第一个AI程序_学习笔记.md /code/

CMD ["fastapi", "run", "test.py", "--port", "80"]
