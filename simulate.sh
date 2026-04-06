#!/bin/bash

while true
do
    r=$((RANDOM % 3))

    if [ $r -eq 0 ]; then
        echo "Normal traffic"
        for i in {1..10}
        do
            curl -s http://localhost:8000/ > /dev/null
            sleep 0.5
        done

    elif [ $r -eq 1 ]; then
        echo "Traffic spike"
        for i in {1..30}
        do
            curl -s http://localhost:8000/ > /dev/null &
        done
        wait

    else
        echo "Failure simulation"
        for i in {1..10}
        do
            curl -s http://localhost:8001/auth > /dev/null &
            curl -s http://localhost:8002/data > /dev/null &
        done
        wait
    fi

    sleep 2
done