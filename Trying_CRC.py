def CRC(line):
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

				if len(remainder) == 0:
					break
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

CRC_32 = '1101'
message = '110100101'
# CRC_32 = '1101'
# message = '100100'

line = list(message)

a = CRC(line)
print a
while len(a) < len(CRC_32) - 1:
	a.insert(0,'0')
data = ''
for i in a:
	data += i
print data