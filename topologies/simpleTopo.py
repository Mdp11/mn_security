#!/usr/bin/python

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Node
from mininet.cli import CLI
from mininet.log import setLogLevel
from privateEtcHost import PrivateEtcHost
import sys

class SimpleTopo(Topo):
    
	"2 or 3 hosts connected through a switch, each with private /etc directories"
  
	# Add Alice and Bob hosts
	def addAliceBob(self, hostGroup):
		hostAlice = self.addHost('alice', ip='10.0.0.1/24', mac='00:00:00:00:00:01',
					 cls=PrivateEtcHost)
		hostBob = self.addHost('bob', ip='10.0.0.2/24', mac='00:00:00:00:00:02',
				       cls=PrivateEtcHost)
		hostGroup.append(hostAlice)
		hostGroup.append(hostBob)

	def build(self, n=2):
	
		n=int(n)
	
		# Add hosts and switch
		centralSwitch = self.addSwitch('s1')
		hostGroup = []
		self.addAliceBob(hostGroup)
		if(n < 2):
			print "*** Minimum number of hosts is two ***"
			print "*** Instantiating two hosts ***"
		elif(n >= 3):
			if(n > 3):
				print "*** Maximum number of hosts is three ***"
				print "*** Instantiating three hosts ***"
			hostChuck = self.addHost('chuck', ip='10.0.0.3/24', mac='00:00:00:00:00:03',
						 cls=PrivateEtcHost)
			hostGroup.append(hostChuck)

		# Add links
		for h in hostGroup:
			self.addLink( centralSwitch, h)  
       
def simpleTopo(): 
	
	# Check arguments passed
	
	nHosts = False
	
	if(len(sys.argv) > 1 and sys.argv[1].isdigit()):
		topo = SimpleTopo(sys.argv[1])
		nHosts = True
	else:
		topo = SimpleTopo()

	net = Mininet( topo )
	if((len(sys.argv) == 2 and sys.argv[1] == 'c') or
	   (len(sys.argv) > 2 and sys.argv[2] == 'c')):
		net.addNAT().configDefault()
	else:
		if (nHosts == False and len(sys.argv) >= 2):
			print "*** Wrong parameters ***"
			print "*** Usage: python simpleTopo.py [n] [c] ***"
			print "*** with n integer number of hosts (optional) that can be 2 or 3"
			print "*** and c to give internet access to the topology. ***"
			print "*** Starting topology with 2 hosts and no internet access ***"
	
	net.start()
	CLI(net)
	net.stop()


if __name__ == '__main__':
	setLogLevel( 'info' )
	simpleTopo()
