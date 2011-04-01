#!/usr/bin/env python

import re
import time
import sys
import subprocess
import tempfile

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

	def curl( self, page, curlops = [] ):
		ops = [ '-c', 'cookie', '-b', 'cookie', '-k', '-L', '-s' ] 
		for op in curlops:
			ops.append( op )
		# Insert the actual curl command into the first part of the list
		ops.insert( 0, '/usr/bin/curl' )
		# Build the url to fetch
		url = "%s%s" % (self.network, page)
		# Add the url to the end of the ops
		ops.append( url )
		# Create a temp file to write to
		f = tempfile.TemporaryFile()
		# Run the curl command
		p = subprocess.Popen( ops, stderr = subprocess.STDOUT, stdout = f )
		# Wait for the process to exit
		p.wait()
		# Seek to the beginning of the file
		f.seek(0)
		# Read the contents of what was fetched
		html = f.read()
		f.close()
		return html

	def _login_success( self, page ):
		# If there is a CurrentProfile in the page then you are logged in
		m = re.search( 'CurrentProfile":{"id":"(.*?)"', page )
		if m:
			return True
		else:
			return False

	def login( self, username = None, password = None ):
		if not username:
			username = self.email
		if not password:
			password = self.password
		self._login_success( self.curl( self.SIGN_IN_PAGE ) )
		return self._login_success( self.curl( self.LOG_IN_PAGE, [ '-d', 'emailAddress=' + username, '-d', 'password=' + password ] ) )

"""
ning = {"CurrentApp":{"premium":true,"iconUrl":"http:\/\/api.ning.com\/icons\/appatar\/4072389?default=4072389&width=64&height=64","url":"http:\/\/thelink-up.ning.com","domains":[],"online":true,"privateSource":true,"id":"thelink-up","description":"A non-profit organization connecting injured veterans with various donors willing to offer assistance participating in outdoor activities.","name":"TheLink-Up.org","owner":"0j052jyv9b0am","createdDate":"2009-09-18T19:28:26.461Z","runOwnAds":false,"category":{"military":null,"veteran":null,"wounded":null,"warrior":null,"soldier":null,"purple":null,"heart":null,"hunts":null,"for":null,"heroes":null},"tags":["military","veteran","wounded","warrior","soldier","purple","heart","hunts","for","heroes"]},"CurrentProfile":{"id":"3owaajts97606","profileUrl":"http:\/\/thelink-up.ning.com\/profile\/TygheVallard","location":"Glendive, MT","age":27,"gender":null,"fullName":"Tyghe Vallard","photoUrl":"http:\/\/api.ning.com:80\/files\/lTjyjb6dQpzOhCjon1klad4eRQvMUjMXDH7etdADCyCu1USZajunEeJZlU9p9BYjtFqFzvYES-H0G3*K8uh5PF8TGgaM0Z4j\/SmallTheLinkUpOrg2.jpg?crop=1%3A1","country":"US"},"maxFileUploadSize":7};
"""
