import datetime
import re
import csv
import sys
from dateutil import parser

INPUT_FILE = sys.argv[1]

#fields to convert to csv
field_list = ['delta', 'g_x', 'g_y', 'g_z', 'a_x', 'a_y', 'a_z', 'agl', 'temp', 'time', 'armed', 'cut']

p_time = 0
data_list = []

with open(INPUT_FILE, 'r') as f:
  s = '' 
  while True:
    try:
      while not s.startswith('2015'):
        s = f.next()
        s = s.rstrip()
        continue
      
      #line starts with 2015, parse the data set out
      #data order is always date, agl, cutter_stuff, accel, gyro, temp
      d = {}
      d['time'] = parser.parse(s)
      
      #agl
      s = f.next()
      s = f.next()
      s = s.rstrip()
      d['agl'] = float(s)
      
      #cutter stuff
      #act based on (0,0) (1,0) or (1,1) value of string
      s = f.next()
      s = s.rstrip()
      (arm, cut) = eval(s)
      d['armed'] = arm
      d['cut'] = cut
      
      #accelerometer
      s = f.next()
      s = f.next()
      s = s.rstrip()
      a, b = s.split()
      d['a_x'] = float(b)
      s = f.next()
      s = s.rstrip()
      a, b = s.split()
      d['a_y'] = float(b)
      s = f.next()
      s = s.rstrip()
      a, b = s.split()
      d['a_z'] = float(b)

      #gyro
      s = f.next()
      s = f.next()
      s = s.rstrip()
      a, b = s.split()
      d['g_x'] = float(b)
      s = f.next()
      s = s.rstrip()
      a, b = s.split()
      d['g_y'] = float(b)
      s = f.next()
      s = s.rstrip()
      a, b = s.split()
      d['g_z'] = float(b)

      #temp
      s = f.next()
      s = f.next()
      s = s.rstrip()
      d['temp'] = float(s)
      

      #calculate the delta field
      if (p_time == 0):
        #add delta field
        d['delta'] = 0
        p_time = d['time']
      else:
        delta = d['time'] - p_time
        d['delta'] = delta.total_seconds()
        p_time = d['time']

      data_list.append(d)
    except StopIteration:
      
      #write to a csv!
      csv_name = INPUT_FILE + '.csv'
      with open(csv_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_list)
        writer.writeheader()
        writer.writerows(data_list)
      sys.exit()      
      #done!
