import flask
import sys
import os
from redis import Redis
from datetime import timedelta
import requests # for sending HTTP requests
import socket 

print("****************************************") 
port = int(os.environ['PORT'])
Address = os.environ['ADDRESS']
API_KEY = os.environ['API_KEY']
time_to_expire = int(os.environ['TIME_TO_EXPIRE'])
cryptoname = os.environ['NAME']
print("****************************************")
print("****************************************")

redis = Redis(host='redis', port = 6379) # connect to the redis server -- host is the name of the redis container
APP = flask.Flask(__name__) # create the Flask app


@APP.route('/', methods=['GET'])   # route for the home page
def get_price(): # function to get the price
    host_name = socket.gethostname()

    if redis.exists(cryptoname) and redis.ttl(cryptoname) > 0: # check if the key exists
        return {'name': cryptoname , 'value': redis.get(cryptoname).decode() , 'host_name': host_name} # return the value from the cache
    price = requests.get( Address + cryptoname, headers={'X-CoinAPI-Key' : API_KEY}) # get the price from the API
    response = price.json()[0] # return the price

    redis.setex(    # set the key to expire in 5 minutes
    cryptoname,   # key
    timedelta(minutes=time_to_expire),  # time to expire
    response['price_usd'] # value
    )

    return {'name': response['name']  ,'price_usd': response['price_usd'], 'host_name': host_name} # return the json response

if __name__ == '__main__':

    APP.run(host='0.0.0.0' , port=port) # run the app

    # docker exec -it myredis sh             to get into the redis container
    # redis-cli                               to get into the redis cache``
    # keys *                                  to see all the keys
    # set key value                           to set a key
    # get key                                 to get a key


    # docker volume create myredisdata        to create a volume
    # docker run -d -p 6379:6379 --name myredis -v myredisdata:/data redis   to run the redis container with the volume
    # docker inspect container_name          to inspect the container

 # docker create network mynetwork         to create a network