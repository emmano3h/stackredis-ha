import os
from flask import Flask
from redis.sentinel import Sentinel

app = Flask(__name__)

sentinelHost = os.environ.get("SENTINEL_HOST", None)
sentinelPort = int(os.environ.get("SENTINEL_PORT", 26379))
redisMasterName = os.environ.get("REDIS_MASTER_NAME", 'mymaster')



@app.route('/')
def hello():
    if sentinelHost is not None and sentinelPort is not None:
        try:
            sentinel = Sentinel([(sentinelHost, sentinelPort)], socket_timeout=0.1)
            redis_master = sentinel.master_for(redisMasterName, socket_timeout=0.1)
            redis_slave = sentinel.slave_for(redisMasterName, socket_timeout=0.1)

            incr_and_return_count = redis_master.incr('hits')
            count_from_slave = redis_slave.get('hits')
            return 'Hello World! I have been seen {} times. Yes Yeah\n'.format(count_from_slave)
        except Exception as e:
            return sentinelHost+ " "+ str(sentinelPort) + 'Exception handled when started to perform actions: Details error {}\n'.format(e)
    else:
        return 'Environment variable sentinelHost or sentinelPort  is not found or empty. \n'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=611, debug=True)