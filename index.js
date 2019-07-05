
require('dotenv').config()

const Discord = require('discord.js')
const client = new Discord.Client()

client.on('ready', () => {
	console.log( `Logged in as ${client.user.tag}!` )
	client.user.setActivity( 'CityRP on rp_rockford_v2b' )
})

client.on( 'message', msg => {
	if( msg == "/lockdown" ){
		msg.channel.send( '```diff\n-The mayor has initiated a lockdown! Remain indoors until the lockdown is over.\n```' )
	}
} )

client.login( process.env.BOT_TOKEN )