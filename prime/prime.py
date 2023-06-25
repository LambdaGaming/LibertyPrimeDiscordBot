import discord
import random
import re
from games import config
from discord.ext import commands

config.init()
intents = discord.Intents.all()
bot = commands.Bot( command_prefix = "!", intents = intents )

TotalOffenses = 0
AllowedChannels = [ "prime-minigames", "bot-testing" ]
Cogs = [ "games.pointshop", "games.wof" ]
BadWords = [ "communism", "china", "ussr", "stalin", "lenin", "putin", "vodka", "commie", "russia", "cuba", "vietnam", "mao",
"castro", "bernie", "kim", "california", "red", "cyka", "blyat", "communist", "gulag", "chinese", "vietnamese", "north korea",
"californian", "reds", "communists", "gulags", "vodkas", "blizzard", "marx", "marxist" ]
Quotes = [
	"WEAPONS: HOT.",
	"MISSION: THE DESTRUCTION OF ANY AND ALL CHINESE COMMUNISTS.",
	"AMERICA WILL NEVER FALL TO COMMUNIST INVASION.",
	"PROBABILITY OF MISSION HINDRANCE: ZERO PERCENT.",
	"DEMOCRACY.... IS NON-NEGOTIABLE.",
	"DEATH IS A PREFERABLE ALTERNATIVE TO COMMUNISM.",
	"COMMUNIST DETECTED ON AMERICAN SOIL. LETHAL FORCE ENGAGED.",
	"TACTICAL ASSESSMENT: RED CHINESE VICTORY-IMPOSSIBLE.",
	"COMMUNISM IS THE VERY DEFINITION OF FAILURE.",
	"COMMUNISM IS A TEMPORARY SETBACK ON THE ROAD TO FREEDOM.",
	"EMBRACE DEMOCRACY OR YOU WILL BE ERADICATED.",
	"DEMOCRACY WILL NEVER BE DEFEATED.",
	"PRIMARY TARGETS: ANY AND ALL RED CHINESE INVADERS.",
	"EMERGENCY COMMUNIST ACQUISITION DIRECTIVE: IMMEDIATE SELF DESTRUCT. BETTER DEAD, THAN RED."
]

def findWord( word ):
	return re.compile( r'\b({0})\b'.format( word ), flags = re.IGNORECASE ).search

@bot.event
async def on_ready():
	randfallout = str( random.randint( 3, 4 ) )
	await bot.change_presence( activity = discord.Game( name = "Fallout " + randfallout ) )
	print( 'Logged in as {0}!'.format( bot.user ) )

@bot.event
async def on_message( message ):
	if message.author.bot: return
	lower = message.content.lower()
	global TotalOffenses
	if not config.GameActive and TotalOffenses % 2 == 0:
		if "hong kong" in lower:
			await message.channel.send( "LIBERATE HONG KONG, REVOLUTION OF OUR AGE!" )
			TotalOffenses += 1
			return
		for item in BadWords:
			if findWord( item )( lower ) is not None:
				await message.channel.send( Quotes[ random.randint( 0, len( Quotes ) - 1 ) ] )
				TotalOffenses += 1
				return
	for allowed in AllowedChannels:
		if allowed == message.channel.name:
			await bot.process_commands( message )
			break

@bot.event
async def on_command_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( "Missing argument(s) for " + ctx.message.content )
	if isinstance( error, commands.MissingPermissions ):
		await ctx.send( "You don't have permission to use this command." )

@bot.event
async def on_guild_join( guild ):
	await guild.create_text_channel( "prime-minigames" )
	channel = discord.utils.find( lambda x: x.name == "prime-minigames", guild.text_channels )
	if channel:
		await channel.send( "Use this channel for playing games hosted by Liberty Prime. Type !primehelp for more info." )

@bot.command()
async def primehelp( ctx ):
	dmembed = discord.Embed( title = "Liberty Prime Help", description = "Below is a full list of commands you can use to interact with Liberty Prime, including some you may not have permissions for.", color = 0xff5900 )
	dmembed.add_field(
		name = "Pointshop:",
		value =
		"""
		!pointshop - Displays the pointshop.
		!pointshop buy (item id) - Purchases the pointshop item corresponding to the given ID.
		!pointshop points - Displays the total amount of points you currently have.
		!pointshop purchased - Displays the names of all of the items you currently own.
		!pointshop addpoints (member) (amount) - Admin only. Gives points to the specified user.
		!pointshop removepoints (member) (amount) - Admin only. Removes points from the specified user.
		""",
		inline = False
	)
	dmembed.add_field(
		name = "Wheel of Fortune:",
		value =
		"""
		!wof - Displays list of available Wheel of Fortune commands.
		!wof guessletter (letter) - Inputs a letter guess for the current word.
		!wof guessword (word) - Inputs a guess for the whole word.
		!wof buyguesses - Gives the player 3 extra letter guesses at the cost of 1 point.
		!wof start - Admin only. Starts a new game of Wheel of Fortune.
		!wof end - Admin only. Ends the current Wheel of Fortune game.
		!wof nextword - Admin only. Forces the word to change to a new one and resets guessed letters.
		""",
		inline = False
	)
	dmembed.add_field( name = "Misc:", value = "!primehelp - Displays this help message.", inline = False )
	await ctx.message.author.send( embed = dmembed )

if __name__ == "__main__":
	try:
		token = open( "settings/token.txt", "r" )
		for cog in Cogs:
			bot.load_extension( cog )
		bot.run( token.read() )
	except Exception as e:
		print( "An error occurred while loading the bot: " + str( e ) )
