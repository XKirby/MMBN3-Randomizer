--[[
###################################################
Mega Man Battle Network 3 Slot-In Script
  By X Kirby/Tterraj42
###################################################
Feature List:
During Battle, you can pause the game to enable the following functions.
- L/R: Cycle between Chip Values to add to your Hand.
- Select: Add Chip to your Hand.
- B: Make L/R Scroll by 10 instead of 1 while held down.
- Twitch Integration with a bunch of commands.
  Disables the above controls while active.

While unpaused, the A button consumes a chip like normal.
However, things are handled a bit differently because of the
script manually controlling slotted chips.

Known Issues:
- Panic crashes on use if slotted in? Not sure why.
- Can slot in version exclusives, but who cares.
- GaiaSwrd/GaiaBlde will consume any Chip that has a damage value of 1 to 9999.
- The Plus Damage chips don't affect your current chips, instead affecting
  the next chip slotted in that matches the elements or types that you've
  added damage to.
- HPMemories "fix" your Maximum Health Pool. In other words, they reset your Max
  Health to the correct value it should be.
- Various things, when constantly written, can prevent savefiles from being
  loaded. This no longer happens, but should you mess with this script, you
  should know this before-hand.
]]--

-- Variables
chip = 1
chiplist = require("MMBN 3 Chips")
stylelist = require("MMBN 3 Styles")
panellist = require("MMBN 3 Panels")
AHeld = false
RHeld = false
LHeld = false
BHeld = false
SelHeld = false
counter = 0
CurrentStyle = 0
ForceNextEncounter = nil
EncounterTimer = 0

Difficulty = 1
AllowPAs = true
AllowCustomScreen = true
AllowEscape = true
Modes = {"Easy","Normal","Hard","Extreme"}

DamageBoosts = {
	Normal = 0,
	Fire = 0,
	Aqua = 0,
	Wood = 0,
	Elec = 0,
	Navi = 0
}

-- Chip Cooldown Initialize
ChipCooldowns = {}
ChipCooldownDelay = {}
ChipCooldownDelay[0] = 0
ChipCooldownDelay[1] = 20*60
ChipCooldownDelay[2] = 40*60
ChipCooldownDelay[3] = 50*60
for i=0,3 do
	table.insert(ChipCooldowns, i, 0)
end

-- Twitch Bot Variables
TwitchBotVars = {
	Channel = "",
	Name = "",
	OAuth = "",
	WhiteList = nil, -- Set to nil to disable, or add usernames to a table to prevent random access
	Moderators = nil, -- Set to nil to disable, or add usernames to a table to circumvent difficulty and whitelist values
	MultiUser = nil, -- Set to nil to disable, set to string to enable multiple bots in single change with seperate calls
	Client = nil
}
CommandTimers = {0,0,0,0,0,0,0,0,0,0,0,0,0}
CommandTimerDelays = {2*60,5*60,5*60,5*60,8*60,5*60,10*60,60*60,30*60,10*60,150*60,150*60,10*60}
RouletteDelays = {30*60,30*60}
RandomValues = {}
RandomValues.zennys = {1000,500,200,200,100,100,50,50,20,20,-10,-15,-25,-40,-75,-100,-150,-250,-500,-1000}
RandomValues.frags = {10,8,5,5,3,3,2,1,1,0,0,-1,-2,-2,-3,-3,-5,-5,-8,-10}
RandomValues.hp = {50,50,40,40,35,30,25,20,15,10,-10,-10,-20,-20,-30,-30,-40,-40,-50,-50}
BanList = {}
BanList.chips = {}
BanList.stages = {0,1,8}
BanList.fights = {}
BanList.styles = {}
loadfile("twitchsettings.txt")()

socket = require("socket.core")
local cli,err = socket.tcp()
TwitchBotVars.Client = cli -- Comment this out to play without Twitch.

if TwitchBotVars.Client then
	TwitchBotVars.Client:settimeout(1/5)
	TwitchBotVars.Client:connect(socket.dns.toip("irc.chat.twitch.tv"),6667)
	TwitchBotVars.Client:send("PASS "..TwitchBotVars.OAuth.."\r\n")
	TwitchBotVars.Client:send("NICK "..TwitchBotVars.Name:lower().."\r\n")
	TwitchBotVars.Client:send("JOIN #"..TwitchBotVars.Channel:lower().."\r\n")
end

-- Special Variables
RouletteHandActive = false
RouletteStageActive = false
RouletteHandTimer = 0
RouletteStageTimer = 0

