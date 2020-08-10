import config
import requests
import json
import random
from games import base

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
class WoF( base.GameBase ):
	def __init__( self, players, word, letters ):
		super().__init__( players )
		self.word = word
		self.letters = letters
		global WoFActive
		WoFActive = True
		config.GameActive = True
	
	def getWord( self ):
		return self.word

	def setWord( self, word ):
		self.word = word

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

	class WoF_Player( base.Player ):
		def __init__( self, id, score, tries, correct ):
			super().__init__( id, score )
			self.tries = tries
			self.correct = correct

		def getTries( self ):
			return self.tries

		def setTries( self, tries ):
			self.tries = tries

		def removeTry( self ):
			self.tries -= max( min( 1, float( 'inf' ) ), 0 )

		def outOfTries( self ):
			return self.tries <= 0

		def addCorrect( self, correct ):
			self.correct += correct

		def setCorrect( self, correct ):
			self.correct = correct

		def getCorrect( self ):
			return self.correct

async def checkChatMessage( message ):
	split = message.content.split( " " )
	global WoFGame
	global WoFActive
	if WoFActive:
		if split[0] == "!wof":
			WoFGame.createPlayer( WoF.WoF_Player( message.author.id, 0, 5, 0 ) )
			MessagePlayer = WoFGame.getPlayerByID( message.author.id )
			if 1 not in range( -len( split ), len( split ) ) or split[1] == " ":
				await message.channel.send( "List of available Wheel of Fortune commands: guessletter, guessword, end, nextword, buyguesses" )
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
				whitelist = open( "settings/whitelist.txt", "r" )
				allowed = False
				for ids in whitelist:
					if ids == str( message.author.id ):
						allowed = True
				if not allowed:
					await message.channel.send( message.author.name + ", you do not have permission to use the end command." )
					return
				await message.channel.send( "Wheel of Fortune has ended. Returning to normal operations.\nPlayer scores from last game: " + WoFGame.getScores( message.guild ) )
				del WoFGame
				WoFActive = False
				config.GameActive = False
			elif split[1] == "nextword":
				whitelist = open( "settings/whitelist.txt", "r" )
				allowed = False
				for ids in whitelist:
					if ids == str( message.author.id ):
						allowed = True
				if not allowed:
					await message.channel.send( message.author.name + ", you do not have permission to use the nextword command." )
					return
				WoFGame.nextWord()
				await message.channel.send( "Word has been forcibly changed to " + WoFGame.getFormattedWord( WoFGame.getWord() ) + "." )
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
				whitelist = open( "settings/whitelist.txt", "r" )
				allowed = False
				for ids in whitelist:
					if ids == str( message.author.id ):
						allowed = True
				if not allowed:
					await message.channel.send( message.author.name + ", you do not have permission to use the start command." )
					return
				if config.GameActive:
					await message.channel.send( "Wheel of fortune cannot be activated at this time. Another game is currently in progress." )
					return
				try:
					WoFGame = WoF( [], getRandomWord(), [] )
					await message.channel.send( "WHEEL OF FORTUNE MODE ACTIVATED\nWord: " + WoFGame.getFormattedWord( WoFGame.getWord() ) )
				except Exception as e:
					await message.channel.send( "Something went wrong while choosing a random word: " + str( e ) )
