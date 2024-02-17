# Install Grafana

* Add the APT key used to authenticate packages:

```bash
sudo mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
```

* Add the Grafana APT repository:
```bash
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
```

* Install Grafana:

```bash
sudo apt-get update
sudo apt-get install -y grafana
```
Grafana is now installed, but not yet running. To make sure Grafana starts up even if the Raspberry Pi is restarted, we need to enable and start the Grafana Systemctl service.

* Enable the Grafana server:
    
```bash 
sudo /bin/systemctl enable grafana-server
```

* Start the Grafana server:

```bash
sudo /bin/systemctl start grafana-server
```

Grafana is now running on the machine and is accessible from any device on the local network.Open a browser and go to `http://<ip address>:3000`, where the IP address is the address that you used to connect to the Raspberry Pi earlier. You’re greeted with the Grafana login page. Log in to Grafana with the default username admin, and the default password admin. Change the password for the admin user when asked.

# Install Influxdb

* Obtain and verify the new key: 

```bash
$ wget -q https://repos.influxdata.com/influxdata-archive_compat.key
$ gpg --with-fingerprint --show-keys ./influxdata-archive_compat.key
pub   
```
```bash
rsa4096 2023-01-18 [SC] [expires: 2026-01-17]
  	9D53 9D90 D332 8DC7 D6C8  D3B9 D8FF 8E1F 7DF8 B07E
uid                  	InfluxData Package Signing Key <support@influxdata.com>
```

* Install the new key. If the above key doesn't work, get the latest key information from: [influxdb_keyrotation](https://www.influxdata.com/blog/linux-package-signing-key-rotation/)

```bash
$ cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null
```

* Update apt sources to use the new key:

```bash
$ echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list
```

* Clean up the old key if required:

```bash
sudo rm -f /etc/apt/trusted.gpg.d/influxdb.gpg
```

* Confirm that `sudo apt-get update` returns no errors for https://repos.influxdata.com

*  Install influxdb

```bash
$ sudo apt install -y influxdb
```

* Start and enable the services to run after each reboot: 

```bash
$ sudo systemctl unmask influxdb.service
$ sudo systemctl start influxdb
$ sudo systemctl enable influxdb.service
```

* Example to create a database and users 

```bash
$ influx

> create database home
> use home

> create user grafana with password '<passwordhere>' with all privileges
> grant all privileges on home to grafana

> show users

user admin
---- -----
grafana true
```