#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf
from privateEtcHost import PrivateEtcHost

def vm1Net():

	# Set machines' addresses
	vm1_ip='w.x.y.z'
	vm2_ip='a.b.c.d'
	controller_ip='a.b.c.d'

	# Create empty network without building it now
	net = Mininet( topo=None, build=False)

	# Configure the remote controller
	net.addController( 'c0', controller=RemoteController, ip=controller_ip,	port=6633)

	# Add hosts, switch and links
	hostAlice = net.addHost( 'alice', ip='10.0.0.1/24', mac='00:00:00:00:00:01',
			       cls=PrivateEtcHost )
	s1 = net.addSwitch( 's1' )
	net.addLink( hostAlice, s1 )

	# Delete old tunnel if it still exists
	s1.cmd('ifconfig s1-gre1 down')
	s1.cmd('ip tunnel del s1-gre1')
	s1.cmd('ip link del s1-gre1')
	
	# Create GRE tunnel	
	s1.cmd('ip link add s1-gre1 type gretap local '+vm1_ip+' remote '+vm2_ip+' ttl 64')
	s1.cmd('ip link set dev s1-gre1 up')
	
	# Add the GRE interface to the switch
	Intf( 's1-gre1', node=s1 )
	
	net.start()
	CLI( net )
	
	# Delete the tunnel before exiting
	s1.cmd('ifconfig s1-gre1 down')
	s1.cmd('ip tunnel del s1-gre1')
	s1.cmd('ip link del s1-gre1')
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	vm1Net()
