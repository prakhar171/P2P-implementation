binfile = open("f_err.txt","r")
decfile = open("f_detect.txt", "w")

CRC_32 = '100000100110000010001110110110111'
start_flag = '10000001'
end_flag = '11111111'
escape = '01111110'


def xor(divisor, dividend):
    answer = []
    length = len(dividend)
    for i in range(1, length):
        if divisor[i] == dividend[i]:
            answer.append('0')
        else:
            answer.append('1')
    answer = ''.join(answer)
    return answer

def remainder_f(dividend, divisor):
    position = len(divisor)
    div_length = len(divisor)
    new_dividend = dividend[0:position]
    temp = ''
    end = len(dividend)
    while position < end:
        if new_dividend[0] == '1':
            temp = xor(divisor, new_dividend)
            new_dividend = temp + dividend[position]

        elif new_dividend[0] == '0':
            temp = xor('0' * div_length, new_dividend)
            new_dividend = temp + dividend[position]

        position += 1

    if new_dividend[0] == '1':
        new_dividend = xor(divisor, new_dividend)
    else:
        new_dividend = xor('0'* div_length, new_dividend)

    remainder = new_dividend
    return remainder

def write2file(err_check, crc_input):
    decfile.write(start_flag)
    decfile.write(crc_input)
    decfile.write(end_flag)
    decfile.write("\n")
    decfile.write(err_check)
    decfile.write("\n")

crc_input = ""
escapeflag = False
#   main function
while True:
    word = binfile.read(8)	# initialize reading
    if word == '':	# reached end of binary file
    	break
    
    if escapeflag == True:
        crc_input = crc_input + word
        escapeflag = False
        continue
    
    if word == escape:
        escapeflag = True
        continue
    elif word == start_flag:	# start flag encountered
        reading = True
        # word = binfile.red(8)	# initialize reading
        continue
    elif word == end_flag:
        reading = False
        check = remainder_f(crc_input,CRC_32)
        final_rem = 0
        for i in check:
        	if i == '1':
        		final_rem = 1
        		break
        if final_rem == 0:
        	write2file('0', crc_input)
        else:
        	write2file('1', crc_input)

        crc_input = ""	# reset frame content

    if reading == True:
    	crc_input = crc_input + word
    	
binfile.close()
decfile.close()
