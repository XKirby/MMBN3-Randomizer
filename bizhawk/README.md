Mega Man Battle Network 3 Bizhawk Scripts
============
This is a set of Lua scripts that are utilized via Bizhawk's mGBA core.
The Twitch Bot script allows Twitch Chat to interact with your game in real-time!
The Folder Editor script allows you to make Folder Setups for the Randomizer and export them from within the game!

Twitch Bot Script Requirements
============
Bizhawk and its prerequisite installer
A Twitch Account (preferrably two, if you want a seperate bot from your personal account)
The Bot Account's OAuth Token (Don't share this with anyone!)
Optionally a GBA BIOS (if you plan to use the Panic Battle Chip)
A set of included lua scripts for reading various data within the games and to connect to Twitch's IRC channels

Folder Editor Script Requirements
============
Bizhawk

Twitch Bot Script Setup
============
First, make sure you have the latest version of Bizhawk, which can be found here: https://tasvideos.org/Bizhawk

Next, download the "twitchbot" directory as a zip file with the "Clone or Download" button.

After that, find where you've downloaded and installed VBA-RR. Make sure there's a folder named "lua" in the same directory as the executable. Extract all of the files in the "twitchbot" folder into "lua" folder.

Once you've done all of that, you'll need to edit "twitchsettings.txt". It's technically a lua script that houses the program's configurable variables. Under the "TwitchBotVars" dictionary, you'll want to edit the values for "Channel", "Name", and "OAuth". To get an OAuth Token for your Twitch account, go here (and don't share your OAuth Token with ANYONE): https://twitchapps.com/tmi/

Feel free to configure the rest of the file however you want.

Folder Editor Script Setup
============
Go into the in-game Folder Editing screen. From there, these buttons can be used on chips that are in your folder:
- A: Highlight Chip
- B: Cancel
- Start: If you have a Chip highlighted, enter Edit Mode
- Select: If you have a Chip highlighted while *not* in Edit Mode, display Folder info

While in Edit Mode, you can use the following buttons:
- B: Cancel
- L/R: Change Chip ID
- DPad Left/Right: Change Code ID
- Select: Export Folder for use with Randomizer

Running the Scripts
============
There's a Lua Script Console within Bizhawk that can run multiple scripts at a time. I suggest only running one of these at a time however.

Twitch Bot Known Issues
============
Most of these bugs are due to handling Battle Chips manually with the script during combat.
- If you die, the bot has a tendency to disconnect. Restarting the bot fixes this.
- If no one's talking or using commands, the bot has a tendency to disconnect. Restarting the bot fixes this.
- If the bot produces an error, it stops. Just restart it.