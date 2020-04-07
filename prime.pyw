import discord
import random

BadWords = [
	"communism",
	"china",
	"ussr",
	"stalin",
	"lennin",
	"putin",
	"vodka",
	"commie",
	"russia",
	"cuba",
	"vietnam",
	"mao",
	"castro",
	"bernie",
	"kim",
	"korea",
	"california",
	"red",
	"cyka",
	"blyat",
	"communist",
	"gulag",
	"chinese",
	"vietnamese",
	"korean",
	"californian",
	"reds",
	"communists",
	"gulags",
	"vodkas",
	"blizzard"
]

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

class MyClient( discord.Client ):
	async def on_ready( self ):
		randfallout = str( random.randint( 3, 4 ) )
		await client.change_presence( activity = discord.Game( name = "Fallout " + randfallout ) )
		print( 'Logged in as {0}!'.format( self.user ) )

		for chan in client.get_all_channels():
			if chan.name == "general-kenobi":
				await chan.send( "LIBERTY PRIME IS ONLINE." )
				break
			if chan.name == "general":
				await chan.send( "LIBERTY PRIME IS ONLINE." )

	async def on_message( self, message ):
		if message.author.bot: return
		if "hong kong" in message.content.lower():
			await message.channel.send( "LIBERATE HONG KONG, REVOLUTION OF OUR AGE!" )
			return
		for item in BadWords:
			if item in message.content.lower():
				await message.channel.send( Quotes[ random.randint( 0, len( Quotes ) ) ].upper() )
				break

try:
	token = open( "token.txt" )
	client = MyClient()
	client.run( token.read() )
except:
	print( "Failed to open token file. File doesn't exist." )