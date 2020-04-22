# ONSET Hobolink RestAPI V2 Tide Guage Access
## Hamptonbay, Gloucester and Scituate MA Stations.


## Summary

##  Info Links
  - hobolink.com 
  - https://webservice.hobolink.com/restv2/

## Requirements 
  - python=2.7 or 3.7

## Approach

## Directories and Files
  - `/home2/data/ONSET/2020`
    - `hamptonbay_hourly.csv`
    - `gloucester.csv`
    - `scituate.csv`

##  Usage
__`hobo_fetch.py`__  
```
usage: hobo_fetch.py [-h] [-od OUT_DIR] [-f CSV_FILE] [-q QUERY] [-ih] [-v]
                     [-t]
                     station_name [hourly [hourly ...]]

positional arguments:
  station_name          Hobolink Station Name: gloucester|hamptonbay|scituate
  hourly                hourly|all. Fetch all 6 min values or just the hourly
                        values, default.

optional arguments:
  -h, --help            show this help message and exit
  -od OUT_DIR, --out_dir OUT_DIR
                        Where to create/update the station csv file. Default
                        is /home2/data/ONSET/2020/
  -f CSV_FILE, --csv_file CSV_FILE
                        CSV File. Use local file vs. Hobolink REST API.
  -q QUERY, --query QUERY
                        Query name. Created in hobolink.com.
  -ih, --inc_headers    Include headers in output file.
  -v, --verbose         Verbose.
  -t, --test            test_mode.
```

## First time usage example.

## [Tools Documentation](docs/hobolink_tools.md)
