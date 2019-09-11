const Discord = require("discord.js");

// Initialize Discord Bot
const bot = new Discord.Client({forceFetchUsers: true});
const config = require("./config.json");
let {PythonShell} = require('python-shell')


//Initial setup
bot.on("ready", () => {
   console.log(`Bot has started!`);
});

//Chat commands, message replies
bot.on("message", async message => {
   if (message.content.indexOf(config.prefix) !== 0) return;
   const args = message.content.slice(config.prefix.length).trim().split(/ +/g);
   const command = args.shift().toLowerCase();
  // message.delete(1000);
   //console.log(JSON.stringify(message))
   

   switch (command) {
        // Generic PING command
        case "ping":
            const m = await message.channel.send("Ping?");
            
            m.edit(`Pong! Latency is ${m.createdTimestamp - message.createdTimestamp}ms. API Latency is ${Math.round(bot.ping)}ms `);
            message.delete(1000);
            console.log(message.channel.id)
            console.log(message.id)
            break;
        case "scrape":
            //var PythonShell = require('python-shell');
            const m1 = await message.channel.send("Working...");
           //var array = JSON.parse("{\"343801\": [1006, \"NeoN\"], \"590859\": [982, \"Yajul\"], \"639335\": [989, \"Ponobi\"], \"621772\": [1012, \"✪[Louis] ・ヤ・✪\"], \"639355\": [999, \"whipped\"], \"590843\": [987, \"✪[Shurfey]自分を信じます！✪\"], \"639336\": [963, \"Chicken God\"], \"459248\": [1002, \"PATAKS GLORIOUS JUICES\"], \"951790\": [966, \"Philenc\"], \"482444\": [1002, \"snuld\"], \"718053\": [999, \"LoCo|StetoGuy中国\"], \"590839\": [991, \"TC SILVER\"], \"639339\": [973, \"Mízt\"], \"471690\": [991, \"JawadJ\"], \"146466\": [991, \"null\"], \"590836\": [989, \"null\"], \"639340\": [991, \"null\"], \"268179\": [993, \"null\"], \"670589\": [998, \"null\"], \"782008\": [1003, \"null\"], \"459247\": [1003, \"null\"], \"834099\": [1003, \"null\"]}")
           // console.log(array)
             PythonShell.run('./scrape_script.py', null, function (err,res) {
                if (err) throw err;
                console.log('finished')
                m1.edit(res[1])
                message.channel.send(res[3])
                //message.channel.send(JSON.stringify(JSON.parse(res[3])));
                console.log(res);

            });
            break;

        default:
            message.channel.send(`Sorry, I don't quite understand what you're asking.`);
            
    }

   });

bot.login(config.token);