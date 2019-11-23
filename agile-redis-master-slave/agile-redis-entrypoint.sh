#!/bin/bash

CONF_FILE=/etc/redis/redis.conf

if [ ! -f $CONF_FILE ]
then
    echo "appendonly yes" > $CONF_FILE

    if [ -n "$REDIS_MASTER_HOST" ]
    then
       echo "slaveof $REDIS_MASTER_HOST ${REDIS_MASTER_PORT:-6379}" >> $CONF_FILE
    fi
    chown redis:redis $CONF_FILE
fi

exec docker-entrypoint.sh redis-server /etc/redis/redis.conf