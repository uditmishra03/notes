#!/bin/bash

file="app.log"

if [ ! -f "$file" ]; then
    echo "$file does not exist, creating..."
    touch "$file"
fi

while true
do
    echo "ERROR inventory-service DB connection timeout host=db-prod-01 latency=5000ms" >> $file
    sleep 15
    echo "INFO api-gateway Request completed method=GET endpoint=/api/v1/orders status=200 latency=45ms" >> $file
done

