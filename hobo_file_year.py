#! /usr/bin/env python
from __future__ import  print_function
"""
Determine the year for the current /home2/data/ONSET/
"""
import os
import pytz
# this works with tz aware datetimes, including utc
from datetime import datetime, timedelta
import dateutil.parser
import argparse
from hoboLinkInfo import hoboLinkGauges, hobo_url

##################################################
def hobo_file_year(dir, station, hourly):
  """
  checks for current year's csv and for the next year's csv and returns the full path name of the file to open.
  Return None if neither file exists.
  """

  cur_dt =  datetime.now(tz=pytz.utc)
  cur_yr =  str(cur_dt.year)
  fn = "{dir}{cur_yr}_{station}_{hourly}.csv".format(dir=dir, cur_yr=cur_yr, station=station, hourly=hourly)

  if os.path.exists(fn):
    return(fn)

  next_yr = str(cur_dt.year + 1)
  fn = "{dir}{next_yr}_{station}_{hourly}.csv".format(dir=dir, next_yr=next_yr, station=station, hourly=hourly)
  if os.path.exists(fn):
    return(fn)

  return(None)
##################################################


if __name__ == "__main__":

  out_dir = "/home2/data/ONSET/"
  valid_stations = list(sorted(hoboLinkGauges.keys()))

  ap = argparse.ArgumentParser()
  ap.add_argument("station_name", help="Hobolink Station Name: " + "|".join(valid_stations) )
  ap.add_argument("hourly", help="hourly|all. Fetch all 6 min values or just the hourly values, default.", nargs="*", default=['hourly'])
  ap.add_argument("-f", "--csv_file", help="CSV File. Use local file vs. Hobolink REST API.")
  ap.add_argument("-ih", "--inc_headers", help="Include headers in output file.", action="store_true")
  
  args = ap.parse_args()

  file_name = hobo_file_year(out_dir, args.station_name, args.hourly[0])
  print(file_name)

