import discord
import random
from games import config
from discord.ext import commands

config.init()
bot = commands.Bot( command_prefix = "!" )

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
	await bot.process_commands( message )

@bot.event
async def on_command_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( "Missing argument(s) for " + ctx.message.content )
	if isinstance( error, commands.MissingPermissions ):
		await ctx.send( "You don't have permission to use this command." )

if __name__ == "__main__":
	try:
		token = open( "settings/token.txt", "r" )
		for cog in Cogs:
			bot.load_extension( cog )
		bot.run( token.read() )
	except Exception as e:
		print( "An error occurred while loading the bot: " + str( e ) )
