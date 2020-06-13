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
        shutil.copyfile("/youtubedl/origconfigs/counter.txt","/configs/counter.txt") 
    
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
    
    print(f"Running youtubedl-auto every {intervalcounter}s", file=sys.stderr)
    while True:
        start_time = time.time()
        
        # if configs folder doesn't have config files then copy the defaults
        if not path.exists("/configs/youtube-dl.conf"):
            shutil.copyfile("/youtubedl/origconfigs/youtube-dl.conf","/configs/youtube-dl.conf")
        if not path.exists("/configs/youtube-dl-archive.txt"):
            shutil.copyfile("/youtubedl/origconfigs/youtube-dl-archive.txt","/configs/youtube-dl-archive.txt")
        if not path.exists("/configs/youtube-dl-channels.txt"):
            shutil.copyfile("/youtubedl/origconfigs/youtube-dl-channels.txt","/configs/youtube-dl-channels.txt")                     
               
        # make sure running latest youtube-dl
        run(["pip", "install", "--upgrade", "youtube-dl"])
        
        # run youtubedl every interval seconds
        run(["/usr/local/bin/youtube-dl", "--config-location", "/configs/youtube-dl.conf"])
        run_time = time.time() - start_time
        if run_time < intervalcounter:
            sleep_time = intervalcounter - run_time
            print(f"Ran for {run_time}s", file=sys.stderr)
            print(f"Sleeping for {sleep_time}s", file=sys.stderr)
            time.sleep(sleep_time)


if __name__ == "__main__":
    main()
