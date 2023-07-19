#!/bin/bash

script_path="scripts/tempScript1.sh"
interval=1200  # 检测间隔时间（秒）

while true; do
    # 检测指定脚本是否正在运行
    if ! pgrep -f "$script_path" >/dev/null; then
        echo "脚本未运行，重新运行中..."
        # 运行指定脚本
        bash "$script_path" 2>>test_removals_Error.log >> test_removals.log &
    fi
    sleep "$interval"
done
