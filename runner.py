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
    #parser = argparse.ArgumentParser()
    #parser.add_argument("interval", type=float, help="Time in seconds between jobs")
    #args = parser.parse_args()
    
    # interval counter, default to 1 week 1 second (should be overrode by counter.txt)
    intervalcounter = float(604801.0)
    
    # try to read counter file
    try:
        infile = open("/youtubedl/configs/counter.txt","r")
        line = infile.readline()
        test=float(line)
        # minimum run time of 1 hour
        if test >= 3600:
            intervalcounter=test
    except:
        print("bad counter.txt file")
    
    print(f"Running youtubedl-auto every {intervalcounter}s", file=sys.stderr)
    while True:
        start_time = time.time()
        
        # if configs folder doesn't have config files then copy the defaults
        if path.exists("/youtubedl/configs/youtube-dl.conf") not True:
            shutil.copyfile("/youtubedl/origconfigs/youtube-dl.conf","/youtubedl/configs/youtube-dl.conf")
        if path.exists("/youtubedl/configs/youtube-dl-archive.txt") not True:
            shutil.copyfile("/youtubedl/origconfigs/youtube-dl-archive.txt","/youtubedl/configs/youtube-dl-archive.txt")
        if path.exists("/youtubedl/configs/youtube-dl-channels.txt") not True:
            shutil.copyfile("/youtubedl/origconfigs/youtube-dl-channels.txt","/youtubedl/configs/youtube-dl-channels.txt")            
        if path.exists("/youtubedl/configs/counter.txt") not True:
            shutil.copyfile("/youtubedl/origconfigs/counter.txt","/youtubedl/configs/counter.txt")          
        
        # Dirty hack to implement the 429 error workaround provided by colethedj, lock to 2-16-20 branch for now
        # https://gitlab.com/colethedj/youtube-dl-429-patch
        prevdir = os.getcwd()
        os.chdir("/temp")
        run(["/usr/bin/git","clone","https://github.com/ytdl-org/youtube-dl.git","-b","2020.02.16","--depth","1"])
        run(["/usr/bin/git","clone","https://gitlab.com/colethedj/youtube-dl-429-patch.git"])
        os.chdir("/temp/youtube-dl/youtube_dl")
        run(["/usr/bin/git","apply","../../youtube-dl-429-patch/youtube.py.patch"])
        os.chdir("/temp/youtube-dl")
        run(["/usr/local/bin/pip3","install","."])
        os.chdir(prevdir)
        
        # re-enable when hack no longer needed
        #run(["pip", "install", "--upgrade", "youtube-dl"])
        run(["/usr/local/bin/youtube-dl", "--config-location", "/youtubedl/configs/youtube-dl.conf"])
        run_time = time.time() - start_time
        if run_time < intervalcounter:
            sleep_time = intervalcounter - run_time
            print(f"Ran for {run_time}s", file=sys.stderr)
            print(f"Sleeping for {sleep_time}s", file=sys.stderr)
            time.sleep(sleep_time)


if __name__ == "__main__":
    main()
