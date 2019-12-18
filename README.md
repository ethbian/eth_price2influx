# eth_price2influx
A python script to get Ethereum price in USD, EUR, BTC and send them to InfluxDB

## dependencies
- **requests** python library  
  *apt-get install python-requests*  
  *pip install requests*  
- **influxdb** python library  
  *apt-get install python-influxdb* or  
  *pip install influxdb*  
- Powered by **CoinGecko API**  

## quick start
- the script should be executed periodically as a crob job  


## data format

    > select * from eth_price order by desc limit 5;
    name: eth_price
    time                btc        eur    usd
    ----                ---        ---    ---
    1576710314865160960 0.01826094 119.46 132.79
    1576710199200453888 0.01826094 119.46 132.79
    1576710037965385984 0.01826894 119.47 132.8
    1576709992666340096 0.01829033 119.41 132.74
    1576709973784369920 0.01829033 119.41 132.74

## use case
Here's a [TODO screenshot](https://ethbian.org/images/TODO) of Grafana dashboard using the provided data.  

Pull requests are more than welcome if you're fixing something