## Performance analysis

Analysis tool for performance output generated by w3af. The input for this tool is generated using the [AWS Collector](https://github.com/andresriancho/collector).

## Usage

```console
$ ./wpa ~/performance_info/master/i-e45d5fb5/

Total memory size:
	0:    64.2 MiB
	1:    68.2 MiB
	2:    123.1 MiB
	3:    665.8 MiB

Memory usage summary:
	Total 8364538 objects, 286 types, Total size = 440.4MiB (461765737 bytes)
	Index   Count    %      Size       %   Cum     Max      Kind
	0       2193778  26     181553569  39  39      4194281  str
	1       12519    0      97231956   21  60      12583052 dict
	2       1599439  19     68293428   14  75      304      tuple
	3       3459765  41     62169616   13  88      20       bzrlib._static_tuple_c.StaticTuple
	4       82       0      29372712   6   94      8388724  set
	5       1052573  12     12630876   2   97      12       int
	6       1644     0      4693700    1   98      2351848  list
	7       4038     0      2245128    0   99      556      _LazyGroupCompressFactory

CPU Usage:
	System load average: 1.59, 0.81, 0.75
	Top10 most time consuming functions:
		0:    parse_foo()
		1:    parse_bar()
		...
		9:    do_spam()

HTTP requests:
	Total:         5030
	Average RPM:   61
	Top RPM:	   890
	Lowest RPM:	   49

$
```

The most common usage of this tool looks like this:

```console
# Use the collector to gather some information
$ ./collect config.yml master
$ ./collect config.yml feature/performance-speedup
# In console #1
$ ./wpa ~/performance_info/master/i-e45d5fb5/
# In console #2
$ ./wpa ~/performance_info/feature-performance-speedup/i-f32dafb9/
# User compares performance results for each by putting the two consoles side by side
```

Processing the performance information can take considerable time, be patient when running `wpa`!

## Internals

This software is *tightly coupled* with the output of the [collector](https://github.com/andresriancho/collector) tool, if the `collector` changes its output format, removes one or more of its files, etc. the `wpa` tool will most likely crash or return unusable information.

The information is analyzed by various (independent) plugins which are stored in the `plugins` directory. If at any point you want to add a new analysis plugin, you'll have to create it inside the `plugins` module, import it from `main.py` and finally add it to the list of plugins to run.

The `logging` module can be used by plugins to write any debugging information to the output.
