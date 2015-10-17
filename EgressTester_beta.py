#Programmer: Brent E. Chambers
#Date: July 9, 2015
#Filename: EgressTester_beta.py
#Description: Egress tester to test client network egress policies

#####################Requirements 
'''
Architecture should be client and server. 
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

'''
from socket import *
import threading
import time


Reachable = []


def standardPorts():
        stdp = Brood()
        stdp.open_range(1, 1024)
        stdp.activate_drones()


def commonPorts():
        stdp = Brood()
        commonPorts = [7,9,20,21,22,23,25,53,80,81,8080,90,9090,123,135,139,445,3389,1433]
        for numb in commonPorts:
                stdp.new_service(numb)
        stdp.activate_drones()


def Activate(sock):
        sock = sock[1]
        while 1:
                try:
                        conn, addr = sock.accept()
                except:
                        continue
                print "Client connection by: ", addr
                conn.send("Hello " + str(addr[0]) + ":" + str(addr[1]) + "\n")
                Reachable.append((conn, addr))
                print "Client", addr, "stored."
                data = conn.recv(1024)
                conn.send(data)
                sock.close()
        

class Brood:
	socket_range = {}
	listen_list  = []
	sniff_list   = []
	log_entry    = []
	
	def new_service(self, port):
		uniqueSock = 'TCP_'+str(port)
		self.socket_range[uniqueSock] = socket(AF_INET, SOCK_STREAM)
		try:
			self.socket_range[uniqueSock].bind(('', port))
		except:
			print "Could not bind addess to socket."
		try:
			self.socket_range[uniqueSock].listen(3)
			print "Socket listening."
		except:
			print "Socket could not listen on port ", port
			
	def del_service(self, port):
		uniqueSock = 'TCP_' + str(port)
		self.socket_range[uniqueSock].close()
		print "Brood service ", uniqueSock, " terminated."
		
		
	def open_range(self, low, high):
		print "Creating sockets..."
		for i in range(low, high+1):
			uniqueSock = "TCP_"+str(i)
			self.socket_range[uniqueSock] = socket(AF_INET, SOCK_STREAM) 
		
		print "Binding ports..."
		for i in range(low, high+1):
			uniqueSock = "TCP_"+str(i)
			try:
				self.socket_range[uniqueSock].bind(('', i))
				self.listen_list.append(uniqueSock)
			except Exception, e:
				self.log_entry.append("Exception binding socket at port %i: %s" % (i, str(e)))
				self.log_entry.append("Likely already in use.  Adding socket to sniffList()")
				self.sniff_list.append(('127.0.0.1', i))
		print "Socket bind complete."
		print "Opening services..."
		for i in self.listen_list:
			print i
			self.socket_range[i].listen(5)
		print "All listed sockets are listening."
		print "["+time.ctime()+"]", "Brood Socket Server online."
		print "Brood Ports: ", low, "-", high
		self.log_entry.append("["+time.ctime()+"]" + "[+] Brood Socket Server online.")
		self.log_entry.append(("Brood Ports: ", low, "-", high))
		
	def close_range(self):
		for i in self.listen_list:
			self.socket_range[i].close()
		print "All Brood Services are closed."

	def activate_drones(self):
		thread_list = []
		for item in self.socket_range.items():
			t = threading.Thread(target=Activate, args=(item,))
			t.setDaemon(True)
			print  time.ctime(), item, " service activated. "
			thread_list.append(t)
		for thread in thread_list:
			print "Active count: ", threading.active_count()
			thread.start()
		for thread in thread_list:
			thread.join()
