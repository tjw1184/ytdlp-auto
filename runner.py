#!/usr/bin/env python3

# Simple Script to replace cron for Docker

import argparse
import os
import sys
import time
import shutil
from subprocess import run
from os import path


def main() -> None:
    
    # if no counter file copy the default
    if not path.exists("/configs/counter.txt"):
        shutil.copyfile("/ytdlp/origconfigs/counter.txt","/configs/counter.txt") 
    
    # interval counter, default to 1 week 1 second (should be overrode by counter.txt)
    intervalcounter = float(604801.0)
    
    # try to read counter file
    try:
        infile = open("/configs/counter.txt","r")
        line = infile.readline()
        test=float(line)
        # minimum interval time of 1 hour
        if test >= 3600:
            intervalcounter=test
    except:
        print("bad counter.txt file")
    
    print(f"Running ytdlp-auto every {intervalcounter}s", file=sys.stderr)
    while True:
        start_time = time.time()
        
        # if configs folder doesn't have config files then copy the defaults
        if not path.exists("/configs/ytdlp.conf"):
            shutil.copyfile("/ytdlp/origconfigs/ytdlp.conf","/configs/ytdlp.conf")
        if not path.exists("/configs/ytdlp-archive.txt"):
            shutil.copyfile("/ytdlp/origconfigs/ytdlp-archive.txt","/configs/ytdlp-archive.txt")
        if not path.exists("/configs/ytdlp-channels.txt"):
            shutil.copyfile("/ytdlp/origconfigs/ytdlp-channels.txt","/configs/ytdlp-channels.txt")                     
               
        # make sure running latest youtube-dl
        run(["pip", "install", "--upgrade", "pip"])      
        run(["pip", "install", "--upgrade", "yt-dlp"])
        run(["pip", "install", "--upgrade", "pycryptodomex"])
        run(["pip", "install", "--upgrade", "websockets"])

        
        # run youtubedl every interval seconds
        run(["/usr/local/bin/yt-dlp", "--config-location", "/configs/ytdlp.conf"])
        run_time = time.time() - start_time
        if run_time < intervalcounter:
            sleep_time = intervalcounter - run_time
            print(f"Ran for {run_time}s", file=sys.stderr)
            print(f"Sleeping for {sleep_time}s", file=sys.stderr)
            time.sleep(sleep_time)


if __name__ == "__main__":
    main()
