#!/usr/bin/env python
import sys

#Map information
runtime = dict()
energy = dict()
count = dict()
#Addressed by
#Benchmark name
#Other
#Self
#CPU Freq

#Loop through every line in the file
f = open(sys.argv[1], 'r')

benchmark = ""
other = -1
self = -1
cpufreq = -1
benchmark_names = []

for line in f:
	#If this line is a file name style
	if( line.find("cpufreq") != -1 and line.find("others") != -1 and line.find("self") != -1 ):
		#Split on underscore
		toks = line.split('_')
		for t in toks:
			if(t.find("cpufreq") != -1):
				t = t.replace("cpufreq","")
				cpufreq = float(t)
			elif(t.find("others") != -1):
				t = t.replace("others","")
				other = int(t)
			elif(t.find("self") != -1):
				t = t.replace("self","")
				self=int(t)
			else:
				benchmark = t
				if( (benchmark in benchmark_names) == False):
					benchmark_names.append(t)
		
	elif( line.find("Energy (J): ") != -1):
		line = line.replace("Energy (J): ","")
		energy[benchmark+str(other)+str(self)+str(cpufreq)] = float(line)
	
	elif( line.find("Runtime (s): ") != -1):
		line = line.replace("Runtime (s): ","")
		runtime[benchmark+str(other)+str(self)+str(cpufreq)] = float(line)
		
	elif( line.find("Average count: ") != -1):
		line = line.replace("Average count: ","")
		count[benchmark+str(other)+str(self)+str(cpufreq)] = float(line)

#Print the results
def info_print(d,dict_name):
	ret = ""
	#For each benchmark name
	for b in benchmark_names:
		#Start with dict name
		ret = ret + dict_name + '\t' + b + '\t'
		#First print things with  0 0 priorities
		_other = 0
		_self = 0
		for _cpufreq in [3.3,2.4,1.6]:
			key = b+str(_other)+str(_self)+str(_cpufreq)
			if(key in d):
				ret = ret + str(d[key]) + '\t'
			else:
				ret = ret + "NA" + '\t'

		#Then print things with  19 0 priorities
		_other = 19
		_self = 0
		for _cpufreq in [3.3,2.4,1.6]:
			key = b+str(_other)+str(_self)+str(_cpufreq)
			if(key in d):
				ret = ret + str(d[key]) + '\t'
			else:
				ret = ret + "NA" + '\t'

		#Then print things with  0 -20 priorities
		_other = 0
		_self = -20
		for _cpufreq in [3.3,2.4,1.6]:
			key = b+str(_other)+str(_self)+str(_cpufreq)
			if(key in d):
				ret = ret + str(d[key]) + '\t'
			else:
				ret = ret + "NA" + '\t'

		#Then print things with  19 -20 priorities
		_other = 19
		_self = -20
		for _cpufreq in [3.3,2.4,1.6]:
			key = b+str(_other)+str(_self)+str(_cpufreq)
			if(key in d):
				ret = ret + str(d[key]) + '\t'
			else:
				ret = ret + "NA" + '\t'
		
		ret = ret + '\n'
		
	return ret
	
	
#print the three dictionaries
print info_print(energy,"Energy:")
print info_print(runtime,"Run Time:")
print info_print(count,"Count:")
	
	
	
	
	
	
	
