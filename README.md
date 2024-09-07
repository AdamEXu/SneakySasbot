# Sneaky SasBot

A Discord bot with a simple economy system and a few other fun commands.
**If you encounter any issues, please DM @thetnter on Discord.**
To suggest features, get support, or use the bot with many other members, join our Discord server [here](https://discord.gg/3cqm3kzuGQ)!

The prefix for this bot is `|`. You can also mention the bot, or use `Sneak` (or sneak or SNEAK) or `ss` as a prefix. Examples:

```
|shop
@Sneaky SasBot inv
sneak bal
Ss stats
```

## Commands

- `|help` - Displays a list of commands.
- `|bal` - Displays your balance.
- `|work` - Gain some money by working. There is a cooldown depending on selected job.
- `|shop` - Displays the shop. You can also use `|shop <category>` to display items from the category rather than using the menu.
- `|buy <item>` - Buy an item from the shop.
- `|inv` - Displays your inventory.
- `|jobs` - Displays a list of jobs you can work as. You will see which jobs are available and apply for them.
- `|use <item>` or `|eat <item>` - Eats a food item
- `|stats` - Displays your stats from three categories: Economy, Work, and Misc.
- `|settings` - Allows you to change a few settings:
  This is a work in progress, so more commands will be added in the future.

## Changelog

- **v0.1.0** - Initial release. Added economy system with balance, shop, inventory, and work commands. Added jobs command.
- **v0.2.0** - Improved shop, fixed many errors in commands, and improved error handling. Also, added the food meter.
- **v0.3.0** - Special shop release! Now you can upgrade your bank account and food meter. Vehicles are working now!
- **v0.4.0** - You can now use certain commands on other users.
- **v0.5.0** - Added some behind the scenes stat counters, but they're not ready to release yet (a lot of places where it isn't counting!)
- **v0.5.1** - Looks like the stat counters broke a ton of stuff so it should be good to go now!
- **v0.5.2** - More fixing of stat counters haha.
- **v0.5.3** - Some jobs were affected by the stat counter change.
- **v0.5.4** - Patched up a lot of holes where it wouldn't count stats.
- **v1.0.0** - First release! New bot account because couldn't figure out how to get some things working on the old account haha.
- **v1.0.1** - Fixed a ton of rounding errors throughout the bot
- **v1.1.0** - FIRST MAJOR UPDATE! Many new features released:
  - New `|stats` command to see your stats.
  - New `|settings` command to edit some portions of the bot's functionality.
  - The game's bad word filter was also imported into the bot as a funny setting.
  - A few new stat counters (these will be at 0)
- **v1.1.1** - Added new Bank Interest DM setting
- **v1.1.2** - Improved migration throughout the bot
- **v1.2.0** - Small QOL changes that were requested:
  - New ping after work cooldown setting in `|settings`
  - Improved embeds throughout the bot

## Progress

- [x] Economy system
- [x] Shop
- [x] Inventory
- [x] Work
- [x] Jobs
- [x] Vehicles (implemented into shop but not yet functional)
- [x] Food bar
- [x] Bank
- [x] Special shop
- [x] Settings
- [x] Stats UI
- [ ] Better more engaging work
- [ ]
- [ ] Meme command
- [ ] Speedrun.com leaderboard API lookup command
- [ ] More coming soon!

Suggest stuff on my Discord server! [JOIN HERE!](https://discord.gg/3cqm3kzuGQ)

This is just a list of ideas that will be implemented in the near future. If you have any suggestions, feel free to let me know!

## Credits

- **Sneaky Sasquatch** - Inspiration for the bot's name and economy system.
- **[discord.py](https://github.com/Rapptz/discord.py)** - I HATE discord.py. But stupid me from a few days ago decided to use it. So I either have to rewrite the entire bot or just keep using it. I'm going to keep using it. But I still hate it. I REALLY REALLY hate discord.py. I wish that I had used something else. I also regret not using slash commands. How hard could they have been to implement?

## Installation

First, clone the repository.

```bash
git clone https://github.com/Speedrun
```

Then, install the required packages.

```bash
pip install -r requirements.txt
```

Now, get a bot token from Discord's developer portal, and set it into the enviroment variable.

```bash
export TOKEN=1234567890HACK.CLUBARCADE.WWWWWWWWWWWWWWWWWWWWW
```

Finally, run the bot.

```bash
python app.py
```

Alternatively, just add the bot to your server using [this link](https://discord.com/oauth2/authorize?client_id=1272666435063251057&permissions=8&integration_type=0&scope=bot). Sorry about the admin permissions, I'll figure out which ones I actually need when I actually finish the bot. Additionally, I have not put it onto a VPS yet so it'll be down 90% of the time as of right now. However, that will change in the future.
