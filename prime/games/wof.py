import requests
import json
import random
import asyncio
from games import config, base
from discord.ext import commands

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

global WoFActive
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
			self.tries = max( min( self.tries - 1, float( 'inf' ) ), 0 )

		def outOfTries( self ):
			return self.tries <= 0

		def addCorrect( self, correct ):
			self.correct += correct

		def setCorrect( self, correct ):
			self.correct = correct

		def getCorrect( self ):
			return self.correct

class WoFCommands( commands.Cog ):
	def __init__( self, bot ):
		self.bot = bot

	def initPlayer( self, ctx ):
		global MessagePlayer
		WoFGame.createPlayer( WoF.WoF_Player( ctx.message.author.id, 0, 5, 0 ) )
		MessagePlayer = WoFGame.getPlayerByID( ctx.message.author.id )

	@commands.group( invoke_without_command = True, ignore_extra = True )
	async def wof( self, ctx ):
		await ctx.send( "List of available Wheel of Fortune commands: start, guessletter, guessword, end, nextword, buyguesses" )

	@wof.command()
	async def guessletter( self, ctx, arg1 ):
		if not WoFActive:
			await ctx.send( "Wheel of Fortune is currently not active." )
			return
		if not arg1.isalpha() or len( arg1 ) > 1:
			await ctx.send( "Please input a single letter for the guessletter command." )
			return
		if arg1.lower() in WoFGame.getLetters():
			await ctx.send( "Letter '" + arg1.upper() + "' has already been guessed." )
			return
		if MessagePlayer.outOfTries():
			await ctx.send( "<@" + str( ctx.message.author.id ) + ">\nYou are out of letter guesses!" )
			return
		self.initPlayer( ctx )
		WoFGame.addLetter( arg1 )
		if arg1 in WoFGame.getWord():
			MessagePlayer.addCorrect( 1 )
			await ctx.send( "<@" + str( ctx.message.author.id ) + "> has guessed a letter correctly!\nGuessed letters so far: " + WoFGame.getFormattedWord( WoFGame.getWord() ) )
			if MessagePlayer.getCorrect() >= 3:
				MessagePlayer.addPoints( 1 )
				MessagePlayer.setCorrect( 0 )
				await ctx.send( "<@" + str( ctx.message.author.id ) + "> has guessed 3 correct letters and earned 1 point!" )
		else:
			MessagePlayer.removeTry()
			await ctx.send( "Letter '" + arg1.upper() + "' is not in this word. <@" + str( ctx.message.author.id ) + "> has " + str( MessagePlayer.getTries() ) + " guesses left." )

	@wof.command()
	async def guessword( self, ctx, arg1 ):
		if not WoFActive:
			await ctx.send( "Wheel of Fortune is currently not active." )
			return
		if not arg1.isalpha():
			await ctx.send( "Please input a word without numbers or special characters." )
			return
		self.initPlayer( ctx )
		if arg1.lower() == WoFGame.getWord().lower():
			await ctx.send( "<@" + str( ctx.message.author.id ) + "> has guessed the correct word and received 1 point!" )
			MessagePlayer.addPoints( 1 )
			WoFGame.nextWord()
			await ctx.send( "Next word: " + WoFGame.getFormattedWord( WoFGame.getWord() ) )
		else:
			MessagePlayer.removePoints( 1 )
			await ctx.send( "<@" + str( ctx.message.author.id ) + "> has incorrectly guessed the word and lost 1 point!" )

	@commands.has_permissions( administrator = True )
	@wof.command()
	async def end( self, ctx ):
		global WoFActive
		global WoFGame
		if not WoFActive:
			await ctx.send( "Wheel of Fortune is currently not active." )
			return
		await ctx.send( "Wheel of Fortune has ended. Returning to normal operations.\nPlayer scores from last game: " + WoFGame.getScores( ctx.message.guild ) )
		del WoFGame
		WoFActive = False
		config.GameActive = False

	@commands.has_permissions( administrator = True )
	@wof.command()
	async def nextword( self, ctx ):
		if not WoFActive:
			await ctx.send( "Wheel of Fortune is currently not active." )
			return
		oldword = WoFGame.getWord()
		WoFGame.nextWord()
		await ctx.send( "The word has been forcibly changed. It was `" + oldword + "`. New word: " + WoFGame.getFormattedWord( WoFGame.getWord() ) )

	@wof.command()
	async def buyguesses( self, ctx ):
		if not WoFActive:
			await ctx.send( "Wheel of Fortune is currently not active." )
			return
		if MessagePlayer.getPoints() < 1:
			await ctx.send( "<@" + str( ctx.message.author.id ) + ">\nYou don't have enough points to buy more guesses." )
			return
		self.initPlayer( ctx )
		MessagePlayer.removePoints( 1 )
		MessagePlayer.setTries( MessagePlayer.getTries() + 3 )
		await ctx.send( "<@" + str( ctx.message.author.id ) + "> has purchased 3 more guesses for 1 point." )

	@wof.command()
	async def start( self, ctx ):
		if config.GameActive:
			await ctx.send( "Wheel of fortune cannot be activated at this time. Another game is currently in progress." )
			return
		try:
			global WoFGame
			WoFGame = WoF( [], getRandomWord(), [] )
			self.initPlayer( ctx )
			await ctx.send( "WHEEL OF FORTUNE MODE ACTIVATED\nWord: " + WoFGame.getFormattedWord( WoFGame.getWord() ) )
		except Exception as e:
			await ctx.send( "Something went wrong while choosing a random word: " + str( e ) )

def setup( bot ):
	bot.add_cog( WoFCommands( bot ) )
