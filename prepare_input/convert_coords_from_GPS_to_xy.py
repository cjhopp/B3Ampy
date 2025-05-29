'''
Convert list of GPS coordinates to xy coordinates (in m UTM) and save in correct file format for B3Ampy
---
Claudia Finger
claudia.finger@ieg.fraunhofer.de
2023-04-21
'''
import utm

import numpy as np
from datetime import datetime
from obspy import read_inventory

def convert_latlon_to_utm(filename, outfile):
    inventory = read_inventory(filename)
    latlon = np.array([(sta.code, sta.latitude, sta.longitude) for sta in inventory[0].stations]).T

    # convert to UTM coordinates ###
    utm_east, utm_north, utm_zone, utm_letter = utm.from_latlon(latlon[:, 0], latlon[:, 1])

    # convert to relative to reference station (use mean as reference) ###
    station_x = utm_east - np.mean(utm_east)
    station_y = utm_north - np.mean(utm_north)
    np.savetxt(outfile, np.hstack([latlon[:, 0], station_x, station_y]), fmt='%s,%.8s,%.8s',
               delimiter=',', header='station name, x (m), y (m)')
    return
