file = open("resource_1.txt", "r")
file_string = file.read()
in_one_line = file_string.replace('\n', ' ')
split_sting = in_one_line.split(' ')
result_array = []

while len(split_sting) != 0:
    counter = 0
    take_first_element = split_sting[0]
    for non in range(len(split_sting)):
        for i in split_sting:
            if i == take_first_element:
                counter += 1
                split_sting.remove(i)
    result_array.append([take_first_element, counter])

    for i in range(len(result_array)):
        for j in range(i + 1, len(result_array)):
            if result_array[i][1] < result_array[j][1]:
                result_array[i], result_array[j] = result_array[j], result_array[i]

file = open("result_1.txt", "w")
file_string = ""

for i in range(len(result_array)):
    print("{0} {1}".format(result_array[i][0], result_array[i][1]))
    file_string += "{0} {1}\n".format(result_array[i][0], result_array[i][1])

file.write(file_string)