krapper
=======

An easy to use data generation script.  Requires a trivial amount of configuration and will crap out a ton of data.

There are a handful of websites that will generate fake data.  Most of them require you to pay money if you want to generate more than 100 or 1,000 records.  I don't want to pay money to have a website just to generate my fake data, and you probably don't want to either.

<b>Still a WIP, more documentation coming soon.</b>
what's coming next?
-------------------
* support for additional output types - csv
* customizable output format - record delimiter, wrapper support
* support for additional field types

example
-------
Example configuration script
```json
# config.json
{
  "fields" : {
    "name" : { "type" : "name", "options" : { "format" : "{last}, {first}" } },
    "age" : { "type" : "range_int", "options" : { "lower_bound" : 18, "upper_bound" : 40 } },
    "gender" : { "type" : "enum", "options" : { "values" : "Male|Female" } },
    "phone" : { "type" : "regex", "options" : { "pattern" : "({d}{d}{d})-{d}{d}{d}-{d}{d}{d}{d}" } }
  }
}
```
Example output
```
$ ./krapper.py --config config.json -n 1
{"name":"Heath, Aubrie", "age":"27", "gender":"Female", "phone":"(499)-498-3029"}

$ ./krapper.py --config config.json -n 10
{"name":"Frazier, Kelsey", "age":"27", "gender":"Female", "phone":"(511)-818-4740"}
{"name":"Perez, Makhi", "age":"34", "gender":"Male", "phone":"(258)-505-2931"}
{"name":"McCormack, Rebecca", "age":"31", "gender":"Female", "phone":"(344)-190-9616"}
{"name":"Phillips, Ingrid", "age":"39", "gender":"Female", "phone":"(387)-047-5360"}
{"name":"Pugh, Melvin", "age":"36", "gender":"Female", "phone":"(118)-709-5514"}
{"name":"English, Holly", "age":"29", "gender":"Female", "phone":"(909)-789-9931"}
{"name":"O'Leary, Isis", "age":"36", "gender":"Male", "phone":"(639)-820-8063"}
{"name":"Harris, Simon", "age":"20", "gender":"Male", "phone":"(229)-361-1569"}
{"name":"O'Connor, Noe", "age":"27", "gender":"Female", "phone":"(790)-413-4575"}
{"name":"Graham, Raiden", "age":"38", "gender":"Female", "phone":"(489)-609-7596"}
```

help
----
```
$ ./krapper.py -h
usage: krapper.py [-h] -c CONFIG [-n NUMBER] [-o {json}]

feed it a little information, and it can crap out a ton of data

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        configuration file
  -n NUMBER, --number NUMBER
                        number of records to create
  -o {json}, --output-type {json}
                        format of records
```
