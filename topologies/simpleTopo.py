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
			self.addAliceBob(hostGroup)
		if(n == 3):
		       	self.addAliceBob(hostGroup)
			hostCarlo = self.addHost('carlo', cls=PrivateEtcHost, ip='10.0.0.3/24', mac='00:00:00:00:00:03')
			hostGroup.append(hostCarlo)
		if(n > 3):
			h1 = self.addHost('h1', cls=PrivateEtcHost, ip='10.0.0.1/24', mac='00:00:00:00:00:01')
			hostGroup.append(h1)
			for k in range(2,n+1):
				host = self.addHost('h%d' %k, cls=PrivateEtcHost, ip='10.0.0.%d/24' %k, mac='%s' %hex(k)[2:].zfill(12))
				hostGroup.append(host)

		# Add links
		for h in hostGroup:
			self.addLink( centralSwitch, h)  
       
def simpleTopo(): 
	if(len(sys.argv) > 1 and sys.argv[1].isdigit()):
		topo = SimpleTopo(sys.argv[1])
	else:
		topo = SimpleTopo()
	net = Mininet( topo )
	if((len(sys.argv) == 2 and sys.argv[1] == 'c') or (len(sys.argv) > 2 and sys.argv[2] == 'c')):
		net.addNAT().configDefault()
	net.start()
	CLI(net)
	net.stop()


if __name__ == '__main__':
	setLogLevel( 'info' )
	simpleTopo()
