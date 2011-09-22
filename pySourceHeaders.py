import os, fnmatch, sys

def put_header(header, dir, filter = '*', comment_char = '#'):

	files = []
	line_comment = comment_char

	for i in os.walk(dir):
		for j in i[2]:
			files.append(i[0].replace('\\', '/') + '/' + j)
	
	files = fnmatch.filter(files, filter)
	
	commented_header = ''
	for line in header.split('\n'):
		commented_header += line_comment + ' ' + line + '\n'
		
	print 'Writing header:\n' + commented_header + 'To files:\n'
	
	for file in files:
		with open(file, 'r+') as f:
			existing = f.read()
			f.seek(0)
			f.truncate()
			f.write(commented_header + '\n' + existing)
			print file
			
def drop_header(num_lines, dir, filter = '*'):

	files = []

	for i in os.walk(dir):
		for j in i[2]:
			files.append(i[0].replace('\\', '/') + '/' + j)
	
	files = fnmatch.filter(files, filter)
	
	for file in files:
		with open(file, 'r+') as f:
			lines = f.readlines()
			f.seek(0)
			f.truncate()
			f.writelines(lines[num_lines:])
		print 'Dropped ' + num_lines + ' lines from ' + file

def test_header(header, dir, filter = '*', comment_char = '#'):

	files = []
	passed = []
	failed = []
	line_comment = comment_char

	for i in os.walk(dir):
		for j in i[2]:
			files.append(i[0].replace('\\', '/') + '/' + j)
	
	files = fnmatch.filter(files, filter)
	print files
	
	commented_header = ''
	for line in header.split('\n'):
		commented_header += line_comment + ' ' + line + '\n'
		
	print 'Testing header:\n' + commented_header
	
	for file in files:
		with open(file, 'r') as f:
			if f.read(len(commented_header)) == commented_header:
				passed.append(file)
			else:
				failed.append(file)
				
	print 'Passed:'
	for f in passed:
		print f
	print 'Failed:'
	for f in failed:
		print f

if __name__ == '__main__':
	
	if sys.argv[1] == '-drop':
		drop_header(int(sys.argv[2]), sys.argv[3], sys.argv[4])
	elif sys.argv[1] == '-put':
		put_header(open(sys.argv[2]).read(), sys.argv[4], sys.argv[5], sys.argv[3])
	elif sys.argv[1] == '-test':
		test_header(open(sys.argv[2]).read(), sys.argv[4], sys.argv[5], sys.argv[3])
	else:
		put_header(open(sys.argv[1]).read(), sys.argv[3], sys.argv[4], sys.argv[2])		