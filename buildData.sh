#!/bin/bash
if [ ! -d './public/data' ]; then
    mkdir './public/data'
fi

if [ -f './externalData/nhc.data.csv' ]; then
    if [ -f './public/data/nhc.data.csv' ]; then
        rm -rf './public/data/nhc.data.csv'
    fi
    cp './externalData/nhc.data.csv' './public/data/nhc.data.csv'
else
    echo 'Build Failed. NHC Data not existst.'
    return 1
fi

if [ -d './Novel-Coronavirus-Updates' ];  then
    rm -rf './Novel-Coronavirus-Updates'
fi

git clone https://github.com/839-Studio/Novel-Coronavirus-Updates.git --depth=1

if [ -d './DXY-COVID-19-Data' ];  then
    rm -rf './DXY-COVID-19-Data'
fi

git clone https://github.com/BlankerL/DXY-COVID-19-Data.git --depth=1

python3 python/overall_data.py
python3 python/dxy_data.py
python3 python/cases_data.py
python3 python/media_data.py

echo "public data ls:"
ls ./public/data