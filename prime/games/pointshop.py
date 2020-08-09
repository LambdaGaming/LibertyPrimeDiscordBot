import config
import discord
import json
import os

PointshopConfig = {
	1 : { # Item ID
		"name" : "CityRP: AR-15",
		"price" : 2,
		"desc" : "Fully automatic rifle that deals decent damage. Only obtainable in-game through crafting."
	},
	2 : {
		"name" : "CityRP: Shotgun",
		"price" : 4,
		"desc" : "Pump shotgun that deals great damage. Only obtainable in-game through crafting."
	},
	3 : {
		"name" : "CityRP: DarkRP Shotgun",
		"price" : 8,
		"desc" : "Pump shotgun that deals huge damage. Not obtainable in-game."
	},
	4: {
		"name" : "CityRP: Random Vehicle",
		"price" : 6,
		"desc" : "Random civilian vehicle worth less than 50k that you don't already own."
	},
	5 : {
		"name" : "SCP: Free 05",
		"price" : 2,
		"desc" : "Free 05 keycard given to you at the beginning of a round of your choice."
	},
	6 : {
		"name" : "SCP: Class of Choice",
		"price" : 3,
		"desc" : "You will become a class of your choice during a round of your choice."
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

def writeJSON( id, table ):
	path = "data/pointshop/" + id + ".json"
	try:
		getfile = open( path, "w" )
		getfile.write( json.dumps( table ) )
	except Exception as e:
		print( "Something went wrong while writing player data: " + e )

def listItems( table ):
	finalstr = ""
	for item in table:
		if table.index( item ) == 0:
			finalstr = PointshopConfig[item]["name"]
		else:
			finalstr += ", " + PointshopConfig[item]["name"]
	return finalstr

async def checkChatMessage( message ):
	split = message.content.split( " " )
	if split[0] == "!pointshop":
		if config.GameActive:
			message.channel.send( "Please wait until the current game is over before accessing the pointshop." )
			return
		shopembed = discord.Embed( title = "Liberty Prime's Pointshop", description = "Use !buy [item number] to buy items for the servers using points earned from minigames.", color = 0xff5900 )
		for k,v in PointshopConfig.items():
			shopembed.add_field( name = "[" + str( k ) + "] " + v["name"], value = "Price: " + str( v["price"] ) + "\nDescription: " + v["desc"], inline = False )
		await message.channel.send( embed = shopembed )
	elif split[0] == "!buy":
		if config.GameActive:
			message.channel.send( "Please wait until the current game is over before buying something from the pointshop." )
			return
		idint = int( split[1] )
		if 1 in range( -len( split ), len( split ) ) and not split[1].isalpha() and idint in PointshopConfig:
			author = str( message.author.id )
			price = PointshopConfig[idint]["price"]
			name = PointshopConfig[idint]["name"]
			if readfile["points"] < price:
				await message.channel.send( message.author.name + ", you don't have enough points to purchase the item '" + name + "'." )
				return
			readfile["points"] -= price
			readfile["purchased"].append( idint )
			writeJSON( author, readfile )
			await message.channel.send( message.author.name + ", you have purchased '" + name + "' for " + str( price ) + " point(s)." )
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
		await message.channel.send( message.author.name + ", you have purchased the following items: " + listItems( readfile["purchased"] ) )
