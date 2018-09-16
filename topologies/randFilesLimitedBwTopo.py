#!/usr/bin/python

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.node import Node
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from privateEtcHost import PrivateEtcHost
import sys

class RandomFilesHost( Node ):

	def config( self, **params ):
		super( RandomFilesHost, self).config( **params )
		
		
		# Create random files
		self.cmd("mkdir /var/www/html/ipsec")
		self.cmd("openssl rand -out /var/www/html/ipsec/10K 10000")
		self.cmd("openssl rand -out /var/www/html/ipsec/100K 100000")
		self.cmd("openssl rand -out /var/www/html/ipsec/1M 1000000")
		self.cmd("openssl rand -out /var/www/html/ipsec/10M 10000000")
		self.cmd("openssl rand -out /var/www/html/ipsec/100M 100000000")
		
		# Create private /etc directory
		etc = '/tmp/etc-%s' % self.name
		self.cmd( 'mkdir -p', etc )
		self.cmd( 'mount --bind /etc', etc )
		self.cmd( 'mount -n -t tmpfs tmpfs /etc' )
		self.cmd( 'ln -s %s/* /etc/' % etc )
		self.cmd( 'rm -rf /etc/*' )
		self.cmd( 'cp -a /%s/. /etc/' % etc )

	def terminate( self ):
		
		# Remove randomly generated files
		self.cmd("rm -r /var/www/html/ipsec")
		
		# Remove temporary /etc directory
		etc = '/tmp/etc-%s' % self.name
		self.cmd( 'umount /etc' )
		self.cmd( 'umount', etc )
		self.cmd( 'rm -r', etc )
		super( RandomFilesHost, self ).terminate()

class LimitedBwTopo(Topo):
    
	# Two hosts connected through a switch, with limited bandwidth.
	# Alice host has random generated files under /var/www/html/ipsec/

	def build(self, bandwidth=5):
	
		# Configure bandwidth value
		bandwidth=float(bandwidth)
		if(bandwidth <= 0):
			print "*** Bandwidth can not be negative. Setting it to the minimum value ***"
			bandwidth=0.01
		elif(bandwidth >= 1000):
			print "*** Maximum bandwidth is 1000 Mbps. Setting it to the maximum value ***"
			bandwidth=1000
	
		# Add hosts and switch
		centralSwitch = self.addSwitch('s1')
		hostAlice = self.addHost('alice', ip='10.0.0.1/24', cls=RandomFilesHost, mac='00:00:00:00:00:01')
		hostBob = self.addHost('bob', ip='10.0.0.2/24', cls=PrivateEtcHost, mac='00:00:00:00:00:02')
	
		# Add links
		self.addLink( centralSwitch, hostAlice, bw=bandwidth)
		self.addLink( centralSwitch, hostBob, bw=bandwidth)
        
def limitedBwTopo(): 
	if(len(sys.argv) > 1):
		
		# Check if argument is a valid float 
		try:
			float(sys.argv[1])
			topo = LimitedBwTopo(sys.argv[1])
		except ValueError:
			print "*** Wrong parameters. Usage: python randFilesLimitedBwTopo.py [b] - with b float value of links' bandwidth in Mb. ***"
			topo = LimitedBwTopo()
	else:
		topo = LimitedBwTopo()
	
	net = Mininet(topo, link=TCLink)
	net.start()
	CLI(net)
	net.stop()


if __name__ == '__main__':
	setLogLevel( 'info' )
	limitedBwTopo() 
