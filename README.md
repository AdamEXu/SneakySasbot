# Sneaky SasBot
A Discord bot with a simple economy system and a few other fun commands.

The prefix for this bot is `|`. You can also mention the bot, or use `Sneak` (or sneak or SNEAK) as a prefix. Examples:
```
|shop
@Sneaky SasBot inv
sneak bal
```

## Commands
- `|help` - Displays a list of commands.
- `|bal` - Displays your balance.
- `|work` - Gain some money by working. There is a cooldown depending on selected job.
- `|shop` - Displays the shop. You can also use `|shop <category>` to display items from the category rather than using the menu.
- `|buy <item>` - Buy an item from the shop.
- `|inv` - Displays your inventory. (Currently only shows food items)
- `jobs` - Displays a list of jobs you can work as. You will see which jobs are available, how many coins they earn, and what their cooldown is. You can then apply for a job using a specific amount of coins.
This is a work in progress, so more commands will be added in the future.

## Changelog
- **v1.0.0** - Initial release. Added economy system with balance, shop, inventory, and work commands. Added jobs command.

## Progress
- [x] Economy system
- [x] Shop
- [x] Inventory
- [x] Work
- [x] Jobs
- [-] Vehicles (implemented into shop but not yet functional)
- [ ] Food bar
- [ ] Bank
- [ ] Special shop
- [ ] Meme command
- [ ] Speedrun.com leaderboard API lookup command
- [-] More coming soon!

[ ] = Not yet implemented, [-] = In progress, [x] = Completed

This is just a list of ideas that will be implemented in the near future. If you have any suggestions, feel free to let me know!

## Credits
- **Sneaky Sasquatch** - Inspiration for the bot's name and economy system.
- **[discord.py](https://github.com/Rapptz/discord.py)** - I HATE discord.py. But stupid me from a few days ago decided to use it. So I either have to rewrite the entire bot or just keep using it. I'm going to keep using it. But I still hate it. I REALLY REALLY hate discord.py. I wish that I had used something else. I also regret not using slash commands. How hard could they have been to implement?