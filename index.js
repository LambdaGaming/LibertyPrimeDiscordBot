
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
	"gulag"
]
const quotes = [
	"Weapons: hot.",
	"Mission: the destruction of any and all Chinese communists.",
	"America will never fall to communist invasion.",
	"Obstruction detected. Composition: titanium alloy supplemented by photonic resonance barrier.",
	"Probability of mission hindrance: zero percent.",
	"Democracy.... is non-negotiable.",
	"Death is a preferable alternative to communism.",
	"Communist detected on American soil. Lethal force engaged.",
	"Tactical assessment: Red Chinese victory—impossible.",
	"Communism is the very definition of failure.",
	"Communism is a temporary setback on the road to freedom.",
	"Embrace democracy or you will be eradicated.",
	"Democracy will never be defeated.",
	"Primary Targets: any and all Red Chinese invaders.",
	"Emergency Communist Acquisition Directive: immediate self destruct. Better dead, than Red."
]

client.on('ready', () => {
	console.log( `Logged in as ${client.user.tag}!` )
	client.user.setActivity( `Fallout ${Math.floor( Math.random() * ( 4 - 3 + 1 ) + 3 ).toString()}` )

	const channel = client.channels.find( channel => channel.name == "general" )
	const channel_meme = client.channels.find( channel => channel.name == "general-kenobi" )
	if( channel_meme ){
		channel_meme.send( "LIBERTY PRIME IS ONLINE." )
	}
	else if( channel ){
		channel.send( "LIBERTY PRIME IS ONLINE." )
	}
})

var cooldown = 0
client.on( 'message', msg => {
	var usertag = msg.member.id
	var split = msg.content.split( " " )
	if( cooldown > Date.now() ){
		return
	}
	for( i=0; i < split.length; i++ ){
		if( usertag == process.env.BOT_ID ){
			return
		}
		if( badwords.includes( split[i].toLowerCase() ) ){
			msg.channel.send( quotes[ Math.floor( Math.random() * quotes.length ) ].toUpperCase() )
		}
	}
	cooldown = Date.now() + 1
} )

client.login( process.env.BOT_TOKEN )