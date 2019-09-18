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
            const m1 = await message.channel.send("Working...");
             PythonShell.run('./scrape_script.py', null, function (err,res) {
                if (err) throw err;
                console.log('finished')
                m1.edit(res[0])
                console.log(res);
            });
            break;
        case "reset":
            const m2 = await message.channel.send("Working...");
                PythonShell.run('./reset_script.py', null, function (err,res) {
                if (err) throw err;
                console.log('finished')
                m2.edit(res[1])
                console.log(res);
            });
            break;
        case "leaderboard":
                PythonShell.run('./leaderboard_script.py', null, async function (err,res) {
                if (err) throw err;
                console.log('finished')
              var newres1 = res[0].replace(/!@£%&/gi, '\n');
              var newres2 = res[1].replace(/!@£%&/gi, '\n');
                message.channel.send({embed: {
                    color: 3447003,
                    title: "Corner shop bois:",
                    fields: [
                      { name: "Players", value: newres1, inline: true},
                      { name: "Scores", value: newres2, inline: true}
                    ]
                  }
                });
            });
            break;

        default:
            message.channel.send(`Sorry, I don't quite understand what you're asking.`);
            
    }

   });

bot.login(config.token);