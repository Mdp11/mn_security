#!/usr/bin/python

from mininet.node import Node

class PrivateEtc( Node ):
	def config( self, **
		super( PrivateEtc, self).config( **params )
		etc = '/tmp/etc-%s' % self.name
		self.cmd( 'mkdir -p', etc )
		self.cmd( 'mount --bind /etc', etc )
		self.cmd( 'mount -n -t tmpfs tmpfs /etc' )
		self.cmd( 'ln -s %s/* /etc/' % etc )
		self.cmd( 'rm -rf /etc/*' )
		self.cmd( 'cp -a /%s/. /etc/' % etc )

	def terminate( self ):
		etc = '/tmp/etc-%s' % self.name
		self.cmd( 'umount /etc' )
		self.cmd( 'umount', etc )
		self.cmd( 'rm -r', etc )
		super( PrivateEtc, self ).terminate()
