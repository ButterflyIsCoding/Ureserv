FROM python:3

ENV PYTHONBUFFERD 1

ENV PYTHONDONTWRTEBYTECODE 1

RUN mkdir /app

WORKDIR /app

COPY . /app/

COPY entrypoint.sh /app/entrypoint.sh

RUN python3 -m pip3 install --upgrade pip3

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 4001

CMD ["gunicorn", "--bind", "0.0.0.0:4001", "ReserveProject.wsgi:application "]