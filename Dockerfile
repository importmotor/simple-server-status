# maintainer info
FROM python:3.12-slim-bullseye
LABEL maintainer="carrergt@gmail.com"

WORKDIR /
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
WORKDIR /app

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]
