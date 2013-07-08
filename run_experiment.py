#!/usr/bin/env python
from subprocess import call #For making shell command calls
import subprocess #for calling commands with file redirection
import os
import time
import sys

#Open the file of benchmark names
f = open("../phoronix_benchmark_names", 'r')

nice_all_file_path="../nice_all/nice_all"
power_virus_path="./power_virus"
timed_phoronix_no_prompt_cmd=[]
timed_phoronix_no_prompt_cmd.append("/usr/bin/time -o")
timed_phoronix_no_prompt_cmd.append("/usr/bin/phoronix-test-suite")
timed_phoronix_no_prompt_cmd.append("batch-run")
#Note: first need to run phoronix-test-suite batch-setup and say no prompt for save and run all options
#DO THIS AS ROOT

#Placeholder for power_virus processes
power_viruses=[]

#For each benchmark
for benchmark in f:
	#Benchmark can be normal or high priority
	for benchmark_nice_val in [-20, 0]:
		#Others can be normal or low priority
		for others_nice_val in [19, 0]:
			#Loop through each cpu freq
			for cpufreq in [3.3,2.4,1.6]:
				benchmark = benchmark.replace('\n','')
				#Get just name part of benchmark name
				benchmark_name = benchmark.replace("pts/","");
				
				#Change all CPUs to specified frequency
				for cpu_index in [0,1,2,3]:
					cmd=[]
					cmd.append("cpufreq-set")
					cmd.append("-c")
					cmd.append(str(cpu_index))
					cmd.append("-g")
					cmd.append("userspace")
					call(cmd)
					cmd=[]
					cmd.append("cpufreq-set")
					cmd.append("-c")
					cmd.append(str(cpu_index))
					cmd.append("-f")
					cmd.append(str(cpufreq)+"GHz")
					call(cmd)
					
				#Launch 4 other power_virus programs
				#Benchmark must force other programs aside to get cpu time
				power_viruses=[]
				for i in [0,1,2,3]:
					cmd=[]
					cmd.append(power_virus_path)
					power_viruses.append(subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE))
				
				#Nice others to specified value
				cmd=[]
				cmd.append(nice_all_file_path)
				cmd.append(str(others_nice_val))
				call(cmd)
				
				#Start running the benchmark
				pid = os.fork()
				#Write this time info to file
				benchmark_output_filename = benchmark_name + "_cpufreq" + str(cpufreq) +  "_others" + str(others_nice_val) + "_self" + str(benchmark_nice_val)
				if(pid ==0):
					#Child
					#Wait a second to let parent do nicing (yes, non deterministic, I know)
					time.sleep(5)
					#Exec the benchmark
					benchmark_args=[]
					benchmark_args.append("/usr/local/bin/likwid-powermeter")				
					benchmark_args.append("/usr/bin/phoronix-test-suite")
					benchmark_args.append("batch-run")
					benchmark_args.append(benchmark)
					#Open the output file
					outfile = os.open(benchmark_output_filename,os.O_WRONLY|os.O_CREAT)
					os.close(1) 
					os.dup(outfile) 
					os.close(2) 
					os.dup(outfile) 
					os.close(outfile)
					os.execv(benchmark_args[0], benchmark_args)
				else:
					#Parent
					#Immediately nice the benchmark process
					#This benchmark process spawns other processes that inherit the nice value - good :-)
					cmd = []
					cmd.append("renice")
					#First arg should be nice value
					cmd.append(str(benchmark_nice_val))
					cmd.append("-p")
					cmd.append(str(pid))
					call(cmd)
					
					#Now wait for that benchmark to finish
					print "Waiting on " + benchmark_output_filename
					os.waitpid(pid,0)
					
					#Kill the 4 power viruses
					#Get their output
					cmd=[]
					cmd.append("killall")
					cmd.append("-SIGINT")
					cmd.append("power_virus")
					call(cmd)
					output = power_viruses[0].stdout.read()
					output = output + power_viruses[1].stdout.read()
					output = output + power_viruses[2].stdout.read()
					output = output + power_viruses[3].stdout.read()
					#Append the kill info to the file
					with open(benchmark_output_filename, "a") as myfile:
						myfile.write(output)
					
					print "Finished: " + benchmark_output_filename
					#Somehow dev null is chmoded wrong in one of the benchmarks...fix it here
					cmd = []
					cmd.append("chmod")
					cmd.append("777")
					cmd.append("/dev/null")
					call(cmd)
