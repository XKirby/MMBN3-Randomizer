local inBattle = false
local edit = false
local chipslot = -1
local chiplist = require('MMBN 3 Chips')

local AHeld = false
local BHeld = false
local RHeld = 0
local LHeld = 0
local StartHeld = false
local SelHeld = false
local RightHeld = false
local LeftHeld = false

function maxLibrary() -- TODO: Test Ending
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

function battleCheck()
	return memory.readbyte(0x020097F8) == 0x08
end

function controls()
	-- Set Chip Slot
	if joypad.get(0).A and not AHeld then
		AHeld = true
		if chipslot > -1 then
			chipslot = -1
		else
			chipslot = memory.readdword(0x0200941C)
		end
	elseif not joypad.get(0).A then
		AHeld = false
	end
	
	if joypad.get(0).B and not BHeld then
		BHeld = true
		edit = false
		chipslot = -1
	elseif not joypad.get(0).B then
		BHeld = false
	end
	
	-- Turn on Edit Mode
	if joypad.get(0).start and not StartHeld and (chipslot >= 0x02001410 and chipslot <= 0x2002000) then
		StartHeld = true
		if edit == false then
			edit = true
		else
			edit = false
			chipslot = -1
		end
	elseif not joypad.get(0).start then
		StartHeld = false
	end
	
	-- Edit Mode
	if chipslot < 0x02000000 then
		chipslot = -1
		return
	end
	local chip = memory.readword(chipslot)
	local code = memory.readword(chipslot + 2)
	gui.register(gui.text(4,150,"Chip: "..chiplist.names[chip].." "..chiplist.codes[code], "white","black"))
	if edit == true then
		gui.register(gui.text(4,10,"Edit Mode Active!", "white","black"))
		
		-- Set Chip ID
		if joypad.get(0).R then
			RHeld = RHeld + 1
			if RHeld >= 31 then RHeld = 31 end
			if RHeld == 1 or RHeld > 30 then
				if chip + 1 > 301 then chip = 301 else chip = chip + 1 end
				memory.writeword(chipslot, chip)
				code = memory.readbyte(0x08011510 + chip*0x20)
				memory.writeword(chipslot + 2, code)
			end
		else
			RHeld = 0
		end
		if joypad.get(0).L then
			LHeld = LHeld + 1
			if LHeld >= 31 then LHeld = 31 end
			if LHeld == 1 or LHeld > 30 then
				if chip - 1 < 1 then chip = 1 else chip = chip - 1 end
				memory.writeword(chipslot, chip)
				code = memory.readbyte(0x08011510 + chip*0x20)
				memory.writeword(chipslot + 2, code)
			end
		else
			LHeld = 0
		end
		
		-- Set Code ID
		if joypad.get(0).right and not RightHeld then
			RightHeld = true
			for i=0,5 do
				local newcode = memory.readbyte(0x08011510 + chip*32 + i)
				if newcode == 0xFF then
					break
				elseif newcode > code then
					memory.writeword(chipslot + 2, newcode)
					break
				end
			end
		elseif not joypad.get(0).right then
			RightHeld = false
		end
		if joypad.get(0).left and not LeftHeld then
			LeftHeld = true
			for i=0,5 do
				local newcode = memory.readbyte(0x08011510 + chip*32 + 5 - i)
				if newcode < code then
					memory.writeword(chipslot + 2, newcode)
					break
				end
			end
		elseif not joypad.get(0).left then
			LeftHeld = false
		end
		
		-- Save to File
		if joypad.get(0).select and not SelHeld then
			SelHeld = true
			local folder = memory.readdword(0x02009418)
			file = io.open("folders.txt", "w")
			for i = 0,29 do
				local endchip = memory.readword(folder + i*4)
				local endcode = memory.readword(folder + i*4 + 2)
				file:write(endchip.." "..endcode)
				if i < 29 then
					file:write(",")
				end
			end
			file:write("\n")
			io.close(file)
		elseif not joypad.get(0).select then
			SelHeld = false
		end
	end
end

maxLibrary()

while true do
	if inBattle then
		inBattle = battleCheck()
	else
		if battleCheck() then
			inBattle = true
		end
	end
	
	if not inBattle then
		controls()
	end
	
	vba.frameadvance()
end

