#!/bin/bash

script_path="scripts/run_test_for_coverage.sh"
interval=1200  # 检测间隔时间（秒）

while true; do
    # 检测指定脚本是否正在运行
    if ! pgrep -f "$script_path" >/dev/null; then
        echo "脚本未运行，重新运行中..."
        # 运行指定脚本
        bash "$script_path" 2>>top_1000_commits_coverage_error3.log >> top_1000_commits_coverage3.log &
    fi
    sleep "$interval"
done
