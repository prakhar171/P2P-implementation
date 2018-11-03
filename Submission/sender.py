import os

#CRC-32: x^32 + x^26 + x^23 + x^22 + x^16 + x^12 + x^11 + x^10 + x^8 + x^7 + x^5 + x^4 + x^2 + x + 1

CRC_32 = '100000100110000010001110110110111'
start_flag = '10000001'
end_flag = '11111111'
escape = '01111110'

f = open("Sender_File.txt", "rb")
f2 = open("f_send.txt","w")
data = f.read()

frame = []
counter = 0

def CRC(line):
	for i in range(len(CRC_32)-1):
		line.append('0')
	remainder = []
	# print line
	j = 0
	while j < len(line):
		x = True
		if len(remainder) != 0:
			# print remainder
			while remainder[0] == '0':
				if len(remainder) == 0:
					break
				else:
					remainder.pop(0)
			# print remainder
		while len(remainder) < len(CRC_32):
			if j == len(line):
				x = False
				break
			remainder.append(line[j])
			j += 1
		# print j
		# print remainder
		if x == False:
			break

		for i in range(len(CRC_32)):
			if CRC_32[i] == remainder[i]:
				remainder[i] = '0'
			else:
				remainder[i] = '1'
		# print remainder
	return remainder

def convert_binary(character):
	string = ''
	binary_value = bin(i)[2:]
	character = (list(binary_value))
	while len(character) < 8:
		character.insert(0,'0')
	for j in character:
		string = string + j
	return string

for i in data:
	counter += 1
	if (counter == 9):
		f2.write('\n')
		counter = 1
	string = convert_binary(i)
	f2.write(string)
f.close()
f2.close()

f2 = open("f_send.txt","r")
f3 = open("Temp.txt","w")
data = f2.read(64)
while data != '':
	line = list(data)
	parity_bits = (CRC(line))
	if len(parity_bits) == len(CRC_32):
		parity_bits.pop(0)
	while len(parity_bits) < 32:
		parity_bits.insert(0,'0')
	# print(len(parity_bits))
	for i in parity_bits:
		data = data + i
	f3.write(data)
	data = f2.read(1)
	data = f2.read(64)
f2.close()
f3.close()
os.remove('f_send.txt')
os.rename('Temp.txt','f_send.txt')

f1 = open('f_send.txt','r')
f2 = open('Temp.txt','w')
data = f1.read(8)
# data = f1.read()
counter = 0
while data != '':
	# print (data)
	counter += 1
	if (counter == 13):
		f2.write(end_flag)
		counter = 1

	if (counter == 1):
		f2.write(start_flag)

	if data == start_flag or data == end_flag or data == escape:
		f2.write(escape)
		f2.write(data)

	else:
		f2.write(data)

	data = f1.read(8)
f2.write(end_flag)
f1.close()
f2.close()
os.remove('f_send.txt')
os.rename('Temp.txt','f_send.txt')
