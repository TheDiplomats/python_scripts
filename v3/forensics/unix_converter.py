from __future__ import print_function
import datetime
import sys

if sys.version_info[0] == 3:
	get_input = input
elif sys.version_info[0] == 2:
	get_input = raw_input
else:
	raise NotImplementedError('Unsuported version of Python used.')
	
__authors__ = ['Chapin Bruce', 'Preston Miller', 'Bakari Levy']
__date__ = 20200612
__description__ = """ Convert Unix formatted timestamps (seconds since
Epoch [1970-01-01 00:00:00]) to human readable."""


def unix_converter(timestamp):
	date_ts = datetime.datetime.utcfromtimestamp(timestamp)
	return date_ts.strftime('%m/%d/%Y %I:%M:%S %p')


def main():
	unix_ts = int(get_input('Unix Timestamp to convert:\n>> '))
	print(unix_converter(unix_ts))

if __name__ == '__main__':
	main()
