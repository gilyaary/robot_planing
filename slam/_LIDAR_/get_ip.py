import subprocess
test = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE)
output = str(test.communicate()[0])
lines = output.split("\\n")

for line in lines:
    #print(line)
    if "192." in line:
        start_index = int(line.index("192."))
        end_index = int(line.index(' ', start_index))
        #print(start_index, end_index)
        print(line[start_index:end_index])