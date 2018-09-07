#!/usr/bin/python

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Node
from mininet.cli import CLI
from mininet.log import setLogLevel
from privateEtcHost import PrivateEtcHost
from mininet.node import CPULimitedHost
import sys

class SimpleTopo(Topo):

	def build(self):

		# Add hosts and switch
		centralSwitch = self.addSwitch('s1')
		hostAlice = self.addHost('alice', cls=PrivateEtcHost, ip='10.0.0.1/24', mac='00:00:00:00:00:01', cpu=.1)
		hostBob = self.addHost('bob', cls=PrivateEtcHost, ip='10.0.0.2/24', mac='00:00:00:00:00:02')
		hostChuck = self.addHost('chuck', cls=PrivateEtcHost, ip='10.0.0.3/24', mac='00:00:00:00:00:03')
		
		# Add links
		self.addLink( centralSwitch, hostAlice)
		self.addLink( centralSwitch, hostBob)
		self.addLink( centralSwitch, hostChuck)
       
def limitedCPU(): 
	topo = LimitedCPU()
	net = Mininet( topo=topo, host=CPULimitedHost)
	net.start()
	CLI(net)
	net.stop()


if __name__ == '__main__':
	setLogLevel( 'info' )
	limitedCPU()
