import sys
import os

project = sys.argv[1]

filePath = f'./Data/{project}/{project}_pure_bloated_nodes.txt'
functionFilePath = f'./Data/{project}/{project}_function_removal.txt'
fileFilePath = f'./Data/{project}/{project}_file_removal.txt'

with open(filePath) as f:
    lines = f.read().splitlines()

old = '/data/js-variants/multee/Playground/'
newPathFunction = '/data/js-variants/multee/VariantsPureDep/' + project + '/variant_functions/'
newPathFile = '/data/js-variants/multee/VariantsPureDep/' + project + '/variant_files/'

# replace /data/js-variants/multee/Playground/ with /data/js-variants/multee/VariantsPureDep/base/variant_functions/
functionFile = open(functionFilePath, 'w')
for line in lines:
    newStr = line.replace(old, newPathFunction)
    functionFile.writelines(newStr + '\n')
functionFile.close()


# replace /data/js-variants/multee/Playground/ with /data/js-variants/multee/VariantsPureDep/base/variant_files/
functionFile = open(fileFilePath, 'w')
for line in lines:
    newStr = line.replace(old, newPathFile)
    functionFile.writelines(newStr + '\n')
functionFile.close()