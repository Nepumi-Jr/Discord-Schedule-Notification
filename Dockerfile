FROM python:3.8-alpine3.14

WORKDIR /usr/src/app

COPY required.txt ./
RUN pip install --no-cache-dir -r required.txt

COPY . .

CMD [ "python", "-u", "./main.py" ]