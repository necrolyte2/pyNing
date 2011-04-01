from pyNing import Ning
import re

class NingLinkUp( Ning ):
	forums = []

	def getForums( self, ignoreForums = [ 'Campfire Conversations' ] ):
		page = self.curl( '/forum' )
		forums = re.findall( '<h3><a href="' + self.network + '(/forum/categories/.*?/listForCategory)">(.*?)</a>', page )
		# Parse out all the forums we should ignore
		for forum in forums:
			for ignore in ignoreForums:
				if forum[1].find( ignore ) == -1:
					self.forums.append( forum )
			
		return self.forums

	def getTopicPages( self, pageHtml ):
		m = re.findall( '<li><a class="" href="' + self.network + '(/forum/categories/[a-zA-Z0-9_-]+/listForCategory.categoryId=\d+%3ACategory%3A\d+&amp;page=(\d+))', pageHtml )
		pages = []
		# We don't want to return the first page since it has already been fetched
		for page in m:
			if page[1] != 1:
				# Quick dirty little fix to fix the & symbol
				pages.append( page[0].replace( '&amp;', '&' ) )
		return pages

	def getTopics( self, forum, ignoreTopics = [ 'Template for Posting' ] ):
		# We have to gather the forum list if it hasn't been gathered already
		if not self.forums:
			self.getForums()

		# This will hold the forum page to fetch
		forumPage = ''

		# Search for the forumUrl
		for f in self.forums:
			if f[1] == forum:
				forumPage = f[0]

		# Grab the first page of topics for this forum
		page = self.curl( forumPage )

		# All the pages for this forum
		pages = self.getTopicPages( page )

		# Now add all the additional pages to the first page's html
		for p in pages:
			page += self.curl( p )

		# Will hold our topics
		topics = []

		# Finall the topics on a page
		m = re.findall( '<h3><a href="' + self.network + '(/forum/topics/[a-zA-Z0-9_-]+)" _snid="[0-9]+:Topic:[0-9]+">(.*?)</a></h3>', page )
		for topic in m:
			for ignore in ignoreTopics:
				if topic[1].find( ignore ) == -1:
					topics.append( topic )
		return topics
