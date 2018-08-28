#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf
from privateEtcHost import PrivateEtcHost

def emptyNet():

	vm1_ip='w.x.y.z'
	vm2_ip='a.b.c.d'
	controller_ip='a.b.c.d'

	net = Mininet( topo=None, build=False )

	net.addController( 'c0', controller=RemoteController, ip=controller_ip, port=6633 )

	hostAlice = net.addHost('alice', cls=PrivateEtcHost, ip='10.0.0.1/24', mac='00:00:00:00:00:01')
	s1 = net.addSwitch('s1')
	net.addLink(hostAlice, s1)

	# Delete old tunnel if still exists
	s1.cmd('ip tun del s1-gre1')
	# Create GRE tunnel
	s1.cmd('ip li ad s1-gre1 type gretap local '+vm1_ip+' remote '+vm2_ip+' ttl 64')
	s1.cmd('ip li se dev s1-gre1 up')
	Intf( 's1-gre1', node=s1 )
	net.start()
	CLI( net )
	#Delete the tunnel before exiting
	s1.cmd('ip li se dev s1-gre1 down')
	s1.cmd('ip tun del s1-gre1')
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	emptyNet()
