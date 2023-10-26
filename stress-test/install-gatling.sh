#!/bin/bash

GATLING_VERSION="3.9.5"

if [ $# -ne 1 ]; then
    echo "Usage: $0 <install directory>"
    exit 1
fi

directory="$1"

if [ -d "$directory" ]; then
    absolute_install_path=$(realpath "$directory")
    echo "Installing to: $absolute_install_path"
else
    echo "Invalid install directory: $directory"
    exit -1
fi

tmp_directory=$(mktemp -d)
curr_dir=$(pwd)

cd "$tmp_directory" && \
  echo "Downloading Gatling ${GATLING_VERSION}" && \
  curl -fsSL "https://repo1.maven.org/maven2/io/gatling/highcharts/gatling-charts-highcharts-bundle/${GATLING_VERSION}/gatling-charts-highcharts-bundle-3.9.5-bundle.zip" > ./gatling.zip && \
  rm -rf ./gatling && \
  unzip gatling.zip && \
  mv gatling-charts-highcharts-bundle-3.9.5 gatling-$GATLING_VERSION && \
  mv gatling-$GATLING_VERSION $absolute_install_path && \
  rm gatling.zip && \
  cd $curr_dir && \
  rm -rf "$tmp_directory" && \
  echo "All done!"

