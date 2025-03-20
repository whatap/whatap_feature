#!/usr/bin/env bash

rm -f dist/main
docker run --rm -v $PWD:/app -w /app -u 1000 feature_build:redhat8 sh -c "/app/build.sh" 
mv dist/main /mnt/c/Users/namhs/Downloads/whfmgr_redhat8_x86_64

docker run --rm -v $PWD:/app -w /app -u 1000 feature_build:redhat7 sh -c "/app/build.sh" 
mv dist/main /mnt/c/Users/namhs/Downloads/whfmgr_redhat7_x86_64


docker run --rm -v $PWD:/app -w /app -u 1000 feature_build:ubuntu2404 sh -c "/app/build.sh" 
mv dist/main /mnt/c/Users/namhs/Downloads/whfmgr_ubuntu_2404_x86_64

docker run --rm -v $PWD:/app -w /app -u 1000 feature_build:ubuntu2204 sh -c "/app/build.sh" 
mv dist/main /mnt/c/Users/namhs/Downloads/whfmgr_ubuntu_2204_x86_64
