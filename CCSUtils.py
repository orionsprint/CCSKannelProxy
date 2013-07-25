#!/usr/bin/python

class Backup(object):
	def _checkConfig(self,logFile):
		raise NotImplementedError

	def Exec(self):
		raise NotImplementedError

	def sendEmail(self):
		raise NotImplementedError

def send_mail(self, send_from, send_to, subject, text, files=[], server="localhost"):
    assert type(send_to)==list
    assert type(files)==list
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach( MIMEText(text) )
    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)
    smtp = smtplib.SMTP(server).starttls()
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


class SimpleLogger :
	DEBUG =  0; WARNING = 10; ERROR = 100; 

	def setup(self, bt = WARNING, file = None):
		self.bootstrap = bt
		from os.path import isfile
		if file is None:
			from sys import stderr
			self.fd = stderr
		else:
			self.fd = open(file)

	def append(self, msg, level = 0):
		if level >= self.bootstrap :
			from datetime import datetime
			import inspect
			print >> self.fd , datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" "+str(inspect.stack()[1][1:3])+"    "+msg
	
	def exit(self):
		if file is not None:
			self.fd.close()

if __name__ == "__main__" :
	logger = SimpleLogger()
	logger.setup(logger.DEBUG)
	L = logger.append
	L("Hi man", logger.DEBUG)
	L("Bye. BYe Debug")
	logger.setup(logger.ERROR)
        L("Hi man", logger.DEBUG)
        L("Bye. BYe Debug")
	L("Welcome Error", logger.ERROR)




