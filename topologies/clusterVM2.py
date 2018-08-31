#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf
from privateEtcHost import PrivateEtcHost

def vm2Net():

	vm1_ip='w.x.y.z'
	vm2_ip='a.b.c.d'
	controller_ip='a.b.c.d'

	net = Mininet( topo=None, build=False)

	# Configure the remote controller
	net.addController( 'c0', controller=RemoteController, ip=controller_ip,	port=6633)

	#Set up hosts, switch and links
	hostChuck = net.addHost( 'chuck', cls=PrivateEtcHost, ip='10.0.1.1/16', mac='00:00:00:00:01:01' )
	hostDave = net.addHost('dave', cls=PrivateEtcHost, ip='10.0.1.2/16', mac='00:00:00:00:01:02')
	s2 = net.addSwitch( 's1' )
	net.addLink( hostChuck, s2 )
	net.addLink( hostDave, s2 )

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