-- Add Chip Command
function add_chip(c)
	local base_offset = 0x2034060
	
	for i = 0,4 do
		-- GaiaSwrd and GaiaBlde
		if memory.readword(base_offset + (i*2)) == 218 or memory.readword(base_offset + (i*2)) == 276 then
			if memory.readword(0x8011530 + (c*32 - 32) + 0xC) > 0 and memory.readword(0x8011530 + (c*32 - 32) + 0xC) <= 9999 then
				memory.writeword(0x2034078 + (i*2), memory.readword(0x2034078 + (i*2)) + memory.readword(0x8011530 + (c*32 - 32) + 0xC))
				break
			end
		end
		-- Atk+10 and Atk+30
		if c == 195 then
			DamageBoosts.Normal = DamageBoosts.Normal + 10
			--print("+10 for next Damage Chip")
			break
		end
		if c == 205 then
			DamageBoosts.Normal = DamageBoosts.Normal + 30
			--print("+30 for next Damage Chip")
			break
		end
		-- Navi+20 and Navi+40
		if c == 200 then
			DamageBoosts.Navi = DamageBoosts.Navi + 20
			--print("+20 for next Navi Chip")
			break
		end
		if c == 206 then
			DamageBoosts.Navi = DamageBoosts.Navi + 40
			--print("+40 for next Navi Chip")
			break
		end
		-- Element+30 Chips
		if c == 196 then
			DamageBoosts.Fire = DamageBoosts.Fire + 30
			--print("+30 for next Fire Chip")
			break
		end
		if c == 197 then
			DamageBoosts.Aqua = DamageBoosts.Aqua + 30
			--print("+30 for next Aqua Chip")
			break
		end
		if c == 198 then
			DamageBoosts.Wood = DamageBoosts.Wood + 30
			--print("+30 for next Wood Chip")
			break
		end
		if c == 199 then
			DamageBoosts.Elec = DamageBoosts.Elec + 30
			--print("+30 for next Elec Chip")
			break
		end
		-- Empty Chip
		if memory.readword(base_offset + (i*2)) == 0xffff then
			memory.writeword(base_offset + (i*2), c)
			memory.writeword(0x200f862 + (i*2), c)
			memory.writeword(0x203406C + (i*2), memory.readword(0x8011530 + (c*32 - 32) + 0xC))
			-- Add Damage Boosts
			if memory.readword(0x8011530 + (c*32 - 32) + 0xC) > 0 and memory.readword(0x8011530 + (c*32 - 32) + 0xC) <= 9999 then
				memory.writeword(0x2034078 + (i*2), DamageBoosts.Normal)
				DamageBoosts.Normal = 0
				-- Fire
				if memory.readbyte(0x8011530 + (c*32 - 32) + 0x6) == 2 then
					memory.writeword(0x2034078 + (i*2), memory.readword(0x2034078 + (i*2)) + DamageBoosts.Fire)
					DamageBoosts.Fire = 0
				end
				-- Aqua
				if memory.readbyte(0x8011530 + (c*32 - 32) + 0x6) == 3 then
					memory.writeword(0x2034078 + (i*2), memory.readword(0x2034078 + (i*2)) + DamageBoosts.Aqua)
					DamageBoosts.Aqua = 0
				end
				-- Wood
				if memory.readbyte(0x8011530 + (c*32 - 32) + 0x6) == 4 then
					memory.writeword(0x2034078 + (i*2), memory.readword(0x2034078 + (i*2)) + DamageBoosts.Wood)
					DamageBoosts.Wood = 0
				end
				-- Elec
				if memory.readbyte(0x8011530 + (c*32 - 32) + 0x6) == 1 then
					memory.writeword(0x2034078 + (i*2), memory.readword(0x2034078 + (i*2)) + DamageBoosts.Elec)
					DamageBoosts.Elec = 0
				end
				-- Navi
				if (c >= 219 and c <= 272) or (c >= 277 and c <= 301) then
					memory.writeword(0x2034078 + (i*2), memory.readword(0x2034078 + (i*2)) + DamageBoosts.Navi)
					DamageBoosts.Navi = 0
				end
			end
			break
		end
	end
	sort_chips()
end

-- Sort Chips Command
function sort_chips()
	if battleCheck() then
		local base_offset1 = 0x2034060
		local base_offset2 = 0x200f862
		local base_offset3 = 0x203406C
		local base_offset4 = 0x2034078
		local chiploc = 0x8011510
		
		-- Write a couple of bytes to force the 1st Chip to always be active
		memory.writebyte(0x203728a,5)
		memory.writebyte(0x20384d8,0)
		
		-- Actually Sort the Chips
		for j = 0,5 do
			for i = 0,3 do
				if memory.readword(base_offset1 + (i*2)) == 0xffff then
					memory.writeword(base_offset1 + (i*2), memory.readword(base_offset1 + (i*2) + 2))
					memory.writeword(base_offset2 + (i*2), memory.readword(base_offset2 + (i*2) + 2))
					memory.writeword(base_offset3 + (i*2), memory.readword(base_offset3 + (i*2) + 2))
					memory.writeword(base_offset4 + (i*2), memory.readword(base_offset4 + (i*2) + 2))
					memory.writeword(base_offset1 + (i*2) + 2, 0xffff)
					memory.writeword(base_offset2 + (i*2) + 2, 0x0000)
					memory.writeword(base_offset3 + (i*2) + 2, 0x0000)
					memory.writeword(base_offset4 + (i*2) + 2, 0x0000)
				end
			end
		end
		
		-- Fix sprites above Mega Man's Head
		local chipicons = 0x6017540
		for i = 0,4 do
			if memory.readword(base_offset1 + (i*2)) == 0xffff then
				break
			end
			for j = 0,0x1f do
				memory.writedword(chipicons + (i*0x80) + (j*4), memory.readdword(memory.readdword(chiploc + (memory.readword(base_offset2 + (i*2))*32) + 20) + (j*4)))
			end
		end
	end
end

