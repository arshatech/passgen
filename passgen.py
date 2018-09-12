#!/usr/bin/env python

import os
import re
import sys
from random import choice
from itertools import product
from optparse import OptionParser

class Main:
    def __init__(self):
        try:
	    self.char_set = {'lower':   'abcdefghijklmnopqrstuvwxyz',
	        	     'upper':   'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                             'digit':   '0123456789',
                             'special': '^!$%\&/()=?{[]}+~#-_"\'.: ,;<>|'
			    }
            blue, yellow, green, cyan, red, nc = self.color()
	    parser = self.get_argument(blue, green, nc)
	    self.set_argument(parser, blue, yellow, green, cyan, red, nc)
	except Exception as err:
	    print red + ' [-] Error: %s' % err + nc + '\n'
	    sys.exit()

    def set_argument(self, parser, blue, yellow, green, cyan, red, nc):
        options, args = parser.parse_args()
	if len(sys.argv) == 1:
            print ' [~] By: Arshatech.com'
            print ' [*] Usage: python ' + sys.argv[0] + ' [options]\n'
	    sys.exit()
	end_to = None
	show = options.show
	pattern = options.pattern
	own_pattern = options.own_pattern
	char_length = options.char_length
	number = options.number
	word = options.word
	various = options.various
	replacement = options.replacement
	save_file = options.save_file
	verbose = options.verbose
	self.start(show, end_to, word, pattern, own_pattern , char_length, number, various, replacement, save_file, verbose, blue, yellow, green, cyan, red, nc)

    def start(self, show, end_to, word, pattern, own_pattern , char_length, number, various, replacement, save_file, verbose, blue, yellow, green, cyan, red, nc):
        char_set = self.char_set
	if show:
	    self.usage(show, blue, green, cyan, nc)
	    sys.exit()

	if not save_file and not verbose:
	    verbose = True

	if save_file:
	    self.handle_file(save_file, blue, yellow, red, nc)
	    opened = open(save_file, 'a+')
	else:
	    opened = None

	if pattern:
    	    if not replacement and not char_length:
	        print red + ' [-] Error: The switch \'-p\' must be used with \'-s\' or \'-l\' switches!' + nc
		sys.exit()
	    elif pattern not in char_set.keys() and pattern != 'mix':
		print red + ' [-] Error: The pattern \'%s\' is not valid!' % pattern + nc
		sys.exit()

	if not own_pattern and word:
	    words = self.upper_lower(word)
	    if not number:
		if verbose:
	    	    passage = '\n [+] All \'%s\' possibilities:' % word
		    splitter = self.print_results(passage)
		    print green + passage + nc
		    print green + splitter + nc
    	        for w in words:
		    if save_file:
		        self.save(w, opened)
		    if verbose:
		        print cyan + '\t%s' % w + nc
	    else:
	        try:
		    i = 0
		    if verbose:
			passage = '\n [+] \'%s\' possibilities for \'%s\':' % (number, word)
			splitter = self.print_results(passage)
			print green + passage + nc
			print green + splitter + nc
		    while i < number:
			if save_file:
		    	    self.save(words[i], opened)
			if verbose:
			    print cyan + '\t%s' % words[i] + nc
		        i += 1
		except Exception:
		    pass

	if not number:
	    number = 1

	if own_pattern:
	    i = 0
	    items = self.join_string(own_pattern)
	    customize = self.custumized_pattern(items)
	    if verbose:
		passage = ' [+] Your own pattern:'
		splitter = self.print_results(passage)
		print green + passage + nc
		print green + splitter + nc
            try:
    	        while i < number:
		    password = self.get_char(word, customize, various)
    		    if save_file:
		        self.save(password, opened)
		    if verbose:
		        print cyan + '\t%s' % password + nc
		    i += 1
            except KeyboardInterrupt:
                print '\n' + yellow + ' [*] Exitting...' + nc
                sys.exit()

	if replacement:
	    if '?' not in replacement:
		print red + ' [-] Error: The string %s must have at least one \'?\' letter!' + nc
		sys.exit()
	    elif not pattern:
		print red + ' [-] Error: You must spesify the pattern. use \'-p\' switch!' + nc
		sys.exit()
	    elif pattern:
		i = 0
		if verbose:
		    passage = '\n [+] Replacement pattern:'
		    splitter = self.print_results(passage)
		    print green + passage + nc
		    print green + splitter + nc
		while i < number:
		    password = self.replace_pattern(replacement, pattern)
		    if save_file:
		        self.save(password, opened)
		    if verbose:
			print cyan + '\t%s' % password + nc
		    i += 1
			
	if char_length:
	    if verbose:
		passage = ' [+] Defined pattern:'
		splitter = self.print_results(passage)
		print green + passage + nc
		print green + splitter + nc

	    char_length = char_length.split('-')
	    if len(char_length) == 1:
		start_from = int(char_length[0])
		end_to = start_from
	    elif len(char_length) == 2:
		try:
	    	    start_from = int(char_length[0])
		    end_to = int(char_length[1])
		except Exception as err:
		    print ' [-] Error: %s' % err
		    sys.exit()
	    else:
	        print '\n [-] Error: The parameter \'-l\' is not valid. Must be \'digit-digit\'.'
	        sys.exit()

	    if start_from <= end_to:
	        for index in range(start_from, end_to+1):
		    self.run_generate_pass(number, index, pattern, opened, verbose, cyan, nc)
	    else:
	        for index in reversed(range(end_to, start_from+1)):
	    	    self.run_generate_pass(number, index, pattern, opened, verbose, cyan, nc)
        print green + '\n [+] Finished!' + nc + '\n'

    def handle_file(self, save_file, blue, yellow, red, nc):
        if os.path.exists(save_file):
	    try:
                answer = raw_input(' [*] The file \'%s\' existed! [a: append], [w: write],  [r: remove and quit], [q: quit]? ' % save_file)
	    except KeyboardInterrupt:
		print '\n' + yellow + ' [*] Exitting...' + nc
		sys.exit()
	    if answer == 'a':
		print blue + ' [*] Results are appending to \'%s\'' % save_file + nc
		pass
	    elif answer == 'w':
		os.remove(save_file)
		print blue + ' [*] Results are writing to \'%s\'' % save_file + nc

            elif answer == 'r':
                os.remove(save_file)
                print blue + ' [*] The file \'%s\' is removed!' % save_file + nc
                print blue + ' [*] Exiting...' + nc
                sys.exit()

	    elif answer == 'q':
		print blue + ' [*] Exiting...' + nc
		sys.exit()

	    else:
		print red + ' [-] Error: Invalid choice!' + nc
		sys.exit()

    def save(self, iteration, opened):
	return opened.write(iteration+'\n')

    def print_results(self, passage):
	n = len(passage) - 6
	splitter = ' '*5 + '-'*n
	return splitter

    def run_generate_pass(self, number, index, pattern, save_file, verbose, cyan, nc):
        i = 0
	while i < number:
	    generator = self.generate_pass(index, pattern)
	    if save_file:
	        self.save(generator, save_file)
	    if verbose:
	        print cyan + '\t%s' % generator + nc
	    i += 1

    def replace_pattern(self, replacement, pattern):
	char_set = self.char_set
	chars = list()
	s_chars = list()
	password = list()
	for s in replacement:
	    s_chars.append(s)

	for s in s_chars:
	    if s == '?':
	        index = s_chars.index(s)
		if pattern in char_set.keys():
		    char = char_set[pattern]
		    for c in char:
			chars.append(c)
        	    a_char=choice(chars)
		elif pattern == 'mix':
		    key = choice(char_set.keys())
		    a_char = choice(char_set[key])
		password.append(a_char)
        k = 0
        for i in s_chars:
	    if i == '?':
	        index = s_chars.index(i)
	        del s_chars[index]
	        s_chars.insert(index, password[k])
	        k += 1
	return ''.join(s_chars)

    def join_string(self, lst):
	pat = re.compile(r'%(\d*)([a-zA-Z]+)')
	out = pat.sub(lambda m:int(m.group(1))*m.group(2) if m.group(1) else m.group(2), lst)
	return out

    def upper_lower(self, word):
	return [''.join(x) for x in product(*[{c.upper(), c.lower()} for c in word])]

    def custumized_pattern(self, own_pattern):
        pattern = list()
        o_pat = {'l': 'lower', 'u': 'upper', 'd': 'digit', 's': 'special', '_': 'replacement'}
	try:
	    for char in own_pattern:
		pattern.append(o_pat[char])
	except Exception as err:
	    print red + ' [-] Error: The pattern \'%s\' is not correct!' % own_pattern + nc
	    sys.exit()
	return pattern

    def get_char(self, word, pattern, various):
	char_set = self.char_set
	chars = list()
	password = list()
	for p in pattern:
	    if p == 'replacement':
	        if various:
		    w = self.upper_lower(word)
		    a_char = choice(w)
		else:
		    a_char = word
	    else:
	        a_char = choice(char_set[p])
	    password.append(a_char)
	return ''.join(password)
			
    def generate_pass(self, index, pattern):
        char_set = self.char_set
	chars = list()
	password = list()
	if pattern in char_set.keys():
	    char = char_set[pattern]
	    for c in char:
	        chars.append(c)
	    while len(password) < index:
		a_char=choice(chars)
		password.append(a_char)
	elif pattern == 'mix':
	    while len(password) < index:
	        key = choice(char_set.keys())
		a_char = os.urandom(1)
		if a_char in char_set[key]:
		    if self.check_prev_char(password, char_set[key]):
			continue
		    else:
			password.append(a_char)
	else:
	    print ' [-] Error: Choose the correct method!'
	    sys.exit()
	return ''.join(password)

    def check_prev_char(self, password, current_char_set):
	index = len(password)
	if index == 0:
            return False
	else:
	    prev_char = password[index - 1]
	    if prev_char in current_char_set:
	        return True
	    else:
		return False

    def get_argument(self, blue, green, nc):
        print blue
        parser = OptionParser(usage='usage: %prog [options]')
	parser.add_option('-e', '--example-show', action='store_true', dest='show', default=False,
						help='Showing description and examples of program how to run.')
	parser.add_option('-p', '--pattern', action='store', type='string', dest='pattern', default=None,
						help='Getting pattern of characters in password.\
						      Choices: lower, upper, digit, special, mix')
	parser.add_option('-o', '--own-pattern', action='store', type='string', dest='own_pattern', default=None,
						help='Getting your own pattern of characters in password.')
	parser.add_option('-w', '--word', action='store', type='string', dest='word', default=None,
						help='If used without \'-o\' witch gets the word and print all upper and lower possibilities.\
	        				      If used with \'-o\' switch and \'_\' occurs in string it replace the word and create dictionary.')
	parser.add_option('--various', action='store_true', dest='various', default=False,
						help='If true, it adds various possibilities of given string in dictionary.')
	parser.add_option('-r', '--replacement', action='store', type='string', dest='replacement', default=False,
						help='Getting string and replace some characters with given pattern to replace.')
	parser.add_option('-l', '--length', action='store', type='string', dest='char_length', default=None,
						help='Getting range for generating passwords.')
	parser.add_option('-n', '--number', action='store', type='int', dest='number', default='0',
						help='Number of passwords you want to generate.')
	parser.add_option('-f', '--save-file', action='store', type='string', dest='save_file', default=None,
						help='If you want to save results you can use this option.')
	parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False,
						help='Verbose mode. If you want to see results you can use this option.')
	return parser

    def color(self):
        colors = {'green':'\x1b[1;32m', 'red':'\x1b[1;31m', 'blue':'\x1b[1;34m', 'cyan':'\x1b[1;36m', 'yellow':'\x1b[1;33m', 'no_color':'\x1b[0m'}
        blue = colors.values()[0]
        yellow = colors.values()[1]
        green = colors.values()[2]
        nc = colors.values()[3]
        cyan = colors.values()[4]
        red = colors.values()[5]
        return blue, yellow, green, cyan, red, nc

    def usage(self, show, blue, green, cyan, nc):
	if show:
            print ' [~] By: Arshatech.com'
	    print '     This script is a very useful password generator.\n'
	    print green + ' [*] Supported patterns: [with \'-p\', \'--pattern\']' + blue
	    print '\t1. lower: This choice sets password in lower_case letters.'
	    print '\t2. upper: This choice sets password in  upper_case letters.'
	    print '\t3. digit: This choice sets password in digits.'
	    print '\t4. special: This choice sets password in special characters.'
	    print '\t5. mix: This choice sets password mixture of all patterns.\n'
	    print green + ' [*] Supported signs: [with \'-o\', \'--own-pattern\']' + blue
	    print '\t1. l: Single lower_case character. %l stands for a random single lower_case character.'
	    print '\t2. u: Single upper_case character. %2u stands for two consecutive upper_case characters.'
	    print '\t3. d: Single digit character. %3d stands for three consecutive digits.'
	    print '\t4. s: Single special character. %4s stands for four consecutive special chraracters.\n'
	    print green + ' [*] Usage of word: [\'-w\', \'--word\']' + blue
	    print '\tThis switch has two uses:'
	    print '\t\t1. If use without \'-o\', \'--own-pattern\' it prints possibilities of lower_case and upper_case string.'
	    print '\t\t   Also if use without \'-n\', \'--number\' it prints all possibilities for you.'
	    print '\t\t2. If use with \'-o\', \'--own-pattern\' and \'_\' exists, the word goes instead of \'_\' in your pattern.\n'
	    print green + ' [*] Usage of string: [\'-r\', \'--replacement\']' + blue
            print '\t For example: ?jk?46'
            print '\t\t It trys random characters to placement the \'?\' sign.\n'
            print green + ' [*] Examples:' + cyan
            print '\tpython %s -h' % sys.argv[0]
            print '\tpython %s -e' % sys.argv[0]
            print '\tpython %s -l 6 -p digit -n 5' % sys.argv[0]
            print '\tpython %s -l 6-10 -p mix -n 4' % sys.argv[0]
            print '\tpython %s -o %s -n 4' % (sys.argv[0], '%2l%u%d%2s')
            print '\tpython %s -w test' % sys.argv[0]
            print '\tpython %s -n 5 -o _%s_%s -w test --various' % (sys.argv[0], '%3d', '%2s%l')
            print '\tpython %s -n 10 -o _%s -w 0912 -f output.txt -v' % (sys.argv[0], '%7d')
            print '\tpython %s -n 10 -r "thi? is t?s?" -p upper' % sys.argv[0]
            print '\tpython %s -n 10 -r "thi? is t?s?" -p special -f output.txt' % sys.argv[0]
            print '\tpython %s -n 10 -r "thi? is t?s?" -p mix -f output.txt -v' % sys.argv[0] + nc
            sys.exit()

if __name__ == '__main__':
    Main()
