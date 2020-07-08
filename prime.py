import discord
import random
import json
import requests
import math

BadWords = [ "communism", "china", "ussr", "stalin", "lenin", "putin", "vodka", "commie", "russia", "cuba", "vietnam", "mao", "castro", "bernie", "kim", "korea", "california", "red", "cyka", "blyat", "communist", "gulag", "chinese", "vietnamese", "korean", "californian", "reds", "communists", "gulags", "vodkas", "blizzard" ]

Quotes = [
	"Weapons: hot.",
	"Mission: the destruction of any and all Chinese communists.",
	"America will never fall to communist invasion.",
	"Obstruction detected. Composition: titanium alloy supplemented by photonic resonance barrier.",
	"Probability of mission hindrance: zero percent.",
	"Democracy.... is non-negotiable.",
	"Death is a preferable alternative to communism.",
	"Communist detected on American soil. Lethal force engaged.",
	"Tactical assessment: Red Chinese victory-impossible.",
	"Communism is the very definition of failure.",
	"Communism is a temporary setback on the road to freedom.",
	"Embrace democracy or you will be eradicated.",
	"Democracy will never be defeated.",
	"Primary Targets: any and all Red Chinese invaders.",
	"Emergency Communist Acquisition Directive: immediate self destruct. Better dead, than Red."
]

"""
	For now, this is going to be a very simplified version of Wheel of Fortune that
	might resemble hangman more than the actual game show.
	
	Initiating the game:
		Discord IDs from an external whitelist will be able to start the game using the
		'!wof start' command. Anyone in the Discord will be able to participate in the game,
		even after it has started. While the game is running, normal Liberty Prime functions
		will not work and he will not respond to any keywords.

	Playing the game:
		A single word will be selected from the random word generator and players will have
		to guess on that word. Each player gets 5 letter guesses wrong before they lose a
		point and can no longer guess on that word. Players can buy 3 more guesses at the cost
		of 1 point. They can also guess what the word is at any time, but will lose a point if
		they are wrong. For every 3 letters a player guesses correctly, they will receive a point.

	Ending the game:
		The same Discord users who are able to start the game can also end it using '!wof end'.
		Once the game ends, a list of players and how many points they got will be printed out.
		Players can then use these points to purchase server-related items such as weapons for
		CityRP or an item on SCP:SL.
"""

def getRandomWord():
	url = requests.get( "https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json" ).json() # Pretty slow but it's good enough for now
	nextWord = random.choice( list( url ) )
	return nextWord

WoFActive = False
class WoF:
	def __init__( self, word, players, letters ):
		self.word = word
		self.players = players
		self.letters = letters
		global WoFActive
		WoFActive = True
	
	def getWord( self ):
		return self.word

	def setWord( self, word ):
		self.word = word
	
	def getPlayers( self ):
		return self.players

	def addPlayer( self, player ):
		self.players.append( player )

	def nextWord( self ):
		randomWord = getRandomWord()
		self.setWord( randomWord )
		self.setLetters( [] )
		for ply in self.getPlayers():
			ply.setTries( 5 )
		return randomWord
	
	def getLetters( self ):
		return self.letters

	def setLetters( self, letters ):
		self.letters = letters

	def addLetter( self, letter ):
		self.letters.append( letter.lower() )

	def getFormattedWord( self, word ):
		if not self.getLetters():
			underscore = ""
			for i in range( len( word ) ):
				underscore += "_"
			return "`" + underscore + "`"
		else:
			letters = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" ]
			for i in self.getLetters():
				letters.remove( i )
			for i in letters:
				if i in word:
					word = word.replace( i, "_" )
		return "`" + word + "`"

	def createPlayer( self, id ):
		plyexists = False
		for ply in self.getPlayers():
			if ply.getID() == id:
				plyexists = True
				break
		if not plyexists:
			self.addPlayer( self.WoF_Player( id, 0, 5, 0 ) )

	def getPlayerByID( self, id ):
		FoundPlayer = None
		for ply in self.getPlayers():
			if ply.getID() == id:
				FoundPlayer = ply
		if FoundPlayer is None:
			return None
		else:
			return FoundPlayer

	class WoF_Player:
		def __init__( self, id, points, tries, correct ):
			self.id = id
			self.points = points
			self.tries = tries
			self.correct = correct
		
		def getID( self ):
			return self.id

		def getPoints( self ):
			return self.points
		
		def addPoints( self, points ):
			self.points += points

		def removePoints( self, points ):
			self.points -= max( min( self.points, math.inf ), 0 )

		def getTries( self ):
			return self.tries

		def setTries( self, tries ):
			self.tries = tries

		def removeTry( self ):
			self.tries -= max( min( 1, math.inf ), 0 )

		def outOfTries( self ):
			return self.tries <= 0

		def addCorrect( self, correct ):
			self.correct += correct

		def setCorrect( self, correct ):
			self.correct = correct

		def getCorrect( self ):
			return self.correct

