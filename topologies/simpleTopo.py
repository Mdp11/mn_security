#!/usr/bin/python

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Node
from mininet.cli import CLI
from mininet.log import setLogLevel
from privateEtcHost import PrivateEtcHost
import sys

class SimpleTopo(Topo):
    
	"N hosts connected through a switch, each with private /etc directories"
  
	# Add Alice and Bob hosts
	def addAliceBob(self, hostGroup):
		hostAlice = self.addHost('alice', cls=PrivateEtcHost, ip='10.0.0.1/24', mac='00:00:00:00:00:01')
		hostBob = self.addHost('bob', cls=PrivateEtcHost, ip='10.0.0.2/24', mac='00:00:00:00:00:02')
		hostGroup.append(hostAlice)
		hostGroup.append(hostBob)

	def build(self, n=2):
	
		n=int(n)
	
		# Add hosts and switch
		centralSwitch = self.addSwitch('s1')
		hostGroup = []
		if(n <= 2):
			if(n < 2):
				print "*** Minimum number of hosts is two. Instantiating two hosts. ***"
			self.addAliceBob(hostGroup)
		elif(n == 3):
		       	self.addAliceBob(hostGroup)
			hostCarlo = self.addHost('carlo', cls=PrivateEtcHost, ip='10.0.0.3/24', mac='00:00:00:00:00:03')
			hostGroup.append(hostCarlo)
		elif(n > 3):
			for k in range(1,n+1):
				host = self.addHost('h%d' %k, cls=PrivateEtcHost, ip='10.0.0.%d/24' %k, mac='%s' %hex(k)[2:].zfill(12))
				hostGroup.append(host)
		elif(n >= 253):
			if(n > 253):
				print "*** Maximum number of hosts is 253. Instantiating 253 hosts. ***"
			for k in range(1,253):
				host = self.addHost('h%d' %k, cls=PrivateEtcHost, ip='10.0.0.%d/24' %k, mac='%s' %hex(k)[2:].zfill(12))
				hostGroup.append(host)

		# Add links
		for h in hostGroup:
			self.addLink( centralSwitch, h)  
       
def simpleTopo(): 
	
	# Check arguments passed
	
	nHosts = False
	
	if(len(sys.argv) > 1 and sys.argv[1].isdigit()):
		topo = SimpleTopo(sys.argv[1])
		nHosts = true
	else:
		topo = SimpleTopo()

	net = Mininet( topo )
	if((len(sys.argv) == 2 and sys.argv[1] == 'c') or (len(sys.argv) > 2 and sys.argv[2] == 'c')):
		net.addNAT().configDefault()
	else:
		if (nHosts == False):
			print "*** Wrong parameters. Usage: python simpleTopo.py [n] [c] - with n integer number of hosts and c to give internet access to the topology. ***"
	
	net.start()
	CLI(net)
	net.stop()


if __name__ == '__main__':
	setLogLevel( 'info' )
	simpleTopo()
