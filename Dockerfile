FROM python:3

# Docker metadata
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION
LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="Bandersnatch" \
      org.label-schema.maintainer="tjw1184" \      
      org.label-schema.description="Preconfigured youtubedl auto Server" \
      org.label-schema.url="https://github.com/tjw1184/youtubedl-auto" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/tjw1184/youtubedl-auto" \
      org.label-schema.vendor="tjw1184" \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0"


## document ports and volumes to be remapped
VOLUME /youtubedl/downloads

# setup paths and default files
RUN mkdir /youtubedl
RUN mkdir /youtubedl/downloads
ADD youtube-dl-channels.txt /youtubedl
ADD youtube-dl-archive.txt /youtubedl
ADD youtube-dl.conf /youtubedl

# Update packages and install ffmpeg.  
RUN apt-get update   
RUN apt-get install -y libav-tools ffmpeg
RUN rm -rf /var/lib/apt/lists/*  

RUN pip install --upgrade pip
RUN pip install --upgrade youtube-dl

# Runs a sync once a day
#CMD ["python", "/src/runner.py", "3600"]
RUN /bin/bash
