#!/usr/bin/env python

import re
import time
import sys
import subprocess

class Ning:
	SIGN_IN_PAGE = '/main/authorization/signIn'
	LOG_IN_PAGE = '/main/authorization/doSignIn'

	# Ning Email
	# Ning Password
	# Ning Network Url
	def __init__( self, email, password, networkUrl ):
		# This will be our post data to log in
		self.email = email
		self.password = password
		self.network = networkUrl

		self.sign_in_url = "%s%s" % (self.network, self.SIGN_IN_PAGE)
		self.log_in_url = "%s%s" % (self.network, self.LOG_IN_PAGE)

	def curl( self, url, curlops, fileName = 'tmp.html' ):
		curlops.insert( 0, '/usr/bin/curl' )
		curlops.append( url )
		with open( fileName, 'w' ) as f:
			subprocess.call( curlops, stdout = f )

	def login( self, username = None, password = None ):
		if not username:
			username = self.email
		if not password:
			password = self.password
		self.curl( self.sign_in_url , [ '-c', 'cookie', '-k', '-L', '-s' ] )
		self.curl( self.log_in_url, [ '-b', 'cookie', '-k', '-L', '-s', '-d', 'emailAddress=' + username, '-d', 'password=' + password ], 'loggedin.html' )
