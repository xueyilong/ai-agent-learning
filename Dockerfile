FROM python:3.12
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY ./13_画stategraph图.py /code/
COPY ./*.md /code/
CMD ["fastapi", "run", "13_画stategraph图.py", "--port", "80"]

