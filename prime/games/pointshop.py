import config
import discord
import json
import os

PointshopConfig = {
	1 : { # Page number (limit to 4 per page to reduce clutter)
		1 : { # Item ID
			"CityRP: AR-15" : "Price: 2 points\nDescription: Fully automatic rifle that deals decent damage. Only obtainable in-game through crafting." # Item name, price, and description
		},
		2 : {
			"CityRP: Shotgun" : "Price: 4 points\nDescription: Pump shotgun that deals great damage. Only obtainable in-game through crafting."
		},
		3 : {
			"CityRP: DarkRP Shotgun" : "Price: 8 points\nDescription: Pump shotgun that deals huge damage. Not obtainable in-game."
		},
		4: {
			"CityRP: Random Vehicle" : "Price: 6 points\nDescription: Random civilian vehicle worth less than 50k that you don't already own."
		}
	},
	2 : {
		5 : {
			"SCP: Free 05" : "Price: 2 points\nDescription: Free 05 keycard given to you at the beginning of a round of your choice."
		},
		6 : {
			"SCP: Class of Choice" : "Price: 3 points\nDescription: You will become a class of your choice during a round of your choice."
		}
	}
}

def getJSON( id ):
	path = "data/pointshop/" + id + ".json"
	if not os.path.exists( path ):
		os.makedirs( "data/pointshop" )
		getfile = open( path, "w" )
		getfile.write( """{"points" : 0, "purchased" : []}""" )
	getfile = open( path, "r" )
	readfile = json.load( getfile )
	return readfile

async def checkChatMessage( message ):
	split = message.content.split( " " )
	if split[0] == "!pointshop":
		if config.GameActive:
			message.channel.send( "Please wait until the current game is over before accessing the pointshop." )
			return
		index = int( split[1] ) if 1 in range( -len( split ), len( split ) ) and int( split[1] ) in PointshopConfig else 1
		shopembed = discord.Embed( title = "Liberty Prime's Pointshop (Page " + str( index ) + " of " + str( len( PointshopConfig ) ) + ")", description = "Use !buy [item number] to buy items for the servers using points earned from minigames.", color = 0xff5900 )
		for k,v in PointshopConfig[index].items():
			for a,b in v.items():
				shopembed.add_field( name = "[" + str( k ) + "] " + a, value = b, inline = False )
		await message.channel.send( embed = shopembed )
	elif split[0] == "!buy":
		if config.GameActive:
			message.channel.send( "Please wait until the current game is over before buying something from the pointshop." )
			return
		if 1 in range( -len( split ), len( split ) ) and not split[1].isalpha() and int( split[1] ) in PointshopConfig:
			readfile = getJSON( str( message.author.id ) )
			
		else:
			await message.channel.send( "Please enter a valid number as the item ID." )
	elif split[0] == "!points":
		readfile = getJSON( str( message.author.id ) )
		await message.channel.send( message.author.name + ", you currently have " + str( readfile["points"] ) + " point(s)." )
	elif split[0] == "!purchased":
		readfile = getJSON( str( message.author.id ) )
		if not readfile["purchased"]:
			await message.channel.send( message.author.name + ", you have not purchased anything." )
			return
		await message.channel.send( message.author.name + ", you have purchased the following items (Listed by their ID): " + str( readfile["purchased"] ) )
