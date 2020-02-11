import discord
import random

class MyClient( discord.Client ):
    async def on_ready( self ):
        randfallout = str( random.randint( 3, 4 ) )
        await client.change_presence( activity = discord.Game( name = "Fallout " + randfallout ) )
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author.bot: return
        if message.content == "!primetest":
            await message.channel.send( "LIBERTY PRIME TEST SUCCESSFUL" )

try:
    token = open( "token.txt" )
    client = MyClient()
    client.run( token.read() )
except:
    print( "Failed to open token file. Make sure your path is correct." )