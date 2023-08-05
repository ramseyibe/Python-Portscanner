
#!/usr/bin/python

from socket import *
import optparse #library that helps us specify the help option to the user -h
from threading import *
from termcolor import colored

def connScan(targetHost, targetPorts):
	"""function that trys to connect to the ports to determine if it is open """

	try:
		sock = socket(AF_INET, SOCK_STREAM)
		sock.connect((targetHost, targetPorts))
		banner = sock.recv(1024)
		print(colored("[+] {}/tcp Open {} ".format(targetPorts, banner), "green"))
	except:
		print(colored("[-] {}/tcp Closed ".format(targetPorts), "red"))
	finally:
		#closes the connection
		sock.close()

def portScan(targetHost, targetPorts):
	"""Port scan function to scan the ports"""

	#resolve the IP address from the hostname
	try:
		targetIP = gethostbyname(targetHost)
	except:
		print(colored("Unkown Host {} ".format(targetHost), "red"))
	#resolve  host from the ip address
	try:
		targetName = gethostbyaddr(targetIP)
		print("[+] Scan Results For: " + targetName[0])
	except:
		print("[+] Scan Results for: " + targetIP)
	setdefaulttimeout(1)
	for targetPort in targetPorts:
		#using different thread to scan the different ports
		t = Thread(target=connScan, args=(targetHost, int(targetPort)))
		#start the port
		t.start()

def main():
	#gives the available options to the user
	parser = optparse.OptionParser('Usage of program: ' + '-H <target host> -p <target port>')

	#adding options to our parser
	parser.add_option('-H', dest='targetHost', type='string', help='specify target host')
	parser.add_option('-p', dest='targetPort', type='string', help='specify target ports seperated by comma')
	(options, args) = parser.parse_args()

	#setting the host and port variable
	targetHost = options.targetHost
	targetPorts = str(options.targetPort).split(',')

	#prints usage message
	if(targetHost == None ) | (targetPorts == None):
		print(parser.usage)
		exit(0)
	#call the portscan function
	portScan(targetHost, targetPorts)
	print("Ports		Service Version")


if __name__ == '__main__':
	main()

