class GameBase( object ):
	def __init__( self, players ):
		self.players = players

	def getPlayers( self ):
		return self.players

	def addPlayer( self, player ):
		self.players.append( player )

	def createPlayer( self, ply ):
		plyexists = False
		for ply in self.getPlayers():
			if ply.getID() == id:
				plyexists = True
				break
		if not plyexists:
			self.addPlayer( ply )

	def getPlayerByID( self, id ):
		FoundPlayer = None
		for ply in self.getPlayers():
			if ply.getID() == id:
				FoundPlayer = ply
		if FoundPlayer is None:
			return None
		else:
			return FoundPlayer

class Player( object ):
	def __init__( self, id, points ):
		self.id = id
		self.points = points

	def getID( self ):
		return self.id

	def getPoints( self ):
		return self.points
	
	def addPoints( self, points ):
		self.points += points

	def removePoints( self, points ):
		self.points -= max( min( self.points, float( 'inf' ) ), 0 )
