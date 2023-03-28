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
local importedFolders = {}
local FolderLoaded = 0

-- Function taken from StackOverflow
-- see if the file exists
function file_exists(file)
  local f = io.open(file, "rb")
  if f then f:close() end
  return f ~= nil
end

-- Function taken from StackOverflow
-- get all lines from a file, returns an empty 
-- list/table if the file does not exist
function lines_from(file)
  if not file_exists(file) then return {} end
  local lines = {}
  for line in io.lines(file) do 
    lines[#lines + 1] = line
  end
  return lines
end

function maxLibrary() -- TODO: Test Ending
	if memory.readbyte(0x080000AA) == 0x42 then -- Blue
		memory.write_u16_le(0x020019B0, 0xD5A4) -- Anti Cheat
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
		memory.write_u16_le(0x020019B0, 0xD22E) -- Anti Cheat
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
	if joypad.get().A and not AHeld then
		AHeld = true
		if chipslot > -1 then
			chipslot = -1
		else
			chipslot = memory.read_u32_le(0x0200941C)
		end
	elseif not joypad.get().A then
		AHeld = false
	end
	
	if joypad.get().B and not BHeld then
		BHeld = true
		edit = false
		chipslot = -1
	elseif not joypad.get().B then
		BHeld = false
	end
	
	if edit == false then
		if joypad.get().Select and not SelHeld then
			SelHeld = true
		elseif not joypad.get().Select then
			SelHeld = false
		end
		
		-- Display Folder
		if SelHeld then
			local folder = memory.read_u32_le(0x02009418)
			for i = 0,29 do
				local endchip = memory.read_u16_le(folder + i*4)
				local endcode = memory.read_u16_le(folder + i*4 + 2)
				gui.pixelText(0 + math.floor(i/15)*120,8+(i%15)*8, "Slot #"..(i+1)..": "..chiplist.names[endchip].." "..chiplist.codes[endcode].." ("..endchip..")", "#FFFFFFFF", "#FF000000")
			end
		end
		
		if #importedFolders > 0 then
			local folder = memory.read_u32_le(0x02009418)
			
			-- Cycle Folders +1
			if joypad.get().R then
				if RHeld == 0 then
					FolderLoaded = FolderLoaded + 1
					if FolderLoaded > #importedFolders then
						FolderLoaded = 1
					end
					local tbl = {}
					local i = 0
					for k,v in string.gmatch(importedFolders[FolderLoaded], "(%d+) (%d+)") do
						if tbl[math.floor(i/2)] == nil then tbl[math.floor(i/2)] = {} end
						tbl[math.floor(i/2)][(i%2)+1] = tonumber(k)
						i=i+1
						tbl[math.floor(i/2)][(i%2)+1] = tonumber(v)
						i=i+1
					end
					for i = 0,29 do
						memory.write_u16_le(folder + i*4,tbl[i][1])
						memory.write_u16_le(folder + i*4 + 2,tbl[i][2])
					end
					print("Folder #"..FolderLoaded.." imported.")
				end
				RHeld = 1
			else
				RHeld = 0
			end
			
			-- Cycle Folders -1
			if joypad.get().L then
				if LHeld == 0 then
					FolderLoaded = FolderLoaded - 1
					if FolderLoaded < 1 then
						FolderLoaded = #importedFolders
					end
					local tbl = {}
					local i = 0
					for k,v in string.gmatch(importedFolders[FolderLoaded], "(%d+) (%d+)") do
						if tbl[math.floor(i/2)] == nil then tbl[math.floor(i/2)] = {} end
						tbl[math.floor(i/2)][(i%2)+1] = tonumber(k)
						i=i+1
						tbl[math.floor(i/2)][(i%2)+1] = tonumber(v)
						i=i+1
					end
					for i = 0,29 do
						memory.write_u16_le(folder + i*4,tbl[i][1])
						memory.write_u16_le(folder + i*4 + 2,tbl[i][2])
					end
					print("Folder #"..FolderLoaded.." imported.")
				end
				LHeld = 1
			else
				LHeld = 0
			end
		end
	end
	
	-- Turn on Edit Mode
	if joypad.get().Start and not StartHeld then
		StartHeld = true
		if (chipslot >= 0x02001410 and chipslot <= 0x2002000) then
			if edit == false then
				edit = true
			else
				edit = false
				chipslot = -1
			end
		else
			if #importedFolders < 1 then
				importedFolders = lines_from("folders.txt")
				print(#importedFolders .. " Folders loaded.")
			else
				importedFolders = {}
				print("Folders unloaded.")
			end
			FolderLoaded = 0
		end
	elseif not joypad.get().Start then
		StartHeld = false
	end
	
	-- Edit Mode
	if chipslot < 0x02000000 then
		chipslot = -1
		return
	end
	local chip = memory.read_u16_le(chipslot)
	local code = memory.read_u16_le(chipslot + 2)
	if edit == true then
		gui.pixelText(0,0,"Chip: "..chiplist.names[chip].." "..chiplist.codes[code].." ("..chip..")")
		gui.pixelText(0,7,"Edit Mode Active!")
		
		-- Set Chip ID
		if joypad.get().R then
			RHeld = RHeld + 1
			if RHeld >= 31 then RHeld = 31 end
			if RHeld == 1 or RHeld > 30 then
				if chip + 1 > 301 then chip = 301 else chip = chip + 1 end
				memory.write_u16_le(chipslot, chip)
				code = memory.readbyte(0x08011510 + chip*0x20)
				memory.write_u16_le(chipslot + 2, code)
			end
		else
			RHeld = 0
		end
		if joypad.get().L then
			LHeld = LHeld + 1
			if LHeld >= 31 then LHeld = 31 end
			if LHeld == 1 or LHeld > 30 then
				if chip - 1 < 0 then chip = 0 else chip = chip - 1 end
				memory.write_u16_le(chipslot, chip)
				code = memory.readbyte(0x08011510 + chip*0x20)
				memory.write_u16_le(chipslot + 2, code)
			end
		else
			LHeld = 0
		end
		
		-- Set Code ID
		if joypad.get().Right and not RightHeld then
			RightHeld = true
			for i=0,5 do
				local newcode = memory.readbyte(0x08011510 + chip*32 + i)
				if newcode == 0xFF then
					break
				elseif newcode > code then
					memory.write_u16_le(chipslot + 2, newcode)
					break
				end
			end
		elseif not joypad.get().Right then
			RightHeld = false
		end
		if joypad.get().Left and not LeftHeld then
			LeftHeld = true
			for i=0,5 do
				local newcode = memory.readbyte(0x08011510 + chip*32 + 5 - i)
				if newcode < code then
					memory.write_u16_le(chipslot + 2, newcode)
					break
				end
			end
		elseif not joypad.get().Left then
			LeftHeld = false
		end
		
		-- Save to File
		if joypad.get().Select and not SelHeld then
			SelHeld = true
			local folder = memory.read_u32_le(0x02009418)
			file = io.open("folders.txt", "a")
			for i = 0,29 do
				local endchip = memory.read_u16_le(folder + i*4)
				local endcode = memory.read_u16_le(folder + i*4 + 2)
				file:write(endchip.." "..endcode)
				if i < 29 then
					file:write(",")
				end
			end
			file:write("\n")
			io.close(file)
		elseif not joypad.get().Select then
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
	
	emu.frameadvance()
	gui.clearGraphics()
end

