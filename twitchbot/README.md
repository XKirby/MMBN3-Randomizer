Mega Man Battle Network 3 VBA-RR Twitch Chat Interaction Bot
============
This bot is a set of Lua scripts that are utilized by VBA-RR. It allows Twitch Chat to interact with your game in real-time!

Requirements
============
VBA-RR
A Twitch Account (preferrably two, if you want a seperate bot from your personal account)
The Bot Account's OAuth Token (Don't share this with anyone!)

Setup
============
First, make sure you have the latest version of VBA-RR, which can be found here: https://github.com/TASVideos/vba-rerecording/releases

Next, download the "twitchbot" directory as a zip file with the "Clone or Download" button.

After that, find where you've downloaded and installed VBA-RR. Make sure there's a folder named "lua" in the same directory as the executable. Extract all of the files in the "twitchbot" folder into "lua" folder.

Once you've done all of that, you'll need to edit "twitchsettings.txt". It's technically a lua script that houses the program's configurable variables. Under the "TwitchBotVars" dictionary, you'll want to edit the values for "Channel", "Name", and "OAuth". To get an OAuth Token for your Twitch account, go here (and don't share your OAuth Token with ANYONE): https://twitchapps.com/tmi/

Feel free to configure the rest of the file however you want.

Running the Script
============
All you need to run the script is to open VBA-RR and go to Tools > Lua Scripting > New Lua Script Window... And then browse for and run "BN3 Slot-In + Twitch Bot.lua". Once you run it, the game may stutter a bit while connecting (and maybe while attempting to stay connected? Not sure.)

Known Issues
============
Most of these bugs are due to handling Battle Chips manually with the script during combat.
- Battle Chips can get eaten without activating during combat if you press A during movement or time stop.
- If you die, the bot has a tendency to disconnect. Restarting the bot fixes this.
- If no one's talking to using commands, the bot has a tendency to disconnect. Restarting the bot fixes this.
- If the bot produces an error, it stops. Just restart it.