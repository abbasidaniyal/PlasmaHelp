FROM python:3.7

ENV PYTHONUNBUFFERED 1

# Update and install packages recomended by Django documentation:
# https://docs.djangoproject.com/ja/1.9/ref/contrib/gis/install/geolibs/
# and extra needed packages
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


WORKDIR /code
COPY . /code


RUN pip install -r requirements.txt
