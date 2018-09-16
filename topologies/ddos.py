#!/usr/bin/python

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Node, CPULimitedHost
from mininet.cli import CLI
from mininet.log import setLogLevel
import sys

class SimpleTopo(Topo):
    
	"50 hosts connected through a switch, with h1 getting only 5% of the available CPU"
  
	def build(self):
		
		# Add hosts and switch
		centralSwitch = self.addSwitch('s1')
		hostGroup = []
		h1 = self.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01', cpu=.05)
		for k in range(2,51):
			host = self.addHost('h%d' %k, ip='10.0.0.%d/24' %k, mac='%s' %hex(k)[2:].zfill(12))
			hostGroup.append(host)

		# Add links
		self.addLink(centralSwitch, h1)
		for h in hostGroup:
			self.addLink( centralSwitch, h)  
       
def simpleTopo(): 

	topo = SimpleTopo()
	net = Mininet( topo)
	net.start()
	CLI(net)
	net.stop()


if __name__ == '__main__':
	setLogLevel( 'info' )
	simpleTopo()
