#!/usr/bin/python

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Node, CPULimitedHost
from mininet.cli import CLI
from mininet.log import setLogLevel
import sys

class TwoHostsLimited(Topo):
    
	# 2 hosts connected through a switch
	# Alice with 5% of the system CPU, Bob with the 50%

	def build(self):

	
		# Add hosts and switch
		centralSwitch = self.addSwitch('s1')
		hostAlice = self.addHost('alice', ip='10.0.0.1/24', mac='00:00:00:00:00:01',
					 cls=CPULimitedHost, cpu=.05)
		hostBob = self.addHost('bob', ip='10.0.0.2/24', mac='00:00:00:00:00:02',
				       cls=CPULimitedHost, cpu=.5)

		# Add links
		self.addLink( centralSwitch, hostAlice)  
		self.addLink( centralSwitch, hostBob)  
       
def twoHostsLimited(): 

	topo = TwoHostsLimited()
	net = Mininet( topo=topo, host=CPULimitedHost )
	net.start()
	CLI(net)
	net.stop()


if __name__ == '__main__':
	setLogLevel( 'info' )
	twoHostsLimited()
