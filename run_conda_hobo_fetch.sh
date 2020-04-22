#!/bin/bash
# Activate conda oisst virtual environment
# This depends on where conda has been installed. Here assuming $HOME and where oisst-clim-daily has been installed.
# Laptop
#source $HOME/miniconda2/bin/activate
# AWS
#source $HOME/miniconda2/bin/activate

# Docker1
# On Docker1 not need to activate.  It's in the admin crontab
# PATH=/home2/miniconda2/bin:/usr/sbin:/usr/local/bin:/usr/bin:/bin
# system-wide install.
#source /home2/miniconda2/bin/activate

# activate the env we want
#conda activate py37

#$HOME/work/Onset/hobo_fetch.py hamptonbay hourly -v
/home2/python/tide-gauges-hobolink/hobo_fetch.py hamptonbay hourly -v
sleep 10
echo "####################"

#$HOME/work/Onset/hobo_fetch.py gloucester hourly -v
/home2/python/tide-gauges-hobolink/hobo_fetch.py gloucester hourly -v
echo "####################"

sleep 10
#$HOME/work/Onset/hobo_fetch.py scituate hourly -v
/home2/python/tide-gauges-hobolink/hobo_fetch.py scituate hourly -v
echo "####################"

