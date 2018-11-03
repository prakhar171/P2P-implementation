binfile = open("Binary_file.txt","r")
writefile = open("writefile.txt","w")

count = 0
while True:
    word = binfile.read(8)
    if word == '':
        break
    if word == '10000001':
        writefile.write("[start] ")
        # print ("start")
        count += 1

    elif word == '11111111':
        # print ("end")
        writefile.write(" [end]")
        writefile.write("\n")
        count += 1

    elif word == '01111110':
        writefile.write(" [escape]")
        writefile.write("\n")
    else:
        writefile.write(word)
        # print (word)
