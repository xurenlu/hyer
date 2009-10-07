# rules monster
# hold on all rules ,to decide if an url can be fetched
from robotparser import RobotFileParser
import urlparse
class rules_monster:
	'''rules monster
	hold on all rules ,to decide if an url can be fetched'''
	def __init__(self,agent='Mozilla/Firefox 3.1'):
		''' '''
		self.rules={}
		self.agent=agent
	def can_fetch(self,url):
		host,path=urlparse.urlparse(url)[1:3]
		if	(self.rules.has_key(host)):
			return self.rules[host].can_fetch(self.agent,url)
		else:
			rp=RobotFileParser()
			robot_url="http://"+host+"/robots.txt"
			rp.set_url(robot_url)
			rp.read()
			self.rules[host]=rp
			return rp.can_fetch(self.agent,url)	
