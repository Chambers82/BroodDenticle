#Programmer: Brent E. Chambers
#Date: July 9, 2015
#Filename: EgressClient_beta.py
#Description: Egress client to connect to remote host on user supplied specifications

#####################Requirements 
'''
Architecture should be client and server. (Done)
Capability of testing both TCP,UDP,Both. 
Ability to test port ranges.  
Speed parameter (multi-threading output)
Timeout parameter
Configuration file to set these parameters (run without args)

Workflow:
	Server by default listens on port 80, 443.  
	Client connects to Server on webport and activates 
	Client generates random payload and sends it to the server on each port
	Server recieves the packet and send the random payload back to the client
	Client verifies the data is right and stores the outbound port
	Server stores all successful connections to a resource file in /usr/local
	

Remaining Requirements:
        [+] Ability to activate one service

#################################################################

'''

from socket import *
import threading
import time



#Outbound socket standard ports (1-1024)
def test_standardPorts():
	pass

class Denticle:
	target_server = '192.168.1.111'
	socket_range= {}
	listen_list = []
	sniff_list  = []
	log_entry   = []
	
	def new_tcp_connection(self, port):
		uniqueSock = "TCP_" + str(port)
		self.socket_range[uniqueSock] = socket(AF_INET, SOCK_STREAM)		#Creates a socket and puts it in the socket_range
		try:
			self.socket_range[uniqueSock].connect((self.target_server, port))
			print "Connected to Brood on:", uniqueSock, self.socket_range[uniqueSock]
		except:
			print "Could not connect to remote port."
			
	def new_udp_connection(self, port):
		uniqueSock = "UDP_" + str(port)
		self.socket_range[uniqueSock] = socket(AF_INET, SOCK_DGRAM)		#Creates a socket and puts it in the socket_range
		try:
			self.socket_range[uniqueSock].connect((self.target_server, port))
			print "Connected to Brood on:", uniqueSock, self.socket_range[uniqueSock]
		except:
			print "Could not connect to remote port."		
		
	def del_tcp_connection(self, port):
		uniqueSock = 'TCP_' + str(port)
		self.socket_range[uniqueSock].close()
		print "Denticle TCP connection to Brood deleted."
		
	def del_udp_connection(self, port):
		uniqueSock = 'UDP_' + str(port)
		self.socket_range[uniqueSock].close()
		print "Denticle UDP connection to Brood deleted."
		
	def TCP_Test(self, low, high):
		print "Testing egress ports..."
		for i in range(low, high):
			self.new_tcp_connection(i)
	
	def UDP_Test(self, low, high):
		print "Testing egress ports..."
		for i in range(low, high):
			self.new_udp_connection(i)
		
if __name__=='__main__':
	Instance = Denticle()
	#Instance.TCP_Test(460, 490)
	Instance.UDP_Test(460, 520)


#Outbound CommonPorts ([7,9,20,21,22,23,25,53,80,81,8080,90,9090,123,135,139,445,3389,1433])




