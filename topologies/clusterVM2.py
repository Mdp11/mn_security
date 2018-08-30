#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf
from privateEtcHost import PrivateEtcHost
import sys

def emptyNet():
	nHosts=1
	if(len(sys.argv) > 1 and sys.argv[1].isdigit()):
		nHosts = sys.argv[1]
		nHosts = int(nHosts)

	vm1_ip='w.x.y.z'
	vm2_ip='a.b.c.d'
	controller_ip='a.b.c.d'

	net = Mininet( topo=None, build=False )
	net.addController( 'c0', controller=RemoteController, ip=controller_ip, port=6633 )


	s2 = net.addSwitch( 's2' )
	hostGroup = []

	if(nHosts==1):
		hostBob = net.addHost('bob', cls=PrivateEtcHost, ip='10.0.1.1/16', mac='00:00:00:00:01:01')
		hostGroup.append(hostBob)
	elif(nHosts==2):
		hostBob = net.addHost('bob', cls=PrivateEtcHost, ip='10.0.1.1/16', mac='00:00:00:00:01:01')
		hostGroup.append(hostBob)
		hostDave = net.addHost('dave', cls=PrivateEtcHost, ip='10.0.1.2/16', mac='00:00:00:00:01:02')
		hostGroup.append(hostDave)
	elif(nHosts>2):
		for k in range(1,nHosts+1):
			host = net.addHost('h2_%d' %k, cls=PrivateEtcHost, ip='10.0.1.%d/16' %k, mac='%s' %hex(k+256)[2:].zfill(12))
			hostGroup.append(host)

	# Add links
	for h in hostGroup:
		net.addLink( s2, h)  

	# Delete old tunnel if still exists
	s2.cmd('ip tun del s2-gre1')
	# Create GRE tunnel
	s2.cmd('ip li ad s2-gre1 type gretap local '+vm2_ip+' remote '+vm1_ip+' ttl 64')
	s2.cmd('ip li se dev s2-gre1 up')
	Intf( 's2-gre1', node=s2 )
	net.start()
	CLI( net )
	#Delete the tunnel before exiting
	s2.cmd('ip li se dev s2-gre1 down')
	s2.cmd('ip tun del s2-gre1')
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	emptyNet()
