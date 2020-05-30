from ctypes import *


class example(Union):
	_fields_ = [
	("example_long", c_long),
	("example_int", c_int),
	("example_char", c_char * 8),
	]


value = raw_input("Enter an amount: ")
my_example = example(int(value))
print("Example as a long: %ld" % my_example.example_long)
print("Example as a int: %d" % my_example.example_int)
print("Example as a char: %s" % my_example.example_char)
