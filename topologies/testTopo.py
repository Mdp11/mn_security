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

	def build(self, n=2):
	
		n=int(n)
	
		# Add hosts and switch
		rightSwitch = self.addSwitch('s1')
		leftSwitch = self.addSwitch('s2')
		hostAlice = self.addHost('alice', cls=PrivateEtcHost, ip='10.0.0.1/24', mac='00:00:00:00:00:01')
		hostChuck = self.addHost('chuck', cls=PrivateEtcHost, ip='10.0.0.2/24', mac='00:00:00:00:00:02')
		hostBob = self.addHost('bob', cls=PrivateEtcHost, ip='10.0.1.1/24', mac='00:00:00:00:01:01')

		# Add links
		self.addLink( rightSwitch, hostAlice)
		self.addLink( rightSwitch, hostChuck)
		self.addLink( leftSwitch, hostChuck)
		self.addLink( leftSwitch, hostBob) 
       
def simpleTopo(): 

	topo = SimpleTopo()
	net = Mininet( topo )
	net.get('chuck').setIP('10.0.1.2/24', intf="chuck-eth1")
	net.start()
	CLI(net)
	net.stop()


if __name__ == '__main__':
	setLogLevel( 'info' )
	simpleTopo()
