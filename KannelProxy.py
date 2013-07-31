from twisted.web import server, resource
from twisted.internet import reactor
from twisted.python.util import println
from twisted.web.client import reactor as creact, getPage
import configobj
import uuid
import urllib
import urllib2

class KannelProxy(resource.Resource):
	isLeaf = True
	numberRequests = uuid.uuid1()
	seq = 0

	def __init__(self):
		print "Welcome CCS Kannel proxy service v0.1 ..\nLoading app.conf................."
		self.registeredSenders = {}
		self.appConfig = configobj.ConfigObj("app.conf")
		for x in self.appConfig :
		          self.registeredSenders[x] = self.appConfig[x]['registered-senders'].split(';')
		print self.registeredSenders
		print "Done. "

	def __checkSender(self, sender, smsc):
		return self.appConfig[smsc[8:]]['fake-sender'] if self.appConfig.has_key(smsc[8:]) and  sender not in self.registeredSenders[smsc[8:]]  else sender

	def Send(self, url):
			print "[" + str(self.seq) + "] : " + url
			getPage(url).addCallbacks(callback=lambda value:(println(value)),errback=lambda error:(println("an error occurred", error)))
	
	def _fixDLR(self, smsc):
		pass

	def render_GET(self, request):
		self.seq += 1
		self.numberRequests = uuid.uuid1()
		request.setHeader("content-type", "text/plain")
		kannel_sendsms_port = request.path[1:]
		url = "http://localhost:" + kannel_sendsms_port + "/cgi-bin/sendsms?username=nemra1&password=koko88&smsc=" + "%s" % (request.args['smsc'][0][8:] if len(request.args['smsc'][0]) > 7 and request.args['smsc'][0][0:7] ==  "SNCheck" else request.args['smsc'][0]) + "&from=" + urllib.quote(self.__checkSender(request.args['from'][0], request.args['smsc'][0])) + "&to=" + urllib.quote(request.args['to'][0]) + "&text=" + urllib.quote(request.args['text'][0]) + "&coding=" + request.args['coding'][0] + "&dlr-mask=7&dlr-url=" + urllib2.quote(request.args['dlr-url'][0])  #http%3A%2F%2Flocalhost%3A8082%2Fdlr%3Fusername%3Dnemra1%26password%3Dkoko88"
		self.Send(url)
		return "Sent." 

reactor.listenTCP(8080, server.Site(KannelProxy()))
reactor.run()
