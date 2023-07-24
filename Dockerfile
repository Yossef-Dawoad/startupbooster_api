# First stage: build the app
FROM python:latest as builder
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.prod.txt requirements.txt

# Use an ARG to define the OS
ARG os
# Use a shell script to run different commands for pip install based on the OS
RUN if [ \"$os\" = \"windows\" ]; then python.exe -m pip install --upgrade pip; else pip3 install --upgrade pip; fi

# RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --target=/app --no-cache-dir

# Second stage: copy the app and run it
FROM python:slim
WORKDIR /app
#copy from builder to the slim version
COPY --from=builder /app /app/
# copy the application to the /app directory
COPY ./api /app
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
