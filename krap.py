#!/usr/bin/env python
import argparse
import json
import collections
import random
import plugins.fields

class KrapperConfigParser(object):
	field_mapping = {		
		'name' : plugins.fields.NameKrapperField,
		'name_first' : plugins.fields.NameFirstKrapperField,
		'name_last' : plugins.fields.NameLastKrapperField,
		'range_int' : plugins.fields.IntRangeKrapperField,
		'enum' : plugins.fields.EnumKrapperField,
		'text' : plugins.fields.TextKrapperField,
		'regex' : plugins.fields.RegexKrapperField
	}

	@staticmethod
	def parse(filename):
		try:
			with open(filename) as config:
				# need to set the object_pairs_hook to ensure order is maintained
				data = json.load(config, object_pairs_hook=collections.OrderedDict)
		except IOError:
			print('no configuration "{}" found'.format(filename))
			
		fields = collections.OrderedDict()
		try:
			for k in data:
				# convert the OrderedDict back to a normal dict, we don't care about order anymore
				if 'options' in data[k]:
					fields[k] = KrapperConfigParser.field_mapping[data[k]['type']](k, **dict(data[k]['options']))
				else:
					fields[k] = KrapperConfigParser.field_mapping[data[k]['type']](k)
		except KeyError:
			print('no registered field plugin for "{}", ignoring this field'.format(data[k]['type']))
		except TypeError:
			print('missing required options for plugin "{}", ignoring this field'.format(data[k]['type']))

		return KrapperConfig(fields)


class KrapperConfig(object):
	def __init__(self, fields):
		self._fields = fields
				
	@property
	def fields(self):		
		return self._fields

class Krapper(object):
	def __init__(self, config, num_records):
		self.config = config
		self.num_records = num_records
		
	def run(self):
		fields = self.config.fields
		for n in range(0, self.num_records):
			record = []
			for c in self.config.fields:
				record.append('"{}":"{}"'.format(c, fields[c].value))
			print('{' + ', '.join(record) + '}')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='data crapper with a k, because k\'s are cool?')
	parser.add_argument('-c', '--config', required=True, help='configuration file')
	parser.add_argument('-n', '--number', type=int, default=10, help='number of records to create')

	args = parser.parse_args()

	krapper = Krapper(KrapperConfigParser.parse(args.config), args.number)
	krapper.run()