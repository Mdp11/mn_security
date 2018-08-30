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

	s1 = net.addSwitch('s1')
	hostGroup = []

	if(nHosts==1):
		hostAlice = net.addHost('alice', cls=PrivateEtcHost, ip='10.0.0.1/16', mac='00:00:00:00:00:01')
		hostGroup.append(hostAlice)
	elif(nHosts==2):
		hostAlice = net.addHost('alice', cls=PrivateEtcHost, ip='10.0.0.1/16', mac='00:00:00:00:00:01')
		hostGroup.append(hostAlice)
		hostCarlo = net.addHost('carlo', cls=PrivateEtcHost, ip='10.0.0.2/16', mac='00:00:00:00:00:02')
		hostGroup.append(hostCarlo)
	elif(nHosts>2):
		for k in range(1,nHosts+1):
			host = net.addHost('h1_%d' %k, cls=PrivateEtcHost, ip='10.0.0.%d/16' %k, mac='%s' %hex(k)[2:].zfill(12))
			hostGroup.append(host)

	# Add links
	for h in hostGroup:
		net.addLink( s1, h)  

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
