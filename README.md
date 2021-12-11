Mega Man Battle Network 3 Randomizer
============
This is a Python 3 64-bit application with a bunch of text files used for randomizing Mega Man Battle Network 3. I've taken some liberties to make it more interesting to use. Credit goes to Mountebank/Samfin, Dabomstew, Prof.9, Rockman.EXE, and potentially other people I don't know about/forgot for the original MMBN3 Randomizer.

Credit to /u/Zinthonian from Reddit for the executable icon.

Please refer to the Instructions.txt for how to use this program.

Also included is a tool for adding new NaviCustomizer Program Shapes to the list of shapes for the randomizer and various notes for how the game stores information. This was made in GameMaker Studio.

Compilation
============
To compile, I've included a .bat file to run Python 3 64-bit's version of PyInstaller with a custom icon for the program. It will make 2 executables in a "dist" folder. "bn3cl" is a command line version, while "bn3ui" is the graphical user interface version.

Features
============
- Supports both Version White and Version Blue! Thanks, Hart-Hunt!
- The original randomizer featured randomizing of Numberman Code Prizes that give Battle Chips, Battle Chip Folders, Green Mystery Data, and Virus Formations. Those are still here!
- Lots of text files. They hold a bunch of data that you can mess around with to some extent. Just be sure to back things up in case something goes wrong.
- Various modifiers are asked of you right off the bat when opening the script. These include Battle Chip Damage and Enemy HP Multipliers and Variance Values, as well as a Custom Run seed and a "Chip Code Roulette" Mode!
- If a Run Seed is not supplied, it will generate one based on the current time.
- More details can be found in Instructions.txt.

Known Issues/Caveats
============
- The rom must be a clean US copy of Mega Man Battle Network 3.
- Messing with things in ways you probably shouldn't mess with can lead to errors, crashing, corrupt ROMs, etc. I take no responsibility for any of this.

ROM Checksums
============
These checksums are from a clean MMBN3 White rom. If you're going to use this randomizer, you'll need a rom that has these checksums.
- CRC32: 0BE4410A
- MD5: 68817204A691449E655CBA739DBB0165

These checksums are from a clean MMBN3 Blue rom. If you're going to the use this randomizer, you'll need a rom that has these checksums.
- CRC32: C0C780F9
- MD5: 6FE31DF0144759B34AD666BADAACC442

Open Mode Patches
============
These patches can be used if you want to experience the game in a different way. Make sure to patch the rom with the correct patch BEFORE randomizing it! The features of these patches are listed below.
- ~~A built-in Full Library code! This took a while to figure out.~~ *(This has been recently disabled.)*
- Every area of the game should be open to the player right off the bat.
- You start the game with every email, access to the NaviCust and StyleChange menus, as well as some NCP programs and Key Items for access to various areas.
- Style Changes happen more frequently.
- You have 4 out of the 7 Savefile Stars unlocked right off the bat! No need to fight Serenade, the Omega Navis, or do the Time Trials unless you want to.
- Code for most of this new version of the Open Mode patch provided by NMarkro, a member of TeamBN. Thanks again!

The Open Mode patches, either in combination with the Randomizer or not, can be used for various types of play. Here are a few ideas:
- Bingo Races
- Alpha or Serenade Races
- Time Trial Races or Practice

HP Unlimiter Patches
============
These patches break the internal HP limit of Navis and Viruses from 4096 to 65536! The last bit of their HP is normally their Element. This patch moves their Element to unused space in the ROM and allows the 4th bit to be used as HP. There's an option in the Randomizer to take this into account. Using this option does the following:

- Allows for unrestricted Damage and HP Multiplier values! (Don't go crazy please...)
- It will write the enemy's Element to the space I've provided in the ROM that the patch uses. Without the patch, this setting leads to some weird behavior. Keep this in mind.
- You may rebalance the game's Chips and HP values with the included Text Files that store their stats! (Again, don't go overboard. And don't change anything you don't understand.)
- Chip Damage is capped at 9999, or at least close to it. At 10000+, the damage value is set to "????" visually and will no longer be randomized properly.

These patches are no longer required due to a recent update allowing the "Ignore HP/Damage Limiters" Setting in the randomizer to apply the patch's features directly.

Changes from the original
============
- Removal of the VarSwrd power decrease by default.
- Addition of Command Line Properties and Options for the original program.
- Addition of a GUI version of the program using PAGE. (To be honest, I should probably use something else.)
- Addition of randomized Battle Chip Damage, Program Advance Damage, and Virus/Navi HP Randomization.
- Addition of Battle Chip Code Modes, to change the Chip Codes throughout the game.
- Addition of various .txt files that store data, with an Instructions.txt that includes info on how to mess/not mess with them.
- Addition of seed input and an extremely detailed Output Log and hash, for speedrunning/races.
- Addition of randomizable Chip/PA and Virus/Navi Names.
- Addition of full support for MMBN3 Blue.
- Addition of NaviCust Shape Randomization features.
- Addition of Element Randomization.
- Addition of Battlefield Randomization.
- Addition of Virus Difficulty Levels.
- Addition of Randomized Blue Mystery Datas. (It's not perfect, but it's there.)
- Addition of Randomized NPC Trade Requirements. (Again, not perfect.)
- Addition of more difficult Hell Mode Settings. Original Hell Mode also included.
- Compiled the program into an executable for people who don't have Python 3.
- Support for the included Open Mode Patch, even when using the "Ignore HP/Damage Limiters" option. (Patch before randomizing!)
