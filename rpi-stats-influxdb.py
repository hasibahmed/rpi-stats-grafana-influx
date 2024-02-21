# !/usr/bin/env python
import datetime
import psutil
from influxdb import InfluxDBClient

# influx configuration - edit these
ifuser = "grafana"
ifpass = "<yourpassword>"
ifdb   = "home"
ifhost = "127.0.0.1"
ifport = 8086
measurement_name = "system"

# take a timestamp for this measurement
time = datetime.datetime.utcnow()

# collect some stats from psutil
disk = psutil.disk_usage('/')
mem = psutil.virtual_memory()
load = psutil.getloadavg()


cpu = psutil.cpu_percent(interval=1, percpu=True)
#cpu = psutil.cpu_times()
temp = psutil.sensors_temperatures()


#
connections = psutil.net_io_counters()
# format the data as a single measurement for influx
body = [
    {
        "measurement": measurement_name,
        "time": time,
        
        "fields": {
            "load_1": load[0],
            "load_5": load[1],
            "load_15": load[2],
            "cpu_percent": cpu,
            "disk_percent": disk.percent,
            "disk_free": disk.free,
            "disk_used": disk.used,
            "mem_percent": mem.percent,
            "mem_free": mem.free,
            "mem_used": mem.used,
            "temp": temp['cpu_thermal'][0].current,
	    "connections": connections
        }
    }
]

# connect to influx
# ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

# write the measurement
# ifclient.write_points(body)

print(body)
