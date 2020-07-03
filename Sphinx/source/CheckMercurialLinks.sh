#!/bin/bash

grep -r '<https://hg.orthanc-server.com' | grep -v CheckMercurialLinks.sh | cut -d '<' -f 2 | cut -d '>' -f 1 | sort | uniq | while read url
do
    echo "${url}"
    curl -s "${url}" > /dev/null
    if [ $? -ne 0 ]
    then
        echo "ERROR!!!"
        exit -1
    fi
done

echo "SUCCESS"
