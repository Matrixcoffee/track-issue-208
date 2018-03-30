import os
import sys

CAFILE = None
CAPATH = None
CONTEXT = None

def eprint(*args, **kwargs):
	kwargs['file'] = sys.stderr
	print(*args, **kwargs)

def setup_socks5():
	s5 = os.environ.get('SOCKS5_SERVER', None)
	if not s5: return

	# Heuristics. Bad example. Wontfix, but don't copy.
	global CAPATH
	CAPATH="/etc/ssl/certs"

	s5s = s5.split(':')
	if len(s5s) != 2:
		eprint("Badly formatted environment variable SOCKS5_SERVER: {!r}".format(s5))
		return

	host = s5s[0]
	port = int(s5s[1])

	import socks
	import socket
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, host, port)
	socket.socket = socks.socksocket

def setup_tls():
	# Ensure at least _something_ is configured.
	# If not, we might not be verifying certificates and
	# thus make insecure connections.

	# Defaults will not work with Python 3.2. If you need it to work there,
	# explicitly set either CAFILE or CAPATH after importing this module.

	global CAFILE, CAPATH, CONTEXT
	if CAFILE is None and CAPATH is None and CONTEXT is None:
		setup_socks5()

	if CAFILE is None and CAPATH is None and CONTEXT is None:
		import ssl
		CONTEXT = ssl.create_default_context()
		# Overkill all the overkill
		CONTEXT.verify_mode = ssl.CERT_REQUIRED

def get_tls_parms():
	# Return a dict suitable for passing to urlopen() as dictionary arguments
	# via **.
	setup_tls()
	parms = {}
	if CAFILE is not None: parms['cafile'] = CAFILE
	if CAPATH is not None: parms['capath'] = CAPATH
	if CONTEXT is not None: parms['context'] = CONTEXT
	return parms
