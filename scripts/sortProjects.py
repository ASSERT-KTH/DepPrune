import sys
import os

filename = sys.argv[1]

filePath = f'{filename}.txt'
newFilePath = f'{filename}_sorted.txt'

with open(filePath) as f:
    lines = f.read().splitlines()

lines.sort()

newFile = open(newFilePath, 'w')
for line in lines:
    newFile.writelines(line + '\n')
newFile.close()