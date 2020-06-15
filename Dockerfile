# Base Image
FROM ubuntu:20.04

# Set working dor
RUN mkdir -p /code
WORKDIR /code

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Dependencies
COPY project/docker_scripts/install.sh .
RUN chmod 700 install.sh
RUN ./install.sh

# Python Dependencies
COPY project/requirements.txt /code/requirements.txt
RUN pip3 install -r requirements.txt


# Copy Project
COPY project/ /code

RUN chmod 700 /code/docker_scripts/start.sh

ENTRYPOINT ["/code/docker_scripts/start.sh"]
