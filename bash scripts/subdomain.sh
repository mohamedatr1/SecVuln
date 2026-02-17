#!/bin/bash

if [ $# -eq 0 ]
then
    echo "How to use : ./sub_finder <domain>"
    echo "Ex: ./sub_finder www.example.com"
else
    rm -f index.html sub.txt valid_sub.txt ips.txt

    target=$1
    if [[ ! $target =~ ^http ]]; then
        target="http://$target"
    fi

    wget -q "$target" -O index.html 2> /dev/null

    if [ -f index.html ]; then

        strings index.html | grep "http" | cut -d "/" -f 3 | cut -d '"' -f 1 | grep "$1" | cut -d "?" -f 1 | tr -d "'," | sort -u > sub.txt
    fi

    if [ -s sub.txt ]; then
        for sub in $(cat sub.txt)
        do
            if ping -c 1 -W 1 "$sub" > /dev/null 2>&1
            then
                echo "$sub ++++ pong"
                echo "$sub" >> valid_sub.txt
            else
                echo "$sub ---- Error"
            fi
        done
    fi

    if [ -f valid_sub.txt ]; then
        for i in $(cat valid_sub.txt)
        do
            host "$i" | grep "has address" | awk '{print $4}' >> ips.txt
        done
        sort -u ips.txt -o ips.txt
    fi

    echo "DONE ...!"
    rm -f index.html
fi
         
