FROM python:3

# Docker metadata
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION
LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="youtubedl-auto" \
      org.label-schema.maintainer="tjw1184" \      
      org.label-schema.description="Preconfigured youtubedl-auto Server" \
      org.label-schema.url="https://github.com/tjw1184/youtubedl-auto" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/tjw1184/youtubedl-auto" \
      org.label-schema.vendor="tjw1184" \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0"

# setup paths 
RUN mkdir /youtubedl
RUN mkdir /youtubedl/downloads
RUN mkdir /youtubedl/configs
RUN mkdir /youtubedl/origconfigs
RUN mkdir /temp

## document ports and volumes to be remapped
VOLUME /youtubedl/downloads
VOLUME /youtubedl/configs

# setup default files
ADD runner.py /youtubedl
ADD youtube-dl-channels.txt /youtubedl/origconfigs
ADD youtube-dl-archive.txt /youtubedl/origconfigs
ADD youtube-dl.conf /youtubedl/origconfigs
ADD counter.txt /youtubedl/origconfigs

# Update packages and install ffmpeg.  
RUN apt-get update   
RUN apt-get install -y ffmpeg nano
RUN rm -rf /var/lib/apt/lists/*  

RUN pip install --upgrade pip
RUN pip install --upgrade youtube-dl

# Runs a sync once a day
CMD ["python", "/youtubedl/runner.py", "86400"]
#RUN /bin/bash
