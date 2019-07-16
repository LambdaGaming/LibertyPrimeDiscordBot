
require('dotenv').config()

const Discord = require('discord.js')
const client = new Discord.Client()
const badwords = [
	"communism",
	"china",
	"ussr",
	"stalin",
	"lennin",
	"putin",
	"vodka",
	"commie"
]
const quotes = [
	"DEATH IS A PREFERRABLE ALTERNATIVE TO COMMUNISM!"
]

client.on('ready', () => {
	console.log( `Logged in as ${client.user.tag}!` )
	client.user.setActivity( 'Fallout 3' )
})

client.on( 'message', msg => {
	var usertag = msg.member.id
	var split = msg.content.split( " " )
	for( i=0; i < split.length; i++ ){
		if( usertag == process.env.BOT_ID ){
			return
		}
		console.log( split[i] )
		if( badwords.includes( split[i].toLowerCase() ) ){
			msg.channel.send( quotes[ Math.floor( Math.random() * quotes.length ) ] )
		}
	}
} )

client.login( process.env.BOT_TOKEN )