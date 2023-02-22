import sys
import os

filePath = f'top_target_174.txt'
newFilePath = f'top_target_174_sorted.txt'

with open(filePath) as f:
    lines = f.read().splitlines()

lines.sort()

newFile = open(newFilePath, 'w')
for line in lines:
    newFile.writelines(line + '\n')
newFile.close()