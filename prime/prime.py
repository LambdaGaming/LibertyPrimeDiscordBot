import discord
import random
from games import config
from discord.ext import commands

config.init()
bot = commands.Bot( command_prefix = "!" )

AllowedChannels = [ "prime-minigames", "bot-testing" ]
Cogs = [ "games.pointshop", "games.wof" ]
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

@bot.event
async def on_ready():
	randfallout = str( random.randint( 3, 4 ) )
	await bot.change_presence( activity = discord.Game( name = "Fallout " + randfallout ) )
	print( 'Logged in as {0}!'.format( bot.user ) )

@bot.event
async def on_message( message ):
	if message.author.bot: return
	lower = message.content.lower()

	if not config.GameActive:
		if "hong kong" in lower:
			await message.channel.send( "LIBERATE HONG KONG, REVOLUTION OF OUR AGE!" )
			return
		for item in BadWords:
			if item in lower:
				await message.channel.send( Quotes[ random.randint( 0, len( Quotes ) - 1 ) ].upper() )
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
