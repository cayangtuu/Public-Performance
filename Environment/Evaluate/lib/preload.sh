#!/bin/sh
# Script to preload ESMF dynamic trace library
env LD_PRELOAD="$LD_PRELOAD /home/cayang/anaconda3/envs/Evaluate/lib/libesmftrace_preload.so" $*
