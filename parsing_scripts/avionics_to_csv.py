import datetime
import re
import csv
import sys
from math import sqrt

INPUT_FILE = sys.argv[1]

#fields to convert to csv
field_list = ['delta', 'avionics', 'g_x', 'g_y', 'g_z', 'a_x', 'a_y', 'a_z', 'lat', 'long', 'agl', 'abs_elev', 'temp', 'time', 'gps_fix', 'gps_time']

p_time = 0
data_list = []

with open(INPUT_FILE, 'r') as f:
  for line in f: 
    s = line.rstrip()

    #check if first line of file
    if s == "starting log":
      continue

    #ensure all values are sane
    s = re.sub(' nan', ' 0', s)
    d = eval(s)

    for q in field_list:
      if not q in d:
        d[q] = 0

    if 'xbee_errors' in d:
      a = d.pop('xbee_errors')

    if (p_time == 0):
      #add delta field
      d['delta'] = 0
      p_time = d['time']
    else:
      delta = d['time'] - p_time
      d['delta'] = delta.total_seconds()
      p_time = d['time']

    d['abs_elev'] = d['agl'] + 1414

    data_list.append(d)

#write to a csv!
csv_name = INPUT_FILE + '.csv'
with open(csv_name, 'w') as csv_file:
  writer = csv.DictWriter(csv_file, fieldnames=field_list)
  writer.writeheader()
  writer.writerows(data_list)


#done!
