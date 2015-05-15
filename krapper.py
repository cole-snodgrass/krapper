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
	def parse(args):
		fields = KrapperConfigParser.parse_config(args.config)
		num_records = args.number
		output_type = args.output_type

		return KrapperConfig(fields, num_records, output_type)

	@staticmethod
	def parse_config(filename):
		try:
			with open(args.config) as config:
				# need to set the object_pairs_hook to ensure order is maintained
				data = json.load(config, object_pairs_hook=collections.OrderedDict)
		except IOError:
			print('no configuration "{}" found'.format(filename))

		if 'fields' in data:
			fields = KrapperConfigParser.parse_fields(data['fields'])			
		else:
			print('no fields defined in configuration "{}"'.format(filename))

		# TODO fix NoneType AttributeError here
		return fields

	@staticmethod
	def parse_fields(config_fields):
		fields = collections.OrderedDict()

		for name, field in config_fields.iteritems():
			try:
				# convert the OrderedDict back to a normal dict, we don't care about order anymore
				if 'options' in field:
					fields[name] = KrapperConfigParser.field_mapping[field['type']](name, **dict(field['options']))
				else:
					fields[name] = KrapperConfigParser.field_mapping[field['type']](name)
			except KeyError:
				print('no registered field plugin for "{}", ignoring this field'.format(field['type']))
			except TypeError:
				print('missing required options for plugin "{}", ignoring this field'.format(field['type']))

		return fields


class KrapperConfig(object):
	def __init__(self, fields, num_records, output_type):
		self._fields = fields
		self._num_records = num_records
		self._output_type = output_type
		# TODO read this in from the configuration
		self._output_empty_fields = True
				
	@property
	def fields(self):		
		return self._fields

	@property
	def num_records(self):
		return self._num_records

	@property
	def output_type(self):
		return self._output_type

	@property 
	def output_empty_fields(self):
		return self._output_empty_fields

class Krapper(object):
	def __init__(self, config):
		self.config = config
		
	def run(self):
		fields = self.config.fields
		for n in range(0, self.config.num_records):
			record = []
			for name, field in fields.iteritems():
				if field.rate == 100 or field.rate >= random.randint(1, 100):
					record.append('"{}":"{}"'.format(name, field.value))
				elif self.config.output_empty_fields: 
					record.append('"{}":""'.format(name))
			print('{' + ', '.join(record) + '}')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='feed it a little information, receive a crap ton of data in return')
	parser.add_argument('-c', '--config', required=True, help='configuration file')
	parser.add_argument('-n', '--number', type=int, default=10, help='number of records to create')
	parser.add_argument('-o', '--output-type', default='json', choices=['json'], help='format of records')

	args = parser.parse_args()

	Krapper(KrapperConfigParser.parse(args)).run()
