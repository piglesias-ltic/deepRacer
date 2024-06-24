#!/bin/bash

for url in ":8100/menu.html" ":8100/Training_and_Evaluation_Overview.html" ":8100/Training_progress.html" ":8100/?robo=all&camera=kvs_stream&quality=75&width=480" ":3000/d/adke0lwv5zwg0e/deepracer-training-template?orgId=1update_to_grafana_urlrefresh%3D10s&refresh=10s&from=now-90m&to=now"
do 
    /usr/bin/open -a "/Applications/Google Chrome.app" "http://"$1$url
done
