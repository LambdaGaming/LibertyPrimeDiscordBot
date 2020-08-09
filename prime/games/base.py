from games import pointshop

class GameBase( object ):
	def __init__( self, players ):
		self.players = players

	def getPlayers( self ):
		return self.players

	def addPlayer( self, player ):
		self.players.append( player )

	def createPlayer( self, ply ):
		plyexists = False
		if ply not in self.getPlayers():
			self.addPlayer( ply )

	def getPlayerByID( self, id ):
		for ply in self.getPlayers():
			if ply.getID() == id:
				return ply

class Player( object ):
	def __init__( self, id ):
		self.id = id

	def getID( self ):
		return self.id

	def getPoints( self ):
		readfile = pointshop.getJSON( str( self.id ) )
		return readfile["points"]
	
	def addPoints( self, points ):
		readfile = pointshop.getJSON( str( self.id ) )
		readfile["points"] += points
		pointshop.writeJSON( str( self.id ), readfile )

	def removePoints( self, points ):
		readfile = pointshop.getJSON( str( self.id ) )
		readfile["points"] -= max( min( points, float( 'inf' ) ), 0 )
		pointshop.writeJSON( str( self.id ), readfile )