class MyClient( discord.Client ):
	async def on_ready( self ):
		randfallout = str( random.randint( 3, 4 ) )
		await client.change_presence( activity = discord.Game( name = "Fallout " + randfallout ) )
		print( 'Logged in as {0}!'.format( self.user ) )

	async def on_message( self, message ):
		global WoFActive
		global WoFGame
		if message.author.bot: return
		split = message.content.split( " " )
		lower = message.content.lower()
		if WoFActive:
			if split[0] == "!wof":
				WoFGame.createPlayer( message.author.id )
				MessagePlayer = WoFGame.getPlayerByID( message.author.id )
				if 1 not in range( -len( split ), len( split ) ) or split[1] == " ":
					await message.channel.send( "List of available Wheel of Fortune commands: guessletter, guessword, end, nextword, points, buyguesses" )
				elif split[1] == "guessletter":
					if 2 not in range( -len( split ), len( split ) ) or split[2] == " " or not split[2].isalpha() or len( split[2] ) > 1:
						await message.channel.send( "Please input a single letter for the guessletter command." )
						return
					if split[2] in WoFGame.getLetters():
						await message.channel.send( "Letter '" + split[2].upper() + "' has already been guessed." )
						return
					if MessagePlayer.outOfTries():
						await message.channel.send( message.author.name + ", you are out of letter guesses!" )
						return
					if split[2] in WoFGame.getWord():
						WoFGame.addLetter( split[2] )
						MessagePlayer.addCorrect( 1 )
						await message.channel.send( message.author.name + " has guessed a letter correctly!\nGuessed letters so far: " + WoFGame.getFormattedWord( WoFGame.getWord() ) )
						if MessagePlayer.getCorrect() >= 3:
							MessagePlayer.addPoints( 1 )
							MessagePlayer.setCorrect( 0 )
							await message.channel.send( message.author.name + " has guessed 3 correct letters and earned 1 point!" )
					else:
						MessagePlayer.removeTry()
						await message.channel.send( "Letter '" + split[2].upper() + "' is not in this word. " + message.author.name + " has " + str( MessagePlayer.getTries() ) + " guesses left." )
				elif split[1] == "guessword":
					if 2 not in range( -len( split ), len( split ) ) or split[2] == " " or not split[2].isalpha():
						await message.channel.send( "Please input a word without numbers or special characters." )
						return
					if split[2].lower() == WoFGame.getWord().lower():
						await message.channel.send( message.author.name + " has guessed the correct word and received 1 point!" )
						MessagePlayer.addPoints( 1 )
						WoFGame.nextWord()
						await message.channel.send( "Next word: " + WoFGame.getFormattedWord( WoFGame.getWord() ) )
					else:
						MessagePlayer.removePoints( 1 )
						await message.channel.send( message.author.name + " has incorrectly guessed the word and lost 1 point!" )
				elif split[1] == "end":
					whitelist = open( "whitelist.txt", "r" )
					allowed = False
					for ids in whitelist:
						if ids == str( message.author.id ):
							allowed = True
					if not allowed:
						await message.channel.send( message.author.name + ", you do not have permission to use the end command." )
						return
					del WoFGame
					WoFActive = False
					await message.channel.send( "Wheel of Fortune has ended. Returning to normal operations." )
				elif split[1] == "nextword":
					whitelist = open( "whitelist.txt", "r" )
					allowed = False
					for ids in whitelist:
						if ids == str( message.author.id ):
							allowed = True
					if not allowed:
						await message.channel.send( message.author.name + ", you do not have permission to use the nextword command." )
						return
					WoFGame.nextWord()
					await message.channel.send( "Word has been forcibly changed to " + WoFGame.getFormattedWord( WoFGame.getWord() ) + "." )
				elif split[1] == "points":
					await message.channel.send( message.author.name + " currently has " + str( MessagePlayer.getPoints() ) + " point(s)." )
				elif split[1] == "buyguesses":
					if MessagePlayer.getTries() > 0:
						await message.channel.send( message.author.name + ", you still have guesses remaining. You don't need to buy more." )
						return
					if MessagePlayer.getPoints() < 1:
						await message.channel.send( message.author.name + ", you don't have enough points to buy more guesses." )
						return
					MessagePlayer.removePoints( 1 )
					MessagePlayer.setTries( 3 )
					await message.channel.send( message.author.name + " has purchased 3 more guesses for 1 point." )
		else:
			if split[0] == "!wof":
				if 1 not in range( -len( split ), len( split ) ) or split[1] == " ":
					await message.channel.send( "List of available Wheel of Fortune commands: start" )
					return
				if split[1] == "start":
					whitelist = open( "whitelist.txt", "r" )
					allowed = False
					for ids in whitelist:
						if ids == str( message.author.id ):
							allowed = True
					if not allowed:
						await message.channel.send( message.author.name + ", you do not have permission to use the start command." )
						return
					try:
						WoFGame = WoF( getRandomWord(), [], [] )
						await message.channel.send( "WHEEL OF FORTUNE MODE ACTIVATED\nWord: " + WoFGame.getFormattedWord( WoFGame.getWord() ) )
					except:
						await message.channel.send( "Something went wrong with the random word generator. GitHub might be down or the host of this bot might have a slow connection." )
				return
			if "hong kong" in lower:
				await message.channel.send( "LIBERATE HONG KONG, REVOLUTION OF OUR AGE!" )
				return
			for item in BadWords:
				if item in lower:
					await message.channel.send( Quotes[ random.randint( 0, len( Quotes ) ) ].upper() )
					break

try:
	token = open( "token.txt", "r" )
	client = MyClient()
	client.run( token.read() )
except:
	print( "Failed to read token file. Either the file doesn't exist or the token format is incorrect." )
