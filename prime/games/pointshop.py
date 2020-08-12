import discord
import json
import os
from games import config, base
from discord.ext import commands

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

class Pointshop( commands.Cog ):
	def __init__( self, bot ):
		self.bot = bot

	@commands.group( invoke_without_command = True )
	async def pointshop( self, ctx ):
		if config.GameActive:
			ctx.send( "Please wait until the current game is over before accessing the pointshop." )
			return
		shopembed = discord.Embed( title = "Liberty Prime's Pointshop", description = "Use !pointshop buy [item number] to buy items for the servers using points earned from minigames.", color = 0xff5900 )
		for k,v in PointshopConfig.items():
			shopembed.add_field( name = "[" + str( k ) + "] " + v["name"], value = "Price: " + str( v["price"] ) + "\nDescription: " + v["desc"], inline = False )
		await ctx.message.author.send( embed = shopembed )

	@pointshop.command()
	async def buy( self, ctx, arg1 ):
		if config.GameActive:
			ctx.send( "Please wait until the current game is over before buying something from the pointshop." )
			return
		idint = int( arg1 )
		if not arg1.isalpha() and idint in PointshopConfig:
			author = str( ctx.message.author.id )
			readfile = getJSON( author )
			price = PointshopConfig[idint]["price"]
			name = PointshopConfig[idint]["name"]
			if readfile["points"] < price:
				await ctx.send( "<@" + author + ">\nYou don't have enough points to purchase the item '" + name + "'." )
				return
			readfile["points"] -= price
			readfile["purchased"].append( idint )
			writeJSON( author, readfile )
			await ctx.send( "<@" + author + ">\nYou have purchased '" + name + "' for " + str( price ) + " point(s)." )
		else:
			await ctx.send( "Please enter a valid number as the item ID." )

	@pointshop.command()
	async def points( self, ctx ):
		readfile = getJSON( str( ctx.message.author.id ) )
		await ctx.send( "<@" + str( ctx.message.author.id ) + ">\nYou currently have " + str( readfile["points"] ) + " point(s)." )

	@pointshop.command()
	async def purchased( self, ctx ):
		readfile = getJSON( str( ctx.message.author.id ) )
		if not readfile["purchased"]:
			await ctx.send( "<@" + str( ctx.message.author.id ) + ">\nYou have not purchased anything." )
			return
		await ctx.send( "<@" + str( ctx.message.author.id ) + ">\nYou have purchased the following items: " + listItems( readfile["purchased"] ) )

	@commands.has_permissions( administrator = True )
	@pointshop.command()
	async def addpoints( self, ctx, arg1: discord.User, arg2 ):
		if isinstance( arg1, discord.User ) and arg2.isdigit():
			plytemp = base.Player( arg1.id, 0 )
			plytemp.addPoints( int( arg2 ) )
			del plytemp
			await ctx.send( "<@" + str( ctx.message.author.id ) + "> gave <@" + str( arg1.id ) + "> " + arg2 + " point(s)." )
		else:
			await ctx.send( "Usage of addpoints command: !addpoints (member) (amount)" )

	@commands.has_permissions( administrator = True )
	@pointshop.command()
	async def removepoints( self, ctx, arg1: discord.User, arg2 ):
		if isinstance( arg1, discord.User ) and arg2.isdigit():
			plytemp = base.Player( arg1.id, 0 )
			plytemp.removePoints( int( arg2 ) )
			del plytemp
			await ctx.send( "<@" + str( ctx.message.author.id ) + "> took " + arg2 + " point(s) from <@" + str( arg1.id ) + ">." )
		else:
			await ctx.send( "Usage of removepoints command: !removepoints (member) (amount)" )

def setup( bot ):
	bot.add_cog( Pointshop( bot ) )
