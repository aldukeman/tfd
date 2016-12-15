#! /usr/bin/env python
import subprocess
import sys
import shutil
import os
import time

def main():
	def run(*args, **kwargs):
		input = kwargs.pop("input", None)
		output = kwargs.pop("output", None)
		assert not kwargs
		redirections = {}
		if input:
			redirections["stdin"] = open(input)
		if output:
			redirections["stdout"] = open(output, "w")
		print args, redirections
		subprocess.check_call(sum([arg.split("+") for arg in args],[]), **redirections)
		p = subprocess.Popen(sum([arg.split("+") for arg in args],[]), **redirections)

	config, domain, problem, result_name, timing_name = sys.argv[1:]
	memory = 0
	start = time.time()

	root = os.environ['HOME'] + "/dev/tfd/downward/"

	# run translator
	run(root + "translate/translate.py", domain, problem)

	# run preprocessing
	run(root + "preprocess/preprocess", input="output.sas")

	# run search
	run(root + "search/search", config, "p", result_name, "F", timing_name, input="output")

	end = time.time()

	with open(timing_name, 'a') as file:
		file.write("," + str(int((end - start) * 1000)))


if __name__ == "__main__":
    main()
