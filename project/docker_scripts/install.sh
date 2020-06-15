#!/bin/sh



apt-get update
apt-get upgrade -y
apt-get install -y  postgis python3 python3-pip gdal-bin postgresql-client -qq --no-install-recommends