#!/usr/bin/python

from mininet.node import Node

class PrivateEtcHost( Node ):
	def config( self, **params):
		super( PrivateEtcHost, self).config( **params )
		etc = '/tmp/etc-%s' % self.name
		self.cmd( 'mkdir -p', etc )
		
		# Bind the /etc folder to the /tmp/etc-hostName folder just created
		# so the same content is accessible in it
		self.cmd( 'mount --bind /etc', etc )
		
		# Mount a temporary fylesystem at the /etc directory
		self.cmd( 'mount -n -t tmpfs tmpfs /etc' )
		
		# Create links to each file from the /tmp/etc-hostName folder
		# in the /etc folder
		self.cmd( 'ln -s %s/* /etc/' % etc )
		
		self.cmd( 'rm -rf /etc/*' )
		self.cmd( 'cp -a /%s/. /etc/' % etc )

	def terminate( self ):
		etc = '/tmp/etc-%s' % self.name
		self.cmd( 'umount /etc' )
		self.cmd( 'umount', etc )
		self.cmd( 'rm -r', etc )
		super( PrivateEtcHost, self ).terminate()
