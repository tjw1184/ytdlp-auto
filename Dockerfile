FROM python:3

# Docker metadata
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION
LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="ytdlp-auto" \
      org.label-schema.maintainer="tjw1184" \      
      org.label-schema.description="Preconfigured ytdlp-auto Server" \
      org.label-schema.url="https://github.com/tjw1184/ytdlp-auto" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/tjw1184/ytdlp-auto" \
      org.label-schema.vendor="tjw1184" \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0"

# setup paths 
RUN mkdir /youtubedl
RUN mkdir /downloads
RUN mkdir /configs
RUN mkdir /youtubedl/origconfigs
RUN mkdir /temp

## document ports and volumes to be remapped
VOLUME /downloads
VOLUME /configs

# setup default files
ADD runner.py /youtubedl
ADD youtube-dl-channels.txt /youtubedl/origconfigs
ADD youtube-dl-archive.txt /youtubedl/origconfigs
ADD youtube-dl.conf /youtubedl/origconfigs
ADD counter.txt /youtubedl/origconfigs

# Update packages and install ffmpeg.  
RUN apt-get update   
RUN apt-get install -y ffmpeg nano python3-mutagen
RUN rm -rf /var/lib/apt/lists/*  

RUN pip install --upgrade pip
RUN pip install --upgrade pycrypto
RUN pip install --upgrade pycryptodomex
RUN pip install --upgrade websockets
RUN pip install --upgrade ffprobe
RUN pip install --upgrade ffprobe3
RUN pip install --upgrade yt-dlp 

# Runs a sync on interval
CMD ["python", "/youtubedl/runner.py"]
#RUN /bin/bash
