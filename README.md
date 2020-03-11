Mega Man Battle Network 3 Randomizer
============

Original Python 2.7 script written by Samfin/Mountebank.
Credit to X Kirby for the following changes:

- Removal of the VarSwrd power decrease by default.
- Addition of Command Line Properties and Options for the original program.
- Addition of a GUI version of the program using PAGE. (To be honest, I should probably use something else.)
- Addition of randomized Battle Chip Damage, Program Advance Damage, and Virus/Navi HP Randomization.
- Addition of Battle Chip Code Modes, to change the Chip Codes throughout the game.
- Addition of various .txt files that store data, with a NOTES.txt that includes info on how to mess/not mess with them.
- Addition of seed input and an extremely detailed Output Log and hash, for speedrunning/races.
- Addition of randomizable Chip/PA and Virus/Navi Names.
- Addition of full support for MMBN3 Blue.
- Addition of NaviCust Shape Randomization features.
- Addition of Element Randomization.
- Addition of Battlefield Randomization.
- Addition of Virus Difficulty Levels.
- Addition of Randomized Blue Mystery Datas. (It's not perfect, but it's there.)
- Addition of Randomized NPC Trade Requirements. (Again, not perfect.)
- Addition of a much more difficult Hell Mode. Original Hell Mode also included.
- Compiled the program into an executable for people who don't have Python 2.7.
- Support for both the included Open Mode and HP Unlimiter Patches, even if used on the same rom. (Patch before randomizing!)

Credit to /u/Zinthonian from Reddit for the executable icon.

Please refer to the Instructions.txt for how to use this program.

Also included is a tool for adding new NaviCustomizer Program Shapes to the list of shapes for the randomizer and various notes for how the game stores information.

============

To compile, I've included a .bat file to run Python 2.7's version of PyInstaller with a custom icon for the program. It will make 2 executables with their own resources in their own folders. "bn3cl" is a command line version, while "bn3ui" is the graphical user interface version.