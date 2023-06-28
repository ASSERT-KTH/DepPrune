#!/bin/bash

file1="Logs/rerun_test_1000_commits_waiting.txt"
file2="Logs/rerun_test_1000_commits_waiting_copy.txt"

# 排序两个文件
sort "$file1" -o "$file1"
sort "$file2" -o "$file2"

# 获取文件1中存在而文件2中不存在的行
diff_lines=$(comm -23 "$file1" "$file2")

# 输出差集的行
echo "$diff_lines"
