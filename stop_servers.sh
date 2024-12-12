#!/bin/bash

# 检查 pids 目录是否存在
if [ ! -d "pids" ]; then
    echo "pids directory not found!"
    exit 1
fi

# 检查是否有 pid 文件
if [ ! -f "pids/servers.pid" ]; then
    echo "No pid file found!"
    exit 1
fi

# 读取并停止主进程
pid=$(cat "pids/servers.pid")
if ps -p $pid > /dev/null; then
    echo "Stopping process $pid"
    kill $pid
    # 等待进程结束
    sleep 2
    # 再次检查进程是否真的停止
    if ps -p $pid > /dev/null; then
        echo "Process $pid did not stop, trying force kill..."
        kill -9 $pid
    fi
else
    echo "Process $pid not found"
fi

# 清理 pid 文件
rm -f "pids/servers.pid"

# 最后检查是否还有相关进程在运行
remaining=$(ps aux | grep "python [c]oncurrent-servers.py" | wc -l)
if [ "$remaining" -gt 0 ]; then
    echo "Warning: Server process might still be running. Please check manually:"
    ps aux | grep "python [c]oncurrent-servers.py"
else
    echo "All servers stopped successfully"
fi