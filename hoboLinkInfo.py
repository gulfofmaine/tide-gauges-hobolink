#! /usr/bin/env python
from __future__ import  print_function
"""
  Onset Tide Gauge Information
  ===============================
  For all gauges data reported in elevation above MLLW (NAVD88) in feet.
  MSL  is Mean Sea Level used by the NECOFS water level forecasts in meters.
  MLLW is Mean Lower Low Water
  https://en.wikipedia.org/wiki/Chart_datum#Mean_Lower_Low_Water
  Conversion of data to MSL requires:
  MSL meters = (MLLW ft. * 0.3048) + GUAGE location correction.
     val_in_feet * 0.3048 = val_in_meters

  -  'scituate'
     At this location MSL is 1.491 meters above MLLW
     Benchmark used: Station ID: 8445138 - SCITUATE, SCITUATE HARBOR 
     MLLW_MSL = 1.491; # meters

  -  'hamptonbay'
     At this location MSL is 1.308 meters above MLLW
     Benchmark used: Station ID: 8440452   - PLUM ISLAND, MERRIMACK  RIVER ENTRANCE (with extrapolated estimate)
     MLLW_MSL = 1.308; # meters

    'gloucester'
    At this location MSL is 1.453 meters above MLLW
    Benchmark used: Station ID: 8441841 - GLOUCESTER HARBOR
    MLLW_MSL = 1.453; # meters
"""
hobo_url = "https://webservice.hobolink.com/restv2"
hoboLinkGauges = {
  'gloucester': {
    'name'   : 'Gloucester',
    'state'  : 'MA',
    'lat'    : '42.61025',
    'lon'    : '-70.6606',
    'user'   : 'mbwln',
    'pw'     : 'mbwln',
    'token'  : '3ENiSHKex4',
    'sn'     : '10889646',
    'pre_sn' : '10064451',
    'path'   : '/data/custom/file',
    'query'  : 'neracoos_last_4_hrs',
    'mllw_msl' : 1.453,
    'status ': 'active'
  },
  'hamptonbay' : {
    'name'  : 'Hampton Harbor',
    'state' : 'MA',
    'lat'   : '42.90010',
    'lon'   : '-70.8185',
    'user'  : 'hamptonbay',
    'pw'    : 'hamptonbay',
    'token' : '3ENiSHKex4',
    'sn'     : '10984905',
    'pre_sn' : '9829890',
    'path'  : '/data/custom/file',
    'query'  : 'neracoos_last_4_hrs',
    'mllw_msl' : 1.308,
    'status': 'active'
   },
  'scituate': {
    'name'  : 'Scituate Harbor',
    'state' : 'MA',
    'lat'   : '42.19945',
    'lon'   : '-70.72009',
    'user'  : 'noaa',
    'pw'    : 'noaa.08',
    'token' : '3ENiSHKex4',
    'sn'     : '',
    'pre_sn' : '',
    'path'  : '/data/custom/file',
    'query'  : 'neracoos_last_4_hrs',
    'mllw_msl' : 1.491,
    'status': 'inactive'
  }
}

if __name__ == "__main__":

  for k,v in sorted(hoboLinkGauges.items()):
    print(k, v['name'], v['sn'], v['lat'], v['lon'], v['state'], v['user'], v['pw'], v['mllw_msl'])

  station_info = hoboLinkGauges['scituate']
  # Hobolink custom data POST request.
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

  print("hobo_path: ", station_info["path"])
  print(json_str)


