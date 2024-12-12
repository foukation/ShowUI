#!/bin/bash

# 创建必要的目录
mkdir -p logs pids

# 检查当前是否已在目标环境中
if [[ "$CONDA_DEFAULT_ENV" != "env_yhs_ShowUI" ]]; then
    source /root/anaconda3/bin/activate env_yhs_ShowUI
fi

# 设置环境变量
export LD_LIBRARY_PATH=/root/anaconda3/envs/env_yhs_ShowUI/lib/python3.10/site-packages/torch/lib/../../nvidia/nvjitlink/lib:/root/anaconda3/envs/env_yhs_ShowUI/lib/python3.10/site-packages/torch/lib/../../nvidia/cusparse/lib:$LD_LIBRARY_PATH
export PATH=/usr/bin:$PATH

# 运行 concurrent-servers.py
nohup python concurrent-servers.py > logs/servers.log 2>&1 &
echo $! > pids/servers.pid
echo "concurrent-servers.py started with PID $(cat pids/servers.pid)"

echo "Servers are running"