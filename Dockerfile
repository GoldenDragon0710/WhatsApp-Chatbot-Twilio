# base image
FROM python:3.10.0-alpine3.14

# set the working directory
WORKDIR /app

# copy the application files
COPY app.py requirements.txt ./

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose the port your application will listen on
EXPOSE 5000

# set environment variables
ENV FLASK_APP=app.py

# start the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]