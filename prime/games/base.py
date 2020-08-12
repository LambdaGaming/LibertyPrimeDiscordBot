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
		for player in self.getPlayers():
			if player.getID() == ply.id:
				plyexists = True
				break
		if not plyexists:
			self.addPlayer( ply )

	def getPlayerByID( self, id ):
		for ply in self.getPlayers():
			if ply.getID() == id:
				return ply

	def getScores( self, guild ):
		finalstr = "N/A"
		for ply in self.getPlayers():
			if self.getPlayers().index( ply ) == 0:
				finalstr = "<@" + str( ply.getID() ) + ">: " + str( ply.getScore() ) + " point(s)"
			else:
				finalstr += ", <@" + str( ply.getID() ) + ">: " + str( ply.getScore() ) + " point(s)"
		return finalstr

class Player( object ):
	def __init__( self, id, score ):
		self.id = id
		self.score = score

	def getID( self ):
		return self.id

	def getScore( self ):
		return self.score

	def setScore( self, points ):
		self.score += points

	def getPoints( self ):
		readfile = pointshop.getJSON( str( self.id ) )
		return readfile["points"]
	
	def addPoints( self, points ):
		readfile = pointshop.getJSON( str( self.id ) )
		readfile["points"] += points
		pointshop.writeJSON( str( self.id ), readfile )
		self.setScore( points )

	def removePoints( self, points ):
		readfile = pointshop.getJSON( str( self.id ) )
		readfile["points"] -= max( min( points, float( 'inf' ) ), 0 )
		pointshop.writeJSON( str( self.id ), readfile )
		self.setScore( -points )
