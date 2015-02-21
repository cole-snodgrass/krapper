#!/usr/bin/env python
import argparse
import json
import collections
import random

class KrapperConfigColumn(object):
	def __init__(self, name):
		self._name = name

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		self._name = value

	def parse_data(self, data_files):
		data = []
		for data_file in data_files:
			with open('data/{}'.format(data_file)) as source:
				data += source.read().splitlines()
		return data


class NameKrapperConfigColumn(KrapperConfigColumn):
	data_files = ['name-first-male.txt', 'name-first-female.txt']

	def __init__(self, name):
		super(NameKrapperConfigColumn, self).__init__(name)
		self.data = super(NameKrapperConfigColumn, self).parse_data(self.data_files)

	
	@property
	def value(self):
		return random.choice(self.data)
		return random.choice(['Cole', 'Jesse', 'Nathan', 'Don'])


class NumericRangeKrapperConfigColumn(KrapperConfigColumn):
	def __init__(self, name, lower_bound, upper_bound):
		super(NumericRangeKrapperConfigColumn, self).__init__(name)
		self.lower_bound = lower_bound
		self.upper_bound = upper_bound

	@property
	def value(self):
		return random.randint(self.lower_bound, self.upper_bound)


class KrapperConfigParser(object):
	column_mapping = {
		'name' : NameKrapperConfigColumn,
		'numeric_range' : NumericRangeKrapperConfigColumn
	}

	@staticmethod
	def parse(filename):
		try:
			with open(filename) as config:
				# need to set the object_pairs_hook to ensure order is maintained
				data = json.load(config, object_pairs_hook=collections.OrderedDict)
		except IOError:
			print('no configuration "{}" found'.format(filename))
			
		columns = collections.OrderedDict()
		for k in data:
			# convert the OrderedDict back to a normal dict, we don't care about order anymore
			if 'options' in data[k]:
				columns[k] = KrapperConfigParser.column_mapping[data[k]['type']](k, **dict(data[k]['options']))
			else:
				columns[k] = KrapperConfigParser.column_mapping[data[k]['type']](k)
			#columns[k] = KrapperConfigColumn(k, **dict(data[k]))

		return KrapperConfig(columns)


class KrapperConfig(object):
	def __init__(self, columns):
		self._columns = columns
				
	@property
	def columns(self):		
		return self._columns

class Krapper(object):
	def __init__(self, config, num_records):
		self.config = config
		self.num_records = num_records
		
	def run(self):
		columns = self.config.columns
		for n in range(0, self.num_records):
			record = []
			for c in self.config.columns:
				record.append('"{}":"{}"'.format(c, columns[c].value))
			print('{' + ', '.join(record) + '}')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='data crapper with a k, because k\'s are cool')
	parser.add_argument('-c', '--config', required=True, help='configuration file')
	parser.add_argument('-n', '--number', type=int, default=10, help='number of records to create')

	args = parser.parse_args()

	krapper = Krapper(KrapperConfigParser.parse(args.config), args.number)
	krapper.run()