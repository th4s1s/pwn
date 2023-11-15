import subprocess
import os
import time
import sys


def run(proc):
	check = False
	bb = []
	c = ["je", "jmp", "jne", "jz", "jnz", "call"]

	output = subprocess.check_output(["objdump", "-s", proc]).decode("utf-8").split("\n")
	for line in output:
		if "preinit_array" in line:
			check = True
			break

	output = subprocess.check_output(["objdump", "-d", proc]).decode("utf-8").split("\n")
	for line in output:
		if ">:" in line or "Disassembly of section" in line or "file format" in line:
			continue

		if "int3" in line:
			check = True

		for _ in c:
			if _ in line:
				bb.append("0x" + line.split(":")[0].strip())
				break

	f = open("./tmp/patches.txt", "w")
	if check:
		f.write("@0xc0fec0fe\n")
	else:
		f.write("@" + hex(len(bb)) + "\n")

	for b in bb:
		f.write(b + "\n")

	f.close()

if __name__ == "__main__":
	run(sys.argv[1])
