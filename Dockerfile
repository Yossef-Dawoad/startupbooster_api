

# First stage: build the app
FROM python:latest as builder
ENV PYTHONUNBUFFERED=1
WORKDIR /api
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --target=/api --no-cache-dir

# Second stage: copy the app and run it
FROM python:slim
WORKDIR /api
COPY --from=builder /api /api/
COPY api /api
EXPOSE 8000
