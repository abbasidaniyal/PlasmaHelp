# Base Image
FROM python:3.7

# Set working dor
WORKDIR /code

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Dependencies
RUN apt-get update -y && \
    apt-get install --auto-remove -y \
      binutils \
      libproj-dev \
      gdal-bin \
      postgis \
      curl \
      locales \
      apt-transport-https && \
    rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

# Copy Project
COPY . /code

RUN chmod 700 /code/django_setup.sh
RUN /code/django_setup.sh
ENTRYPOINT ["uvicorn" ,"plasma_for_covid.asgi:application" ,"--host", "0.0.0.0","--port","8000","--reload"]