-- Controls
function controls()
	if battleCheck() then
		-- Pause State Check
		if TwitchBotVars.Client == nil then
			if memory.readbyte(0x2001889) == 1 then
				-- B Press Check
				if joypad.get(0).B and not BHeld then
					BHeld = true
				elseif not joypad.get(0).B then
					BHeld = false
				end

				-- R Press Check, Cycle Chip Right
				if joypad.get(0).R and not RHeld then
					RHeld = true
					if BHeld then
						chip = chip + 10
					else
						chip = chip + 1
					end
					if chip == 41 then
						chip = chip + 1
					end
					if chip >= 313 and chip <= 319 then
						chip = 320
					end
					if chip >= 352 then
						chip = 1
					end
				elseif not joypad.get(0).R then
					RHeld = false
				end
				
				-- L Press Check, Cycle Chip Right
				if joypad.get(0).L and not LHeld then
					LHeld = true
					if BHeld then
						chip = chip - 10
					else
						chip = chip - 1
					end
					if chip == 41 then
						chip = chip - 1
					end
					if chip >= 313 and chip <= 319 then
						chip = 312
					end
					if chip <= 0 then
						chip = 351
					end
				elseif not joypad.get(0).L then
					LHeld = false
				end
			end

			-- Select Press Check, Slot In or Use Chip
			if joypad.get(0).select and not SelHeld then
				SelHeld = true
				-- Pause State Check
				if memory.readbyte(0x2001889) == 1 then
					add_chip(chip)
				end
			elseif not joypad.get(0).select then
				SelHeld = false
			end
		end
		
		if joypad.get(0).A and not AHeld then
			AHeld = true
			if memory.readbyte(0x2001889) == 0 and memory.readbyte(0x0203728a) < 5 and memory.readbyte(0x2037274) == 0 then
				memory.writeword(0x2034060, 0xffff)
				memory.writeword(0x200f862, 0x0000)
				memory.writeword(0x203406C, 0x0000)
				memory.writeword(0x2034078, 0x0000)
				sort_chips()
			end
		elseif not joypad.get(0).A then
			AHeld = false
		end
	end
end

-- Health Changing Functions
function changeMaxHealth(val)
	fix_hp()
	if val == nil then
		fix_hp()
		return 0
	end
	if math.abs(tonumber(val)) >= memory.readword(0x20018A2) and tonumber(val) < 0 then
		memory.writeword(0x20018A2, 0)
		if battleCheck() then
			memory.writeword(0x2037296, memory.readword(0x20018A2))
			if memory.readword(0x2037296) >= memory.readword(0x20018A2) then
				memory.writeword(0x2037296, memory.readword(0x20018A2))
			end
		end
		fix_hp()
		return "lethal"
	end
	memory.writeword(0x20018A2, memory.readword(0x20018A2) + tonumber(val))
	if memory.readword(0x20018A2) > 9999 then
		memory.writeword(0x20018A2, 9999)
	end
	if battleCheck() then
		memory.writeword(0x2037296, memory.readword(0x20018A2))
	end
	fix_hp()
	return val
end

function changeCurHealth(val)
	fix_hp()
	if val == nil then
		fix_hp()
		return 0
	end
	if math.abs(tonumber(val)) >= memory.readword(0x20018A0) and tonumber(val) < 0 then
		memory.writeword(0x20018A0, 0)
		if battleCheck() then
			memory.writeword(0x2037294, memory.readword(0x20018A0))
			if memory.readword(0x2037294) >= memory.readword(0x20018A0) then
				memory.writeword(0x2037294, memory.readword(0x20018A0))
			end
		end
		fix_hp()
		return "lethal"
	end
	memory.writeword(0x20018A0, memory.readword(0x20018A0) + tonumber(val))
	if memory.readword(0x20018A0) >= memory.readword(0x20018A2) then
		memory.writeword(0x20018A0, memory.readword(0x20018A2))
	end
	
	if battleCheck() then
		memory.writeword(0x2037294, memory.readword(0x20018A0))
		if memory.readword(0x2037294) >= memory.readword(0x20018A2) then
			memory.writeword(0x2037294, memory.readword(0x20018A2))
		end
	end
	fix_hp()
	return val
end

-- Currency Changing Functions
function changeZenny(val)
	if val == nil then
		return 0
	end
	if memory.readdword(0x20018F4) <= math.abs(tonumber(val)) and tonumber(val) < 0 then
		memory.writedword(0x20018f4, 0)
		val = 0
		return "empty"
	end
	memory.writedword(0x20018f4, memory.readdword(0x20018F4) + tonumber(val))
	if memory.readdword(0x20018F4) > 999999 then
		memory.writedword(0x20018F4, 999999)
	end
	return val
end

function changeFrags(val)
	if val == nil then
		return 0
	end
	if memory.readword(0x20018F8) <= math.abs(tonumber(val)) and tonumber(val) < 0 then
		memory.writeword(0x20018f8, 0)
		val = 0
		return "empty"
	end
	memory.writeword(0x20018f8, memory.readword(0x20018F8) + tonumber(val))
	if memory.readword(0x20018F8) > 9999 then
		memory.writeword(0x20018F8, 9999)
	end
	return val
end

