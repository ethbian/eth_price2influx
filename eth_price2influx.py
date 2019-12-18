#!/usr/bin/env python
"""
Use the script to:
- get Ethereum price in USD, EUR, BTC
  (powered by CoinGecko API)
- send it to InfluxDB database
...so that it could be used with eg. Grafana
https://ethbian.org | https://github.com/ethbian/ethbian/
"""
import datetime
import json

try:
    import requests
except ImportError:
    raise ImportError('\n\n cannot find Python library: requests\n' +
                      ' try executing: pip install python-requests or pip install requests')

try:
    import influxdb
except ImportError:
    raise ImportError('\n\n cannot find Python library: influxdb\n' +
                      ' try executing: pip install influxdb or apt-get install python-influxdb')

DB_HOST = 'localhost'
DB_PORT = 8086
DB_NAME = 'collectd'
DB_TABLE = 'eth_price'
URL = 'https://api.coingecko.com/api/v3/simple/price'
PARAMS = {'ids': 'ethereum', 'vs_currencies': 'btc,usd,eur'}
HEADERS = {'Accept': 'application/json'}

try:
    db_client = influxdb.InfluxDBClient(
        host=DB_HOST, port=DB_PORT, database=DB_NAME)
except Exception as e:
    raise SystemExit('Error connecting to database: {}'.format(e))

data_ok = False
try:
    response = requests.get(URL, params=PARAMS, headers=HEADERS)
    if response.status_code == 200:
        data_ok = True
except Exception as e:
    print 'Error getting the data: {}'.format(e)

if data_ok:
    response_json = response.json()
    price2db = response_json['ethereum']
else:
    price2db = {u'usd': 0.0, u'btc': 0.0, u'eur': 0.0}

data2db = {}
data2db['measurement'] = DB_TABLE
data2db['time'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
data2db['fields'] = price2db

try:
    db_client.write_points([data2db])
except Exception as e:
    print 'Error writing to database: {}'.format(e)
else:
    print 'ETH price sent to db: {}'.format(price2db)

db_client.close()
