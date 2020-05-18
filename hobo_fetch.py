#! /usr/bin/env python
from __future__ import  print_function
import sys
import requests
import csv
from datetime import datetime
import argparse
import Units as Units

from hoboLinkInfo import hoboLinkGauges, hobo_url
from hobo_file_year import hobo_file_year

############################################
def fix_time(time_in, hourly=False):
  [date, time] = time_in.split()
  #print(date)
  #print(time)
  [mo, dy, yr] = [int(x) for x in date.split('/')]
  yr = yr + 2000
  [hr, min, sec] = [int(x) for x in time.split(':')]
  # to only get hourly values.
  if hourly and min != 0:
    return None    
  dt = datetime( yr, mo, dy, hr, min )
  return dt
########################## run stand-alone ##################
def fetch_hobo_csv(station, query=None, verbose=False, test_mode=False):
  station_info = hoboLinkGauges[station]
  hobo_path = station_info["path"]
  # So we are passing station_info dict so if query we want to override the station_info[query]
  if query:
    station_info['query'] = query
  if verbose:
    print(station_info['query'])
    print(station_info['user'])

  # working only on hoboware queries, UTC, w/o battery
  json_str = """\
  {{
    "authentication": {{
      "password": "{pw}",
      "token": "{token}",
      "user": "{user}"
    }},
    "query": "{query}"
  }}\
  """.format(**station_info)
  
  headers = {'Content-Type' : 'application/json'}
  
  this_url = hobo_url + hobo_path
  if verbose:
    print(this_url)
    #print(json_str)
  
  title = station + "_" + station_info["user"] + "_" + station_info["query"] + ".csv"
  req = requests.post(this_url, headers=headers,  data=json_str)
  if req.status_code != requests.codes.ok:
    print(req.status_code, file=sys.stderr)
    print("ERROR. Could not fetch: ", req.url, station_info["query"], file=sys.stderr)
    return(req.text, False)
  # HERE to get raw results for tests.
  # quick tests.
  #print(req.content)
  # O.K. This is what we want. the end="" removes the last empty line.
  #print(req.text, end="")
  #print(req.text)
  #exit()

  if verbose: print("Fetched: ", title)
  
  return(req.text, True)
#########################################  
def hobo_strip_hw(res_text, verbose=False, test=False ):
  """
    remove the hoboware CSV headers which end with 
    '------------'
    removes blank lines
    from the requests.text response. A string.
    Also handles files which don't have the hoboware headers.
  """
  lines = [line for line in res_text.split('\n') if line.strip() != '']
  try:
    idx = lines.index("------------")
  except ValueError:
    idx = -1

  return(lines[idx+1:])

#########################################  
def hobo_strip_hw_file(csv_file, verbose=False, test=False ):
  """
    remove the hoboware CSV headers which end with 
    '------------'
    removes blank lines
    from a local file.
    Also handles files which don't have the hoboware headers.
  """
  lines = [line for line in csv_file.readlines() if line.strip() != '']
  try:
    idx = lines.index("------------\n")
  except ValueError:
    idx = -1
  return(lines[idx+1:])
#########################################  
def hobo_strip_dt(res_list, dt_filter="", verbose=False, test=False ):
  """
    res_list: a list of lists. Need to loop.
    dt_filer:  iso time string  YYYY-MM-DDTHH:MM:SS
    Search for the dt_filter iso string. Delete all lines prior to and including the dt_filter value
  """
  idx = -1
  for i, sl in enumerate(res_list):
    if dt_filter in sl:
      #print("Found", i, dt_filter)
      idx = i

  return(res_list[idx+1:])

#########################################  
def hobo_fix_csv(station_name, res_text, hourly='hourly', dt_filter="", verbose=False ):
  station_info = hoboLinkGauges[station_name]
  lat = station_info["lat"]
  lon = station_info["lon"]
  station_desc = station_info["name"]
  # convert MLLW_meter to MSL
  mllw_msl = station_info["mllw_msl"]
  # this is for the time filter
  all_rows = []

  # scituate station flag. Only MLLW is in CSV, not Temp
  sci_flag = (station_name == 'scituate') or False

  reader = csv.reader(res_text)
  for csv_row in reader:
    # skip the headers
    if csv_row[0] == 'Line#' or csv_row[0] == '#':
      continue

    # skip rows with no temp or water level values
    # Scituate only has MLLW, csv_row[2] but no Temp value.
    # Other have Temp inr csv_row[2]
    if not  csv_row[2]:
      continue
    # for Hampton and Gloucester check for MLLW value, csv_row[3]
    if not sci_flag and not csv_row[3]:
      continue

    time_str = csv_row[1]
    if hourly == 'hourly':
      dt = fix_time(time_str, hourly=True)
      if not dt:
        continue
    else:
      dt = fix_time(time_str)

    this_row = []
    this_row.append(station_desc)
    this_row.append(lat)
    this_row.append(lon)
    this_row.append(dt.isoformat())
    # MLLW for scituate, Temp and MLLW for others
    if sci_flag:
      this_row.append(csv_row[2])
      meter_val = Units.conv_feet_to_meters(float(csv_row[2]))
    else:
      this_row.append(csv_row[2])
      this_row.append(csv_row[3])
      meter_val = Units.conv_feet_to_meters(float(csv_row[3]))

    msl_val  = meter_val + float(mllw_msl)
    this_row.append(meter_val)
    this_row.append(msl_val)
    all_rows.append(this_row)

  if dt_filter:
    all_rows = hobo_strip_dt(all_rows, dt_filter=dt_filter)
  return(all_rows)