-- Twitch Bot Commands
function twitchbot_commands()
	local msg, err = TwitchBotVars.Client:receive()
	if msg then
		print(msg)
		
		-- Whitelist Check
		local user = nil
		if type(TwitchBotVars.WhiteList) == "table" then
			for i=1,#TwitchBotVars.WhiteList do
				m, l = string.find(msg:lower(), ":")
				l = string.find(msg:lower(), "!")
				if m == nil or l == nil then
					break
				end
				user = string.sub(msg:lower(),m+1,l-1)
				if user:lower() == TwitchBotVars.WhiteList[i]:lower() then
					break
				end
				user = nil
			end
		else
			user = "all users can use commands"
		end
		
		-- Moderator Check
		local mod = nil
		if type(TwitchBotVars.Moderators) == "table" then
			for i=1,#TwitchBotVars.Moderators do
				m, l = string.find(msg:lower(), ":")
				l = string.find(msg:lower(), "!")
				if m == nil or l == nil then
					break
				end
				mod = string.sub(msg:lower(),m+1,l-1)
				if mod:lower() == TwitchBotVars.Moderators[i]:lower() then
					break
				end
				mod = nil
			end
		else
			mod = nil
		end
		
		-- Streamer Check
		local streamer = false
		m, l = string.find(msg:lower(), ":")
		l = string.find(msg:lower(), "!")
		if type(m) == "number" and type(l) == "number" then
			if string.sub(msg:lower(),m+1,l-1):lower() == TwitchBotVars.Channel:lower() or string.sub(msg,m+1,l-1):lower() == TwitchBotVars.Name:lower() then
				streamer = true
			end
		end
		
		-- "Difficulty" Command
		m, l = string.find(msg:lower(), ":!difficulty")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!difficulty "..TwitchBotVars.MultiUser:lower())
		end
		if m and (streamer or type(mod) == "string") then
			local c = string.sub(msg:lower(), l+2, string.len(msg))
			c = tonumber(c)
			
			if type(c) == "number" then
				c = math.floor(c)
				if c >= 1 and c <= #Modes then
					Difficulty = c
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Bot Difficulty set to "..Modes[Difficulty]..". \r\n")
				end
			end
		end
		
		-- "Command List" Command
		m, l = string.find(msg:lower(), ":!cmdlist")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!cmdlist "..TwitchBotVars.MultiUser:lower())
		end
		if m and CommandTimers[2] == 0 and (type(user) == "string" or type(mod) == "string") then
			CommandTimers[2] = CommandTimerDelays[2]
			TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Commands are !difficulty, !chiplist, !stylelist, !fightlist, !slotin, !zennyplz, !fragsplz, !maxhealthplz, !healthplz, !stylechange, !fightme, !scramble, !setstage, !roulettehand, !roulettestage, !chipplz \r\n")
		end
		
		-- Slot In Command
		m, l = string.find(msg:lower(), ":!slotin")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!slotin "..TwitchBotVars.MultiUser:lower())
		end
		if m and battleCheck() and CommandTimers[1] == 0 and RouletteHandActive == false and ((type(user) == "string" and Difficulty >= 1) or type(mod) == "string") then
			local c = string.sub(msg:lower(), l+2, string.len(msg))
			c = tostring(c)
			
			-- Find Chip
			for i = 1,351 do
				if chiplist.names[i] then
					if string.lower(chiplist.names[i]) == c:lower() then
						c = i
						break
					end
				end
			end
			if type(tonumber(c)) == "number" then
				c = tonumber(c)
				c = math.floor(c)
			end
			
			-- Give Chip (Unless nonexistant, on cooldown, PA-limited, or Panic, Panic Crashes)
			if type(c) == "number" and table.find(compareValue(c), BanList.chips) then
				TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Chip not added. (It's banned.)\r\n")
			elseif type(c) == "number" and c == 41 then
				TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Chip not added. (It crashes the game D:)\r\n")
			elseif type(c) == "number" and c >= 320 and AllowPAs == false and mod == nil then
				TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Chip not added. (No PAs allowed from normal users.)\r\n")
			elseif type(c) == "number" and ((c > 0 and c < 313 and type(ChipCooldowns[(memory.readbyte(0x8011530 + (c*32 - 32) + 0x11))]) == "number") or (c > 319 and c < 352 and type(ChipCooldowns[3]) == "number")) and ((ChipCooldowns[(memory.readbyte(0x8011530 + (c*32 - 32) + 0x11))] > 0 and c < 313) or (ChipCooldowns[3] > 0 and c >= 320)) then
				TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :"..chiplist.names[c].." is on cooldown. \r\n")
			elseif type(c) == "number" and ((c > 0 and c < 313 and type(ChipCooldowns[(memory.readbyte(0x8011530 + (c*32 - 32) + 0x11))]) == "number") or (c > 319 and c < 352 and type(ChipCooldowns[3]) == "number")) and ((ChipCooldowns[(memory.readbyte(0x8011530 + (c*32 - 32) + 0x11))] <= 0 and c < 313) or (ChipCooldowns[3] <= 0 and c >= 320)) then
				CommandTimers[1] = CommandTimerDelays[1]
				print("Slot in! "..chiplist.names[c].."!")
				-- Restart Cooldown
				if c >= 320 then
					ChipCooldowns[3] = ChipCooldownDelay[3]
				else
					ChipCooldowns[(memory.readbyte(0x8011530 + (c*32 - 32) + 0x11))] = ChipCooldownDelay[(memory.readbyte(0x8011530 + (c*32 - 32) + 0x11))]
				end
				add_chip(c)
				TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Slot-In "..chiplist.names[c].."! \r\n")
			else
				TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Chip not Found. \r\n")
			end
		end
		
		-- Chip List Command
		m, l = string.find(msg:lower(), ":!chiplist")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!chiplist "..TwitchBotVars.MultiUser:lower())
		end
		if m and CommandTimers[2] == 0 and ((type(user) == "string" and Difficulty >= 1) or type(mod) == "string") then
			CommandTimers[2] = CommandTimerDelays[2]
			TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :https://docs.google.com/spreadsheets/d/e/2PACX-1vS2q_BwXDdNe3EQOBI6CibqqTUTwrFDT00bm35vsHUqqpuX1Km7eZsqEaLtyCLJLNN1ufX3eZAqb2-6/pubhtml# \r\n")
		end
		
		-- Style List Command
		m, l = string.find(msg:lower(), ":!stylelist")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!stylelist "..TwitchBotVars.MultiUser:lower())
		end
		if m and CommandTimers[2] == 0 and ((type(user) == "string" and Difficulty >= 1) or type(mod) == "string") then
			CommandTimers[2] = CommandTimerDelays[2]
			TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :https://docs.google.com/spreadsheets/d/1yTRxDQpO5KpG3P_LDmmTpg-cFHgCLKYO0oChQVHkln4/edit?usp=sharing \r\n")
		end
		
		-- Fight List Command
		m, l = string.find(msg:lower(), ":!fightlist")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!fightlist "..TwitchBotVars.MultiUser:lower())
		end
		if m and CommandTimers[2] == 0 and ((type(user) == "string" and Difficulty >= 4) or type(mod) == "string") then
			CommandTimers[2] = CommandTimerDelays[2]
			TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :https://docs.google.com/spreadsheets/d/1scqHm9vdilQ9d-yXjgpLyAjrlyO4_G8zprSu6LDWIrA/edit?usp=sharing \r\n")
		end
		
		-- "Plz" Commands (Gives or Takes Zenny/Frags/HP/Battle Chips)
		
		m, l = string.find(msg:lower(), ":!zennyplz")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!zennyplz "..TwitchBotVars.MultiUser:lower())
		end
		if m and CommandTimers[3] == 0 and ((type(user) == "string" and Difficulty >= 2) or type(mod) == "string") then
			CommandTimers[3] = CommandTimerDelays[3]
			local choice = RandomValues.zennys[math.random(0,#RandomValues.zennys-1)]
			choice = changeZenny(choice)
			if choice == 0 then
				TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Nothing Happened. \r\n")
			else
				if type(choice) == "number" and choice > 0 then
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Gained "..tostring(choice).." Zenny! \r\n")
				elseif type(choice) == "number" and choice < 0 then
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Lost "..tostring(choice).." Zenny! \r\n")
				elseif choice == "empty" then
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :We're broke now! \r\n")
				end
			end
		end
		
		m, l = string.find(msg:lower(), ":!fragsplz")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!fragsplz "..TwitchBotVars.MultiUser:lower())
		end
		if m and CommandTimers[4] == 0 and ((type(user) == "string" and Difficulty >= 3) or type(mod) == "string") then
			CommandTimers[4] = CommandTimerDelays[4]
			local choice = RandomValues.frags[math.random(0,#RandomValues.frags-1)]
			choice = changeFrags(choice)
			if choice == 0 then
				TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Nothing Happened. \r\n")
			else
				if type(choice) == "number" and choice > 0 then
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Gained "..tostring(choice).." Bug Frags! \r\n")
				elseif type(choice) == "number" and choice < 0 then
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Lost "..tostring(choice).." Bug Frags! \r\n")
				elseif choice == "empty" then
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Empty on BugFrags! \r\n")
				end
			end
		end
		
		m, l = string.find(msg:lower(), ":!maxhealthplz")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!maxhealthplz "..TwitchBotVars.MultiUser:lower())
		end
		if m and CommandTimers[5] == 0 and ((type(user) == "string" and Difficulty >= 3) or type(mod) == "string") then
			CommandTimers[5] = CommandTimerDelays[5]
			local choice = RandomValues.hp[math.random(0,#RandomValues.hp-1)]
			choice = changeMaxHealth(choice)
			if type(choice) == "number" then
				changeCurHealth(choice)
			elseif choice == "lethal" then
				changeCurHealth(-9999)
			end
			if choice == 0 then
				TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Nothing Happened. \r\n")
			else
				if type(choice) == "number" and choice > 0 then
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Gained "..tostring(choice).." Max Health! \r\n")
				elseif type(choice) == "number" and choice < 0 then
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Lost "..tostring(choice).." Max Health! \r\n")
				elseif choice == "lethal" then
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :WELL YOU'RE DEAD PERMANENTLY NOW \r\n")
				end
			end
		end
		
		m, l = string.find(msg:lower(), ":!healthplz")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!healthplz "..TwitchBotVars.MultiUser:lower())
		end
		if m and CommandTimers[6] == 0 and ((type(user) == "string" and Difficulty >= 3) or type(mod) == "string") then
			CommandTimers[6] = CommandTimerDelays[6]
			local choice = RandomValues.hp[math.random(0,#RandomValues.hp-1)]
			choice = changeCurHealth(choice)
			if choice == 0 then
				TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Nothing Happened. \r\n")
			else
				if type(choice) == "number" and choice > 0 then
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Healed "..tostring(choice).." Health! \r\n")
				elseif type(choice) == "number" and choice < 0 then
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Took "..tostring(choice).." Damage! \r\n")
				elseif choice == "lethal" then
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :You're dead! \r\n")
				end
			end
		end
		
		m, l = string.find(msg:lower(), ":!chipplz")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!chipplz "..TwitchBotVars.MultiUser:lower())
		end
		if m and CommandTimers[13] == 0 and ((type(user) == "string" and Difficulty >= 1 or type(mod) == "string")) then
			local c = string.sub(msg:lower(), l+2, string.len(msg))
			c = tostring(c)
			
			-- Find Chip
			for i = 1,311 do
				if chiplist.names[i] then
					if string.lower(chiplist.names[i]) == c:lower() then
						c = i
						break
					end
				end
			end
			if type(tonumber(c)) == "number" then
				c = tonumber(c)
				c = math.floor(c)
			end
			
			-- Over/Underflow Check
			if c < 1 or c > 311 then
				TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." : Chip not found. \r\n")
			else
				-- Find Code
				local codeVal = 0xFF
				local codeSlot = 0
				repeat
					codeSlot = math.random(0,5)
					codeVal = memory.readbyte(0x08011510 + (c*32) + codeSlot)
				until codeVal < 0xFF
				
				-- Massive If Statement that checks Chip ID, Chip Code, and Version-Exclusive Chips.
				if (codeVal >= 0 and codeVal <= 26 and c >= 0 and c <= 312) or ((memory.readbyte(0x080000AA) == 0x42 and ((c >= 302 and c <= 303) or (c >= 309 and c <= 311))) or (memory.readbyte(0x080000AA) == 0x57 and (c >= 304 and c <= 308))) then
					-- If your Backpack is full with that chip.
					local checkSlots = 0
					local emptySlots = {}
					repeat
						if memory.readbyte(0x02001F60 + (c*18) + checkSlots) >= 99 then
							if checkSlots == codeSlot and #emptySlots >= 1 then
								codeSlot = emptySlots[math.random(1,#emptySlots)]
							end
						elseif memory.readbyte(0x08011510 + (c*32) + checkSlots) < 0xFF then
							emptySlots[#emptySlots+1] = checkSlots
						end
						if memory.readbyte(0x02001F60 + (c*18) + codeSlot) < 99 then
							if checkSlots == codeSlot then
								CommandTimers[13] = CommandTimerDelays[13]
								memory.writebyte(0x02001F60 + (c*18) + codeSlot, memory.readbyte(0x02001F60 + (c*18) + codeSlot)+1)
								TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." : "..chiplist.names[c].. " "..chiplist.codes[codeVal].." added to Pack! \r\n")
								break
							end
						end
						checkSlots = checkSlots + 1
					until checkSlots == 6
				else
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." : Chip not found. (Might be version-exclusive?) \r\n")
				end
			end
		end
		
		-- "Style Change" Command
		m, l = string.find(msg:lower(), ":!stylechange")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!stylechange "..TwitchBotVars.MultiUser:lower())
		end
		if m and CommandTimers[7] == 0 and ((type(user) == "string" and Difficulty >= 1) or type(mod) == "string") then
			CommandTimers[7] = CommandTimerDelays[7]
			local c = string.sub(msg:lower(), l+2, string.len(msg))
			c = tostring(c)
			
			-- Find Style
			for i = 0,0x3F do
				if stylelist[i] then
					if string.lower(stylelist[i]) == c:lower() then
						c = i
						break
					end
				end
			end
			if type(tonumber(c)) == "number" then
				c = tonumber(c)
				c = math.floor(c)
			end
			
			-- Give Style
			if type(c) == "number" and (c >= 0 and c < 0x40) then
				if table.find(compareValue(c), BanList.styles) then
					CommandTimers[6] = 0
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Style not changed. (This Style has been banned.) \r\n")
				else
					print("Style Change! "..stylelist[c].."!")
					CurrentStyle = c
					force_stylechange(c)
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Style Changes to "..stylelist[c].."! \r\n")
				end
			else
				CommandTimers[6] = 0
				TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Style not Found. \r\n")
			end
		end
		
		-- "Force Encounter" command
		m, l = string.find(msg:lower(), ":!fightme")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!fightme "..TwitchBotVars.MultiUser:lower())
		end
		if m and CommandTimers[8] == 0 and not battleCheck() and ((type(user) == "string" and Difficulty >= 4) or type(mod) == "string") then
			CommandTimers[8] = CommandTimerDelays[8]
			local c = string.sub(msg:lower(), l+2, string.len(msg))
			
			if type(tonumber(c)) == "number" then
				c = tonumber(c)
				c = math.floor(c)
			end
			
			-- Set Next Encounter variable
			if type(c) == "number" then
				if c == 92 or (c >= 247 and c <= 252) or (c >= 1124 and c <= 1163) or table.find(compareValue(c), BanList.fights) then
					CommandTimers[8] = 0
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Encounter not added. (This fight is banned.) \r\n")
				elseif (c >= 0 and c < 1124) then
					print("Incoming Viruses! Encounter #"..c.." Loaded!")
					ForceNextEncounter = c
					EncounterTimer = 30
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Forcing next Encounter to #"..c.."! \r\n")
				else
					CommandTimers[8] = 0
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Encounter not found. \r\n")
				end
			end
		end
		
		-- "Scramble" Command
		m, l = string.find(msg:lower(), ":!scramble")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!scramble "..TwitchBotVars.MultiUser:lower())
		end
		if m and CommandTimers[9] == 0 and not battleCheck() and ((type(user) == "string" and Difficulty >= 2) or type(mod) == "string") then
			CommandTimers[9] = CommandTimerDelays[9]
			shuffleFolders()
			TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Follders were scrambled! \r\n")
		end
		
		-- "SetStage" Command
		m, l = string.find(msg:lower(), ":!setstage")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!setstage "..TwitchBotVars.MultiUser:lower())
		end
		
		if m and CommandTimers[10] == 0 and battleCheck() and RouletteStageActive == false and ((type(user) == "string" and Difficulty >= 3) or type(mod) == "string") then
			CommandTimers[10] = CommandTimerDelays[10]
			local c = string.sub(msg:lower(), l+2, string.len(msg))
			
			-- Find Panel Type
			for i = 0,10 do
				if stylelist[i] then
					if string.lower(panellist[i]) == c:lower() then
						c = i
						break
					end
				end
			end
			if type(tonumber(c)) == "number" then
				c = tonumber(c)
				c = math.floor(c)
			end
			
			if type(c) == "number" and (c >= 0 and c <= 10) then
				if table.find(compareValue(c), BanList.stages) then
					CommandTimers[9] = 0
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Stage not changed. (This Stage has been banned.) \r\n")
				else
					print("Stage set to "..panellist[c].."!")
					force_setstage(c)
					TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Stage set to "..panellist[c].."! \r\n")
				end
			else
				CommandTimers[9] = 0
				TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Stage not Found. \r\n")
			end
		end
		
		-- "Roulette Hand" Command
		m, l = string.find(msg:lower(), ":!roulettehand")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!roulettehand "..TwitchBotVars.MultiUser:lower())
		end
		if m and CommandTimers[11] == 0 and battleCheck()  and RouletteHandActive == false and ((type(user) == "string" and Difficulty >= 4) or type(mod) == "string") then
			CommandTimers[11] = CommandTimerDelays[11]
			RouletteHandActive = true
			RouletteHandTimer = RouletteDelays[1]
			print("Roulette Slot-in Mode Activated!")
			TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Russian Roulette Slot-in Mode Activated! \r\n")
		end
		
		-- "Roulette Stage" Command
		m, l = string.find(msg:lower(), ":!roulettestage")
		if type(TwitchBotVars.MultiUser) == "string" then
			m, l = string.find(msg:lower(), ":!roulettestage "..TwitchBotVars.MultiUser:lower())
		end
		if m and CommandTimers[12] == 0 and battleCheck() and RouletteStageActive == false and ((type(user) == "string" and Difficulty >= 4) or type(mod) == "string") then
			CommandTimers[12] = CommandTimerDelays[12]
			RouletteStageActive = true
			RouletteStageTimer = RouletteDelays[2]
			print("Roulette SetStage Mode Activated!")
			TwitchBotVars.Client:send("PRIVMSG #"..TwitchBotVars.Channel.." :Russian Roulette SetStage Mode Activated! \r\n")
		end
	end
end

-- Fill the player's Library
function maxLibrary()
	if memory.readbyte(0x080000AA) == 0x42 then -- Blue
		memory.writeword(0x020019B0, 0xD5A4) -- Anti Cheat
		memory.writebyte(0x02000330, 0x7F)
		memory.writebyte(0x02000356, 0x07)
		memory.writebyte(0x02000357, 0x00)
		for i=0x331,0x355 do
			memory.writebyte(0x02000000 + i, 0xFF)
		end
		for i=0x358,0x35B do
			memory.writebyte(0x02000000 + i, 0xFF)
		end
	else--if memory.readbyte(0x080000AA) == 0x57 then -- White
		memory.writeword(0x020019B0, 0xD22E) -- Anti Cheat
		memory.writebyte(0x02000330, 0x7F)
		memory.writebyte(0x02000357, 0x80)
		for i=0x331,0x356 do
			memory.writebyte(0x02000000 + i, 0xFF)
		end
		for i=0x358,0x35D do
			memory.writebyte(0x02000000 + i, 0xFF)
		end
	end
end

-- Shuffle the player's Folders.
function shuffleFolders()
	if not battleCheck() then
		folders = {}
		folders.one = {}
		folders.two = {}
		
		for i = 1, 30, 1 do
			folders.one[i] = memory.readdword(0x02001410 + ((i-1) * 4))
			folders.two[i] = memory.readdword(0x02001410 + ((i-1) * 4) + (60*4))
		end
		
		folders.one = shuffleTable(folders.one)
		folders.two = shuffleTable(folders.two)
		
		for i = 1, 30, 1 do
			memory.writedword(0x02001410 + ((i-1) * 4), folders.one[i])
			memory.writedword(0x02001410 + ((i-1) * 4) + (60*4), folders.two[i])
		end
	end
end

-- Shuffle Lua Tables
function shuffleTable(tbl)
	size = #tbl
	for i = size, 1, -1 do
		local rand = math.random(i)
		tbl[i], tbl[rand] = tbl[rand], tbl[i]
	end
	return tbl
end

function compareValue(value)
	return function (v) return v == value end
end

-- In-Battle Check
function battleCheck()
	return memory.readbyte(0x020097F8) == 0x08
end

-- Force Style Change
function force_stylechange(style)
	if type(tonumber(style)) == "number" then
		memory.writebyte(0x2001881, tonumber(style))
	end
end

function force_setstage(ID)
	if type(tonumber(ID)) == "number" then
		for i = 0, 23 do
			if not (i==0 or i==7 or i==8 or i==15 or i==16 or i==23) then
				memory.writebyte(0x0200F5A0 + (i * 0x10), ID)
			end
		end
	end
end

-- Force Fight
function force_encounter(encounter)
	local fights = nil
	if memory.readbyte(0x080000AA) == 0x42 then 
		fights = require("MMBN 3 Battles Blue")
	else
		fights = require("MMBN 3 Battles White")
	end
	if tonumber(encounter) >= 0 and tonumber(encounter) < 1124 then
		if fights[encounter] > 0 and (memory.readdword(0x2006d0c) == 0 or memory.readdword(0x2006d0c) == 0x200f8c8 or(memory.readdword(0x2006d0c) >= 0x8000000 and memory.readdword(0x2006d0c) < 0x8022000)) then
			memory.writeword(0x2001ddc, 0xFFFF)
			memory.writedword(0x20018AC, 0x0200f8c8)
			memory.writedword(0x2006d0c, 0x0200f8c8)
			memory.writedword(0x200f8cc, 0x08000000 + fights[encounter])
		end
	end
end

-- Shuffle your Hand EVERY FRAME! :D
function rouletteHand()
	if battleCheck() and RouletteHandActive == true then
		-- Erase Hand Completely
		local base_offset1 = 0x2034060
		local base_offset2 = 0x200f862
		local base_offset3 = 0x203406C
		local base_offset4 = 0x2034078
		for i = 0,4 do
			memory.writeword(base_offset1 + (i*2), 0xffff)
			memory.writeword(base_offset2 + (i*2), 0x0000)
			memory.writeword(base_offset3 + (i*2), 0x0000)
			memory.writeword(base_offset4 + (i*2), 0x0000)
		end
		
		-- Refill Hand up to 5 Chips
		for i = 0,4 do
			add_chip(math.random(1,#chiplist.names))
		end
	end
	RouletteHandTimer = RouletteHandTimer - 1
	if RouletteHandTimer < 1 then
		RouletteHandTimer = 0
		RouletteHandActive = false
	end
end

-- Shuffle the stage's panels every 10 Frames! :D
function rouletteStage()
	if battleCheck() and RouletteStageActive == true and RouletteStageTimer % 10 == 0 then
		for i = 0, 23 do
			if not (i==0 or i==7 or i==8 or i==15 or i==16 or i==23) and memory.readbyte(0x0200F5A0 + (i * 0x10)) >= 2 then
				memory.writebyte(0x0200F5A0 + (i * 0x10), math.random(4,10))
			end
		end
	end
	RouletteStageTimer = RouletteStageTimer - 1
	if RouletteStageTimer < 1 then
		RouletteStageTimer = 0
		RouletteStageActive = false
	end
end

-- Fix Health Pools
function fix_hp()
	-- Current Health fix
	if battleCheck() and not (memory.readword(0x20018A0) == memory.readword(0x2037294)) then
		memory.writeword(0x20018A0, memory.readword(0x2037294))
	end
	
	-- Max Health Fix
	if battleCheck() and not (memory.readword(0x20018A2) == memory.readword(0x2037296)) then
		memory.writeword(0x20018A2, memory.readword(0x2037296))
	end
end

-- Table Search
function table.find(f, l) -- find element v of l satisfying f(v)
  for _, v in ipairs(l) do
    if f(v) then
      return v
    end
  end
  return nil
end

-- Write Library
maxLibrary()

-- Main Loop
while 1 do
	controls()
	if battleCheck() then
		-- Shuffle Hand and Stage if activated.
		rouletteHand()
		rouletteStage()
		
		-- Potentially Disallow Custom Screen when past the tutorial
		if not AllowCustomScreen and memory.readbyte(0x2001886) >= 1 then
			memory.writebyte(0x2006CAE, 0)
			if memory.readword(0x2006CCC) >= 0x3fe0 then
				memory.writeword(0x2006CCC, 0)
			end
		end
		
		-- Potentially Disallow Escaping
		if not AllowEscape then
			memory.writebyte(0x2001A20, 0)
		end
		
		EncounterTimer = EncounterTimer - 1
		if EncounterTimer <= 0 then
			ForceNextEncounter = nil
			EncounterTimer = 0
		end
		
		if not TwitchBotVars.Client then
			gui.register(gui.text(4,140,"Slot-In Chip: "..chiplist.names[chip], "white","black"))
		end
	elseif memory.readword(0x20018a0) > 0 then
		CurrentStyle = tonumber(memory.readbyte(0x2001881))
		if stylelist[CurrentStyle] then
			gui.register(gui.text(4,150,"Style: "..stylelist[CurrentStyle], "white","black"))
		end
	end
	
	for i=0,3 do
		ChipCooldowns[i] = ChipCooldowns[i] - 1
		if ChipCooldowns[i] < 0 then
			ChipCooldowns[i] = 0
		end
	end
	
	if type(ForceNextEncounter) == "number" and ForceNextEncounter >= 0 and ForceNextEncounter < 1124 then
		force_encounter(ForceNextEncounter)
	end
	
	for i = 1,#CommandTimers do
		if CommandTimers[i] == nil then
			CommandTimers[i] = 0
		end
		CommandTimers[i] = CommandTimers[i] - 1
		if CommandTimers[i] < 0 then
			CommandTimers[i] = 0
		end
	end
	if counter % 10 == 0 and TwitchBotVars.Client then
		twitchbot_commands()
	end
	if counter == 60 and TwitchBotVars.Client then
		TwitchBotVars.Client:settimeout(1/30)
	end
	if counter == 120 then
		counter = 0
	end
	counter = counter + 1
	
	vba.frameadvance()
end