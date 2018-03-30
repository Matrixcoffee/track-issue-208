#!/usr/bin/env python3

# https://developer.github.com/v3/
# https://developer.github.com/v3/issues/
# https://docs.python.org/release/3.2/library/json.html
# https://docs.python.org/release/3.2/library/urllib.request.html

import argparse
import codecs
import difflib
import json
import os
import subprocess
import sys
import time
import urllib.request

import tls_setup

def eprint(*args, **kwargs):
	kwargs['file'] = sys.stderr
	print(*args, **kwargs)

def _noprint(*args, **kwargs):
	pass

parser = argparse.ArgumentParser(description="Download issue 208. Commit if changed.")
parser.add_argument("-c", "--cached", action='store_true', default=False, help="Use cached data instead of downloading. For debugging.")
parser.add_argument("-d", "--debug", action='store_const', const=eprint, default=_noprint, help="Enable debug messages.")
options = parser.parse_args()

dprint = options.debug

def exists(path):
	return os.access(path, os.F_OK)

class git:
	@staticmethod
	def checkout(what):
		return subprocess.call(("git", "checkout", what))

	@staticmethod
	def add(what):
		return subprocess.call(("git", "add", what))

	@staticmethod
	def commit(msg=""):
		return subprocess.call(("git", "commit", "-m", msg))

def skip_http_headers(fs):
	nskipped = 0
	while len(fs.readline()) > 1: nskipped += 1
	dprint("Skipped:", nskipped)
	return nskipped

def download_issue():
	if options.cached:
		fs = open("208.json", 'r')
		#skip_http_headers(fs)
	else:
		rawfs = urllib.request.urlopen("https://api.github.com/repos/matrix-org/matrix-appservice-irc/issues/208", **tls_setup.get_tls_parms())
		fs=codecs.getreader(rawfs.headers.get_content_charset())(rawfs)

	with fs:
		rawjson = fs.read()

	dprint(repr(rawjson))
	dprint("-" * 79)

	with open("208.json.new", 'w') as f:
		f.write(rawjson)

	issue = json.loads(rawjson)

	dprint(repr(issue))
	dprint("-" * 79)

	dprint(repr(issue['body']))

	with open("208.md.new", 'w') as f:
		f.write("\n".join(issue['body'].split("\r\n")))
		f.write("\n")

def compare_download():
	with open("208.md") as f:
		seq1 = f.read()

	with open("208.md.new") as f:
		seq2 = f.read()

	sm = difflib.SequenceMatcher()
	sm.set_seq1(seq1)
	sm.set_seq2(seq2)

	dprint("rqr:", sm.real_quick_ratio())
	dprint("qr:", sm.quick_ratio())
	r = sm.ratio()
	dprint("r:", r)

	return sm.ratio()

def main():
	download_issue()

	r = git.checkout("208.md")
	if r != 0: return
	d = compare_download()
	if d < 0.3: return
	if d > 0.9999999999: return
	os.rename("208.md.new", "208.md")
	os.rename("208.json.new", "208.json")
	r = git.add("208.md")
	if r != 0: return
	r = git.commit(time.strftime("Commit new change detected on %c", time.gmtime()))
	if r != 0: return

if __name__ == '__main__':
	main()
