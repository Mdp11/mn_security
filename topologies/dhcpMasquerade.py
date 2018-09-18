#!/usr/bin/python

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from privateEtcHost import PrivateEtcHost

class DHCPTopo( Topo ):
	
	# 3 hosts connected through a switch, with one being connected
	# to a link with limited bandiwdth and 500ms of delay"

	def build( self ):
		
		# Add hosts and switch
		switch = self.addSwitch( 's1' )

		hostAlice = self.addHost( 'alice', ip='10.0.0.1/24', mac='00:00:00:00:00:01',
					 cls=PrivateEtcHost )
		hostBob = self.addHost( 'bob', ip='10.0.0.2/24', mac='00:00:00:00:00:02',
				       cls=PrivateEtcHost )
		hostChuck = self.addHost( 'chuck', ip='10.0.0.3/24', mac='00:00:00:00:00:03',
					 cls=PrivateEtcHost )

		# Add links
		self.addLink( hostAlice, switch )
		self.addLink( hostChuck, switch )
		self.addLink( hostBob, switch, bw=10, delay='500ms' )


def dhcp():

	topo = DHCPTopo()
	net = Mininet( topo=topo, link=TCLink )
	net.addNAT().configDefault()
	net.start()
	CLI(net)
	net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    dhcp()
