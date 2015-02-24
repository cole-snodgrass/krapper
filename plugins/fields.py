import random

class KrapperField(object):
	def __init__(self, name):
		self._name = name

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		self._name = value

	@property
	def column_type(self):
		return self._column_type

	def parse_data(self, data_files):
		data = []
		for data_file in data_files:
			with open('data/{}'.format(data_file)) as source:
				data += source.read().splitlines()
		return data


# http://www.regular-expressions.info/posixbrackets.html
# [:digit:] = 0-9
# [:lower:] = a-z
# [:upper:] = A-Z
# [:xdigit:] = A-Fa-f0-9
# [:alnum:] = a-zA-Z0-9
# [:alpha:] = a-zA-Z
# [:punct:] = !"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~
#
class RegexKrapperField(KrapperField):
	column_type = 'regex'
	
	# digit
	d = '0123456789'
	# digit, no zero
	d1 = '123456789'
	# character
	c = 'abcdefghijklmnopqrstuvwxyz'
	# CHARACTER
	C = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	# hex
	x = 'abcdef' + d
	# HEX
	X = 'ABCDEF' + d
	# alphanumeric
	an = c + C + d 
	# alpha
	a = c + C
	# punctuation
	p = '!"#$%&\'()*+,\-./:;<=>?@[\]^_`{|}~'

	mapping = {
		'{d}' : d,
		'{d1}' : d1,
		'{c}' : c,
		'{C}' : C,
		'{x}' : x,
		'{X}' : X,
		'{an}' : an,
		'{a}' : a,
		'{p}' : p
	}

	def __init__(self, name, pattern):
		super(RegexKrapperField, self).__init__(name)
		self.pattern = pattern
		import re
		self.regex = re.compile('({})'.format("|".join(map(re.escape, self.mapping.keys()))))

	@property
	def value(self):
		return self.regex.sub(lambda mo: random.choice(self.mapping[mo.string[mo.start():mo.end()]]), self.pattern)
		#return '{}{}'.format(random.choice(self.alnum), random.choice(self.punct))

class EnumKrapperField(KrapperField):
	column_type = 'enum'

	def __init__(self, name, values, delimiter='|'):
		super(EnumKrapperField, self).__init__(name)
		if isinstance(values, list):
			self.values = values
		else:
			self.values = values.split(delimiter)		

	@property
	def value(self):
		return random.choice(self.values)

class TextKrapperField(KrapperField):
	column_type = 'text'
	data_file = ['text.txt']

	def __init__(self, name, lower_bound, upper_bound):
		super(TextKrapperField, self).__init__(name)
		self.lower_bound = lower_bound
		self.upper_bound = upper_bound
		self.data = super(TextKrapperField, self).parse_data(self.data_file)

	@property
	def value(self):
		num_words = random.randint(self.lower_bound, self.upper_bound)
		words = []
		for i in range(0, num_words):
			words.append(random.choice(self.data))
		return ' '.join(words)


class NameKrapperField(KrapperField):
	column_type = 'name'
	data_files_first = ['name-first-male.txt', 'name-first-female.txt']
	data_files_last = ['name-last.txt']
	
	def __init__(self, name, format='{first} {last}'):
		super(NameKrapperField, self).__init__(name)
		self.format = format
		self.data_first = super(NameKrapperField, self).parse_data(self.data_files_first)
		self.data_last = super(NameKrapperField, self).parse_data(self.data_files_last)

	@property
	def value(self):
		return self.format.format(first=random.choice(self.data_first), last=random.choice(self.data_last))

class NameFirstKrapperField(KrapperField):
	column_type = 'name_first'
	data_files = ['name-first-male.txt', 'name-first-female.txt']
	
	def __init__(self, name):
		super(NameFirstKrapperField, self).__init__(name)
		self.data = super(NameFirstKrapperField, self).parse_data(self.data_files)

	@property
	def value(self):
		return random.choice(self.data)

class NameLastKrapperField(KrapperField):
	column_type = 'name_last'
	data_files = ['name-last.txt']
	
	def __init__(self, name):
		super(NameLastKrapperField, self).__init__(name)
		self.data = super(NameLastKrapperField, self).parse_data(self.data_files)

	@property
	def value(self):
		return random.choice(self.data)


class IntRangeKrapperField(KrapperField):
	column_type = 'range_int'

	def __init__(self, name, lower_bound, upper_bound):
		super(IntRangeKrapperField, self).__init__(name)
		self.lower_bound = lower_bound
		self.upper_bound = upper_bound

	@property
	def value(self):
		return random.randint(self.lower_bound, self.upper_bound)