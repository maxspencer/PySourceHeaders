# (C) Copyright 2011 Active Web Solutions Ltd
#     All rights reserved.
# This software is provided "as is" without warranty of any kind, express or
# implied, including but not limited to warranties as to quality and fitness
# for a particular purpose. Active Web Solutions Ltd does not support the
# Software, nor does it warrant that the Software will meet your requirements or
# that the operation of the Software will be uninterrupted or error free or that
# any defects will be corrected. Nothing in this statement is intended to limit
# or exclude any liability for personal injury or death caused by the negligence
# of Active Web Solutions Ltd, its employees, contractors or agents.

'''

	pySourceHeaders: A module for controlling the headers in your source code.
	
pySourceHeaders is a helpful module for writing, checking and removing the
discalimers and other headers often found at the top of your source code files.

'''
import os, fnmatch, sys

def _commented_header(header, comment_start, comment_end = ''):
	''' Returns the lines in header each appropriately commented.
	'''
	commented_header = ''
	
	for line in header.splitlines():
		commented_header += comment_start + ' ' + line + comment_end + '\n'
		
	return commented_header
	
def _comment_chars_from_ext(ext):
	''' Returns a tuple of the start and end comment chars/strings for the given
	file extension.
	'''
	map = {'py': ('#', ''), 'js': ('//', '')}
	
	try:
		return map[ext]
	except KeyError:
		# Default.
		return ('/*', '*/')

def put_header(header, dir, filter = '*', 
			   comment_start = None, comment_end = None):
	'''	Writes *header* to the top of all files in *dir* matched by *filter*.
	'''
	# Get the list of files.
	files = []
	successes = []
	for i in os.walk(dir):
		for j in i[2]:
			files.append(i[0].replace('\\', '/') + '/' + j)	
	files = fnmatch.filter(files, filter)
	
	if comment_start:
		# If the start comment character/string is specified in the kwargs, 
		# construct the header now and use it for all files.
		ch = _commented_header(
			header,
			comment_start,
			comment_end
		)
		print 'Writing header:\n' + ch + 'To files:\n'
		for file in files:
			with open(file, 'r+') as f:
				cur = f.read()
				f.seek(0)
				f.truncate()
				f.write(ch + '\n' + cur)
			
			print file
	else:
		# Otherwise work out the header for each file based on its type...
		print 'Writing header:\n' + header + '\n(commenting characters will be' +\
			  'determined on a file-by-file basis)\n To files:'
		for file in files:
			# ...here inside the loop.
			(cs, ce) = _comment_chars_from_ext(file.split('.')[-1])
			ch = _commented_header(header, cs, ce)
		
			with open(file, 'r+') as f:
				cur = f.read()
				f.seek(0)
				f.truncate()
				f.write(ch + '\n' + cur)
			
			print file
			
	# Return the list of files to which the header was added.
	return files
			
def drop_lines(num_lines, dir, filter = '*'):
	'''	Removes *num_lines* lines from the top of all files in *dir* matched by
	*filter*.
	'''
	# Get the list of files.
	files = []
	for i in os.walk(dir):
		for j in i[2]:
			files.append(i[0].replace('\\', '/') + '/' + j)	
	files = fnmatch.filter(files, filter)

	for file in files:
		with open(file, 'r+') as f:
			cur = f.readlines()
			f.seek(0)
			f.truncate()
			f.writelines(cur[num_lines:])
		print 'Dropped ' + num_lines + ' lines from ' + file
		
	# Return the list of files from which lines were dropped.
	return files

def test_header(header, dir, filter = '*', 
				comment_start = None, comment_end = None):
	'''	Tests whether the given *header" is found at thetop of all files in
	*dir* matched by *filter*.
	'''
	# Get the list of files.
	files = []
	for i in os.walk(dir):
		for j in i[2]:
			files.append(i[0].replace('\\', '/') + '/' + j)	
	files = fnmatch.filter(files, filter)
	
	# Results.
	passes = []
	fails = []
	
	if comment_start:
		# If the start comment character/string is specified in the kwargs, 
		# construct the header now and use it for all files.
		ch = _commented_header(
			header,
			comment_start,
			comment_end
		)
		print 'Testing for header:\n' + ch
		for file in files:
			with open(file, 'r') as f:
				if f.read(len(ch)) == ch:
					passes.append(file)
				else:
					fails.append(file)
	else:
		# Otherwise work out the header for each file based on its type...
		print 'Testing for header:\n' + header + '\n(commenting characters ' +\
			  'will be determined on a file-by-file basis)'
		for file in files:
			# ...here inside the loop.
			(cs, ce) = _comment_chars_from_ext(file.split('.')[-1])
			ch = _commented_header(header, cs, ce)
		
			with open(file, 'r') as f:
				if f.read(len(ch)) == ch:
					passes.append(file)
				else:
					fails.append(file)
				
	print 'Passed:'
	for f in passes:
		print f
	print 'Failed:'
	for f in fails:
		print f
		
	return passes, fails

if __name__ == '__main__':
	
	if sys.argv[1] == '-drop':
		drop_header(int(sys.argv[2]), sys.argv[3], sys.argv[4])
	elif sys.argv[1] == '-put':
		put_header(open(sys.argv[2]).read(), sys.argv[4], sys.argv[5], sys.argv[3])
	elif sys.argv[1] == '-test':
		test_header(open(sys.argv[2]).read(), sys.argv[4], sys.argv[5], sys.argv[3])
	else:
		put_header(open(sys.argv[1]).read(), sys.argv[3], sys.argv[4], sys.argv[2])