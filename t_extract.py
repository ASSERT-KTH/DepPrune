# get data for one column
with open(f'statistic.txt', "r") as file:
    lines = file.readlines()

sorted_lines = sorted(lines)
numbers = []
for item in sorted_lines:
    number = item.split(',')[1]
    numbers.append(number)

with open(f'statistic.txt', "w") as file:
    file.writelines(numbers)