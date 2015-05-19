#!/usr/bin/env python

import sys
import socket
import argparse
import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable()  ## This line enables CGI error reporting

def main():
	parser = argparse.ArgumentParser(description='CGI HTTP server')
	parser.add_argument('-p','--port', help="Server port", nargs='?', default="8000", required=False)
	parser.add_argument("-a",'--addr', help="Server IPv4 address ", nargs='?', default="127.0.0.1", required=False)
	#parser.add_argument("-r",'--root', help="CGI root path", nargs='?', default="/", required=False)
	args = parser.parse_args()

	port = int(args.port)
	ip = args.addr
	#path = args.root
	path = "/"

	#valid ipv4?
	try:
		socket.inet_pton(socket.AF_INET,ip)
	except:
		print("Invalid IPv4 address")
		exit(1)

	server = BaseHTTPServer.HTTPServer
	handler = CGIHTTPServer.CGIHTTPRequestHandler
	server_address = (ip, port)
	handler.cgi_directories = [path]
	httpd = server(server_address, handler)

	print ("Serving on port {} with IPv4 '{}'.\nRoot path is '{}'".format(port, ip, path))
	httpd.serve_forever()

main()
