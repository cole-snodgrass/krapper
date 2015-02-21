#!/usr/bin/env python
import argparse
import json
import collections
import random
import plugins.columns

class KrapperConfigParser(object):
	column_mapping = {		
		'name' : plugins.columns.NameKrapperColumn,
		'name_first' : plugins.columns.NameFirstKrapperColumn,
		'name_last' : plugins.columns.NameLastKrapperColumn,
		'range_int' : plugins.columns.IntRangeKrapperColumn,
		'enum' : plugins.columns.EnumKrapperColumn,
		'text' : plugins.columns.TextKrapperColumn
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
		try:
			for k in data:
				# convert the OrderedDict back to a normal dict, we don't care about order anymore
				if 'options' in data[k]:
					columns[k] = KrapperConfigParser.column_mapping[data[k]['type']](k, **dict(data[k]['options']))
				else:
					columns[k] = KrapperConfigParser.column_mapping[data[k]['type']](k)
		except KeyError:
			print('no registered column plugin for "{}", ignoring this column'.format(data[k]['type']))
		except TypeError:
			print('missing required options for plugin "{}", ignoring this column'.format(data[k]['type']))

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