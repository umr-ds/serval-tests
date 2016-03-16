#!/usr/bin/env python

import hashlib, socket, time, argparse, signal, sys, random
from Helpers import *

parser = argparse.ArgumentParser(description='Periodically generate and add directed files into the serval rhizome store.')
parser.add_argument('-d', dest='min_delay_ms', default=0, help='set minimum insertion delay (ms)')
parser.add_argument('-j', dest='delay_jitter_ms', default=1000, help='set maximum jitter (ms) for insertion delay')
parser.add_argument('-s', dest='size_k', default=1024, help='size (KiB) of files to be inserted')
args = parser.parse_args()

# adding parsed /default values to global dict 
globals().update(vars(args))
random.seed(socket.gethostname())
my_sid = getSid()
neighbours = getNeightbourSids()

if __name__ == "__main__":
    count = 0
    running = True
    def signal_handler(signal, frame): print("Received SIGINT, stopping..."); sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    basename = socket.gethostname()
    if len(neighbours) == 0: print("No neighbours found, exiting"); sys.exit(1)
    while running:
        their_sid = random.choice(neighbours)
        rhizomeRandomFile(basename+"-"+str(size_k)+"k-"+str(count)+".bin", size_k, my_sid, their_sid=their_sid)
        count += 1
        insertion_delay_ms = min_delay_ms + random.randint(0, delay_jitter_ms)
        print("Inserted files to "+their_sid+", sleeping for "+str(insertion_delay_ms)+"ms")
        time.sleep(float(insertion_delay_ms)/100)