#########################################  

#########################################  
if __name__ == "__main__":
  # Gloucester queries Note: 20 fields
  #query = 'neracoos_hoboware_test'
  # HamptonBay queries Note: 19 fields.
  #query = 'neracoos_last2hours_hw'  # hoboware CSV

  # HERE
  out_dir = "/home2/data/ONSET/"

  valid_stations = list(sorted(hoboLinkGauges.keys()))
  ap = argparse.ArgumentParser()
  ap.add_argument("station_name", help="Hobolink Station Name: " + "|".join(valid_stations) )
  ap.add_argument("hourly", help="hourly|all. Fetch all 6 min values or just the hourly values, default.", nargs="*", default=['hourly'])
  ap.add_argument("-od", "--out_dir", help="Where to create/update the station csv file. Default is /home2/data/ONSET/2020/")
  ap.add_argument("-f", "--csv_file", help="CSV File. Use local file vs. Hobolink REST API.")
  ap.add_argument("-q", "--query", help="Query name. Created in hobolink.com.", default=None)
  ap.add_argument("-ih", "--inc_headers", help="Include headers in output file.", action="store_true")
  ap.add_argument("-v", "--verbose", help=" Verbose.", action="store_true")
  ap.add_argument("-t", "--test", help=" test_mode.", action="store_true")

  args = ap.parse_args()

  if args.hourly[0] not in ['hourly', 'all']:
    print("Invalid hourly value: ", args.hourly[0])
    exit()

  if args.station_name not in valid_stations:
    print("Invalid station: ", args.station_name)
    exit()

  if args.out_dir:
    out_dir = args.out_dir
    if not out_dir.endswith('/'): 
      out_dir += '/'
          
  if args.verbose:
    print("station_name:", args.station_name)
    print("hourly:", args.hourly[0])
    print("inc_headers:", args.inc_headers)


  station_info = hoboLinkGauges[args.station_name]
  status = False
  res_strip_hw = []

  # HERE 
  #out_file = out_dir +  args.station_name + "_" + args.hourly[0] + ".csv"
  # confirms year file exists.
  # None means a brand new file. Still needs work.
  out_file = hobo_file_year(out_dir, args.station_name, args.hourly[0])
  if not out_file:
    print("File: '{0}' does not exists. New year file must be created.".format(out_file), file=sys.stderr)
    print("Exiting!")
    exit()

  if args.verbose: print(out_file, args.query )

  if args.csv_file:
    try:
      f = open(args.csv_file, 'r')
      res_strip_hw = hobo_strip_hw_file(f)
      f.close()
      if(len(res_strip_hw) != 0):
        status = True
    except IOError:
      print("File: '{0}' does not exists.".format(args.csv_file), file=sys.stderr)
  else:
    res_text, status = fetch_hobo_csv(args.station_name, query=args.query, verbose=args.verbose, test_mode=args.test)
    if status:
      res_strip_hw = hobo_strip_hw(res_text)
      #for l in res_strip_hw:
      #  print(l)

  # Open writer
  try:
    w = open(out_file, 'a+')
    #w = open(out_file, 'w', newline="")
    status = True
  except IOError:
    print("Could not create csv: '{0}'.".format(args.station_name + ".csv"), file=sys.stderr)

  # something went wrong.
  if not status:
     exit()

  # Get the last date in the out_file
  #Hampton Harbor,42.90010,-70.8185,2020-03-10T20:00:00,6.26,5.0016,1.52448768,2.83248768
  # So first time thru the lines[-1], no lines created yet. so no dt_filter
  dt_filter = ''
  w.seek(0)
  lines = w.readlines()
  if len(lines):
    last_row = lines[-1]
    dt_filter = last_row.split(",")[3]
    if args.verbose: print(dt_filter)
  # HERE
  # Need to check the query for <station>_after_2020-01-01
  # To update the after_2020 file

  if args.station_name == 'scituate':
    csv_headers = ['Station', 'Latitude', 'Longitude', 'Time', 'MLLW_feet', 'MLLW_meter', 'MSL']
  else:
    csv_headers = ['Station', 'Latitude', 'Longitude', 'Time', 'Temp', 'MLLW_feet', 'MLLW_meter', 'MSL']

  writer = csv.writer(w)
  if args.inc_headers:
    writer.writerow(csv_headers)


  new_res = hobo_fix_csv(args.station_name, res_strip_hw, hourly=args.hourly[0], dt_filter=dt_filter)

  for this_row in new_res:
    assert( len(csv_headers) == len(this_row))
    writer.writerow(this_row)
  w.close()

  if args.verbose:
    print("Update:", out_file)
