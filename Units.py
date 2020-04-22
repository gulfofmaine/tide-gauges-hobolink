#! /usr/bin/env python
"""GMRI Common Unit conversions."""

SCALE_POUNDS_TO_KILOS  = 0.4536
compass = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']

def conv_celsius_to_fahrenheit(in_put):
  return ( (in_put * 1.8 ) + 32.0 )

def conv_fahrenheit_to_celsius(in_put):
  return ( (in_put - 32.0 ) / 1.8)

def conv_fathoms_to_meters(in_put):
  return ( in_put * 1.8288 )

def conv_meters_to_fathoms(in_put):
  return ( (in_put / 1.8288) )

def conv_meters_to_feet(in_put):
  return ( (in_put / 0.3048) )

def conv_feet_to_meters(in_put):
  return ( (in_put * 0.3048) )

def conv_meters_to_miles(in_put):
  return ( (in_put / 1609.344) )

def conv_meters_to_nautical_miles(in_put):
  return ( (in_put / 1853.184) )

def conv_mps_to_knots(in_put):
  """ convert meters per second to knots """
  return ( (in_put / 0.5144444) )

def conv_mps_to_mph(in_put):
  """ convert meters per second to miles per hour """
  return ( (in_put / 0.2777778) )

def conv_mph_to_knots(in_put):
  return ( (in_put / 0.44704) * 0.5144444 )

def conv_knots_to_mph(in_put):
  return ( (in_put / 0.5144444 ) * 0.44704 )

def conv_radians_to_degrees(in_put):
  return ( in_put * ( 180 / 3.14159) )

def conv_uM_to_mlL(in_put):
  """ microMoles to milliliter per Liter
  For the UNH Great Bay buoy dissolved_oxygen which reports microMoles uM
  """
  return ( in_put  / 44.6596 )

def conv_degrees_to_compass(degrees):
  """ convert degrees to 16 compass direction strings. 0 and 360 degree are 'N'
  """
  degrees = ( degrees + 22.5 ) / 22.5
  degrees -= .5
  # Note: Units.pm relied on integer truncation
  quad = int(degrees % 16)
  return compass[quad]

if __name__ == '__main__':
    res = conv_degrees_to_compass(45.0)
    print(res)
    res = conv_mph_to_knots(5.0)
    print(res)
    res2 = conv_knots_to_mph(res)
    print(res2)
    assert(res2 == 5.0)
    res = conv_meters_to_feet(1.0)
    print(res)
    res = conv_feet_to_meters(3.0)
    print(res)
    res = conv_feet_to_meters(3)
    # need round() on all these
    print(res)

