# syntax=docker/dockerfile:1
# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY devrequirements.txt /code/
RUN pip install -r devrequirements.txt

# Copy project
COPY . /code/

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
