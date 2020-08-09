import discord
import random
import config
from games import wof, pointshop

config.init()

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

class MyClient( discord.Client ):
	async def on_ready( self ):
		randfallout = str( random.randint( 3, 4 ) )
		await client.change_presence( activity = discord.Game( name = "Fallout " + randfallout ) )
		print( 'Logged in as {0}!'.format( self.user ) )

	async def on_message( self, message ):
		if message.author.bot: return
		lower = message.content.lower()

		await pointshop.checkChatMessage( message )
		await wof.checkChatMessage( message ) # Check to see if the chat sent is for a minigame

		if not config.GameActive:
			if "hong kong" in lower:
				await message.channel.send( "LIBERATE HONG KONG, REVOLUTION OF OUR AGE!" )
				return
			for item in BadWords:
				if item in lower:
					await message.channel.send( Quotes[ random.randint( 0, len( Quotes ) - 1 ) ].upper() )
					break

try:
	token = open( "settings/token.txt", "r" )
	client = MyClient()
	client.run( token.read() )
except Exception as e:
	print( "An error occurred while reading the token file: " + str( e ) )
