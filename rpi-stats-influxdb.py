# !/home/pi/.cache/pypoetry/virtualenvs/rpi-stats-grfana-influx-34pQiECe-py3.11/bin/python3.11
import datetime
import psutil
from influxdb import InfluxDBClient

# influx configuration - edit these
ifuser = "grafana"
ifpass = "Fne6Z58ewQdDFn"
ifdb   = "pisysmonitor"
ifhost = "192.168.1.131"
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
            "cpu1_percent": cpu[0],
            "cpu2_percent": cpu[1],
            "cpu3_percent": cpu[2],
            "disk_percent": disk.percent,
            "disk_free": float(disk.free),
            "disk_used": float(disk.used),
            "mem_percent": mem.percent,
            "mem_free": float(mem.free),
            "mem_used": float(mem.used),
            "temp": float(temp['cpu_thermal'][0].current),
	    "bytes_sent": float(connections.bytes_sent),
            "bytes_recv": float(connections.bytes_recv),
            "packets_sent": float(connections.packets_sent),
            "packets_recv": float(connections.packets_recv),
            "errin": float(connections.errin),
            "errout": float(connections.errout),
            "dropin": float(connections.dropin),
            "dropout": float(connections.dropout)
        }
    }
]

# connect to influx
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

# write the measurement
ifclient.write_points(body)

#print(body)
