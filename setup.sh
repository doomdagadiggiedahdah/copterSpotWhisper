#!/bin/bash

export PATH="/root/.local/bin:$PATH"

## install packages
add-apt-repository ppa:apt-fast/stable -y
apt install apt-fast -y

apt update
apt install ffmpeg
apt-get install nvim pigz
alias vim="nvim"

curl -LsSf https://astral.sh/uv/install.sh | sh # uv
uv venv
source .venv/bin/activate
uv pip install -U transformers openai-whisper psutil

## comfort food
set -o vi
shopt -s autocd

## install first audio
if [[ -d "./audio/2021/09" ]]; then
    echo "already downloaded tar ball"
else
    wget http://radio.copterspotter.com/delta/202109.tar.gz
    mkdir ./audio

    tar xvzf 202109.tar.gz -C ./audio/

    # tar xvzf 202109.tar.gz -C ./audio/ \
    #     2021/09/20210901_000226.mp3 \
    #     2021/09/20210901_000526.mp3 \
    #     2021/09/20210901_000839.mp3 \
    #     2021/09/20210901_001001.mp3 \
    #     2021/09/20210901_001006.mp3 \
    #     2021/09/20210901_001018.mp3 \
    #     2021/09/20210901_001309.mp3 \
    #     2021/09/20210901_001332.mp3 \
    #     2021/09/20210901_010439.mp3 \
    #     2021/09/20210901_010445.mp3

fi


## list of all tarballs
# http://radio.copterspotter.com/delta/202109.tar.gz
# http://radio.copterspotter.com/delta/202210.tar.gz
# http://radio.copterspotter.com/delta/202405.tar.gz
# http://radio.copterspotter.com/delta/202110.tar.gz
# http://radio.copterspotter.com/delta/202211.tar.gz
# http://radio.copterspotter.com/delta/202406.tar.gz
# http://radio.copterspotter.com/delta/202111.tar.gz
# http://radio.copterspotter.com/delta/202212.tar.gz 
# http://radio.copterspotter.com/delta/202308.tar.gz
# http://radio.copterspotter.com/delta/202407.tar.gz
# http://radio.copterspotter.com/delta/202112.tar.gz
# http://radio.copterspotter.com/delta/202309.tar.gz 
# http://radio.copterspotter.com/delta/202408.tar.gz
# http://radio.copterspotter.com/delta/202201.tar.gz 
# http://radio.copterspotter.com/delta/202301.tar.gz 
# http://radio.copterspotter.com/delta/202310.tar.gz  
# http://radio.copterspotter.com/delta/202409.tar.gz
# http://radio.copterspotter.com/delta/202204.tar.gz
# http://radio.copterspotter.com/delta/202302.tar.gz
# http://radio.copterspotter.com/delta/202311.tar.gz
# http://radio.copterspotter.com/delta/202411.tar.gz
# http://radio.copterspotter.com/delta/202205.tar.gz
# http://radio.copterspotter.com/delta/202303.tar.gz
# http://radio.copterspotter.com/delta/202312.tar.gz 
# http://radio.copterspotter.com/delta/202412.tar.gz
# http://radio.copterspotter.com/delta/202206.tar.gz
# http://radio.copterspotter.com/delta/202304.tar.gz
# http://radio.copterspotter.com/delta/202207.tar.gz
# http://radio.copterspotter.com/delta/202305.tar.gz
# http://radio.copterspotter.com/delta/202401.tar.gz 
# http://radio.copterspotter.com/delta/202208.tar.gz
# http://radio.copterspotter.com/delta/202306.tar.gz
# http://radio.copterspotter.com/delta/202402.tar.gz
# http://radio.copterspotter.com/delta/202209.tar.gz
# http://radio.copterspotter.com/delta/202307.tar.gz
# http://radio.copterspotter.com/delta/202403.tar.gz


# "http://radio.copterspotter.com/delta/202109.tar.gz", 
# "http://radio.copterspotter.com/delta/202210.tar.gz", 
# "http://radio.copterspotter.com/delta/202405.tar.gz", 
# "http://radio.copterspotter.com/delta/202110.tar.gz", 
# "http://radio.copterspotter.com/delta/202211.tar.gz", 
# "http://radio.copterspotter.com/delta/202406.tar.gz", 
# "http://radio.copterspotter.com/delta/202111.tar.gz", 
# "http://radio.copterspotter.com/delta/202212.tar.gz", 
# "http://radio.copterspotter.com/delta/202308.tar.gz", 
# "http://radio.copterspotter.com/delta/202407.tar.gz", 
# "http://radio.copterspotter.com/delta/202112.tar.gz", 
# "http://radio.copterspotter.com/delta/202309.tar.gz", 
# "http://radio.copterspotter.com/delta/202408.tar.gz", 
# "http://radio.copterspotter.com/delta/202201.tar.gz", 
# "http://radio.copterspotter.com/delta/202301.tar.gz", 
# "http://radio.copterspotter.com/delta/202310.tar.gz", 
# "http://radio.copterspotter.com/delta/202409.tar.gz", 
# "http://radio.copterspotter.com/delta/202204.tar.gz", 
# "http://radio.copterspotter.com/delta/202302.tar.gz", 
# "http://radio.copterspotter.com/delta/202311.tar.gz", 
# "http://radio.copterspotter.com/delta/202411.tar.gz", 
# "http://radio.copterspotter.com/delta/202205.tar.gz", 
# "http://radio.copterspotter.com/delta/202303.tar.gz", 
# "http://radio.copterspotter.com/delta/202312.tar.gz", 
# "http://radio.copterspotter.com/delta/202412.tar.gz", 
# "http://radio.copterspotter.com/delta/202206.tar.gz", 
# "http://radio.copterspotter.com/delta/202304.tar.gz", 
# "http://radio.copterspotter.com/delta/202207.tar.gz", 
# "http://radio.copterspotter.com/delta/202305.tar.gz", 
# "http://radio.copterspotter.com/delta/202401.tar.gz", 
# "http://radio.copterspotter.com/delta/202208.tar.gz", 
# "http://radio.copterspotter.com/delta/202306.tar.gz", 
# "http://radio.copterspotter.com/delta/202402.tar.gz", 
# "http://radio.copterspotter.com/delta/202209.tar.gz", 
# "http://radio.copterspotter.com/delta/202307.tar.gz", 
# "http://radio.copterspotter.com/delta/202403.tar.gz", 