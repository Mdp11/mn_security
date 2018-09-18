#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf
from privateEtcHost import PrivateEtcHost

def vm2Net():

	# Set machines' addresses
	vm1_ip='w.x.y.z'
	vm2_ip='a.b.c.d'
	controller_ip='a.b.c.d'

	# Create empty network without building it now
	net = Mininet( topo=None, build=False)

	# Configure the remote controller
	net.addController( 'c0', controller=RemoteController, ip=controller_ip,	port=6633)

	# Add hosts, switch and links
	hostBob = net.addHost( 'bob', ip='10.0.0.2/24', mac='00:00:00:00:00:02',
			     cls=PrivateEtcHost )
	s2 = net.addSwitch( 's2' )
	net.addLink( hostBob, s2 )

	# Delete the old tunnel if still exists
	s2.cmd('ifconfig s2-gre1 down')
	s2.cmd('ip tunnel del s2-gre1')
	s2.cmd('ip link del s2-gre1')

	# Create GRE tunnel
	s2.cmd('ip link add s2-gre1 type gretap local '+vm2_ip+' remote '+vm1_ip+' ttl 64')
	s2.cmd('ip link set dev s2-gre1 up')
	
	# Add the GRE interface to the switch
	Intf('s2-gre1', node=s2)
	
	net.start()
	CLI( net )
	
	# Delete the tunnel before exiting
	s2.cmd('ifconfig s2-gre1 down')
	s2.cmd('ip tunnel del s2-gre1')
	s2.cmd('ip link del s2-gre1')
	
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	vm2Net()
