FILE_INPUT = "data_input.txt"
FILE_OUPUT = "data_output.txt"

f = open(FILE_INPUT, "r")
temp = list()

for x in f:
    result = int(x)/94
    #roundedResult = round(result, 4)
    temp.append(result)
# for

f = open(FILE_OUPUT, "w")
for i in temp:
    f.write(str(i)+"\n")
f.close()