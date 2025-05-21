FROM python:3.13-alpine

LABEL name="linux-monitor"
LABEL maintainer="schnitz81"
LABEL description="Monitoring tool for Linux systems that generates graphs and web pages dynamically."
LABEL url="https://github.com/schnitz81/linux-monitor"

RUN apk update --no-cache \
&& apk add --no-cache bash coreutils curl grep gcc gfortran build-base zlib zlib-dev jpeg libjpeg jpeg-dev freetype-dev \
    lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev tzdata font-opensans cairo-dev cairo-gobject \
    py3-gobject3-dev gobject-introspection-dev \
&& ls /usr/share/zoneinfo && cp /usr/share/zoneinfo/Europe/Stockholm /etc/localtime && echo "Europe/Stockholm" > /etc/timezone \
&& mkdir /backups \
&& mkdir /linux-monitor \
&& mkdir -p /linux-monitor/static

ADD *.py *.txt clients.conf /linux-monitor/
ADD static/* /linux-monitor/static/

WORKDIR /linux-monitor
RUN pip install -U pip \
&& pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python","-u","main.py"]

# build:
# docker build . -t linux-monitor

# run:
# docker run --name linux-monitor --cpus=".15" --restart unless-stopped -d -v /run:/run -v $PWD/backups:/backups -v $PWD/clients.conf:/linux-monitor/clients.conf linux-monitor
