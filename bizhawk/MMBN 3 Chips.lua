-- Battle Chip Info for MMBN 3 by Tterraj42, enjoy.

local chips = {};

chips.codes = {};
chips.codes[-1] = '-';
chips.codes[ 0] = 'A';
chips.codes[ 1] = 'B';
chips.codes[ 2] = 'C';
chips.codes[ 3] = 'D';
chips.codes[ 4] = 'E';
chips.codes[ 5] = 'F';
chips.codes[ 6] = 'G';
chips.codes[ 7] = 'H';
chips.codes[ 8] = 'I';
chips.codes[ 9] = 'J';
chips.codes[10] = 'K';
chips.codes[11] = 'L';
chips.codes[12] = 'M';
chips.codes[13] = 'N';
chips.codes[14] = 'O';
chips.codes[15] = 'P';
chips.codes[16] = 'Q';
chips.codes[17] = 'R';
chips.codes[18] = 'S';
chips.codes[19] = 'T';
chips.codes[20] = 'U';
chips.codes[21] = 'V';
chips.codes[22] = 'W';
chips.codes[23] = 'X';
chips.codes[24] = 'Y';
chips.codes[25] = 'Z';
chips.codes[26] = '*';
chips.codes['-'] = -1;
chips.codes['A'] =  0;
chips.codes['B'] =  1;
chips.codes['C'] =  2;
chips.codes['D'] =  3;
chips.codes['E'] =  4;
chips.codes['F'] =  5;
chips.codes['G'] =  6;
chips.codes['H'] =  7;
chips.codes['I'] =  8;
chips.codes['J'] =  9;
chips.codes['K'] = 10;
chips.codes['L'] = 11;
chips.codes['M'] = 12;
chips.codes['N'] = 13;
chips.codes['O'] = 14;
chips.codes['P'] = 15;
chips.codes['Q'] = 16;
chips.codes['R'] = 17;
chips.codes['S'] = 18;
chips.codes['T'] = 19;
chips.codes['U'] = 20;
chips.codes['V'] = 21;
chips.codes['W'] = 22;
chips.codes['X'] = 23;
chips.codes['Y'] = 24;
chips.codes['Z'] = 25;
chips.codes['*'] = 26;

chips.names = {};
chips.names[0] = "Empty";
chips.names[1] = "Cannon";
chips.names[2] = "HiCannon";
chips.names[3] = "M-Cannon";
chips.names[4] = "AirShot1";
chips.names[5] = "AirShot2";
chips.names[6] = "AirShot3";
chips.names[7] = "LavaCan1";
chips.names[8] = "LavaCan2";
chips.names[9] = "LavaCan3";
chips.names[10] = "ShotGun";
chips.names[11] = "V-Gun";
chips.names[12] = "SideGun";
chips.names[13] = "Spreader";
chips.names[14] = "Bubbler";
chips.names[15] = "Bub-V";
chips.names[16] = "BublSide";
chips.names[17] = "HeatShot";
chips.names[18] = "Heat-V";
chips.names[19] = "HeatSide";
chips.names[20] = "MiniBomb";
chips.names[21] = "SnglBomb";
chips.names[22] = "DublBomb";
chips.names[23] = "TrplBomb";
chips.names[24] = "CannBall";
chips.names[25] = "IceBall";
chips.names[26] = "LavaBall";
chips.names[27] = "BlkBomb1";
chips.names[28] = "BlkBomb2";
chips.names[29] = "BlkBomb3";
chips.names[30] = "Sword";
chips.names[31] = "WideSwrd";
chips.names[32] = "LongSwrd";
chips.names[33] = "FireSwrd";
chips.names[34] = "AquaSwrd";
chips.names[35] = "ElecSwrd";
chips.names[36] = "BambSwrd";
chips.names[37] = "CustSwrd";
chips.names[38] = "VarSwrd";
chips.names[39] = "StepSwrd";
chips.names[40] = "StepCros";
chips.names[41] = "Panic";
chips.names[42] = "AirSwrd";
chips.names[43] = "Slasher";
chips.names[44] = "ShockWav";
chips.names[45] = "SonicWav";
chips.names[46] = "DynaWave";
chips.names[47] = "GutPunch";
chips.names[48] = "GutStrgt";
chips.names[49] = "GutImpct";
chips.names[50] = "AirStrm1";
chips.names[51] = "AirStrm2";
chips.names[52] = "AirStrm3";
chips.names[53] = "DashAtk";
chips.names[54] = "Burner";
chips.names[55] = "Totem1";
chips.names[56] = "Totem2";
chips.names[57] = "Totem3";
chips.names[58] = "Ratton1";
chips.names[59] = "Ratton2";
chips.names[60] = "Ratton3";
chips.names[61] = "Wave";
chips.names[62] = "RedWave";
chips.names[63] = "MudWave";
chips.names[64] = "Hammer";
chips.names[65] = "Tornado";
chips.names[66] = "ZapRing1";
chips.names[67] = "ZapRing2";
chips.names[68] = "ZapRing3";
chips.names[69] = "Yo-Yo1";
chips.names[70] = "Yo-Yo2";
chips.names[71] = "Yo-Yo3";
chips.names[72] = "Spice1";
chips.names[73] = "Spice2";
chips.names[74] = "Spice3";
chips.names[75] = "Lance";
chips.names[76] = "Scuttlst";
chips.names[77] = "Momogra";
chips.names[78] = "Rope1";
chips.names[79] = "Rope2";
chips.names[80] = "Rope3";
chips.names[81] = "Magnum1";
chips.names[82] = "Magnum2";
chips.names[83] = "Magnum3";
chips.names[84] = "Boomer1";
chips.names[85] = "Boomer2";
chips.names[86] = "Boomer3";
chips.names[87] = "RndmMetr";
chips.names[88] = "HoleMetr";
chips.names[89] = "ShotMetr";
chips.names[90] = "IceWave1";
chips.names[91] = "IceWave2";
chips.names[92] = "IceWave3";
chips.names[93] = "Plasma1";
chips.names[94] = "Plasma2";
chips.names[95] = "Plasma3";
chips.names[96] = "Arrow1";
chips.names[97] = "Arrow2";
chips.names[98] = "Arrow3";
chips.names[99] = "TimeBomb";
chips.names[100] = "Mine";
chips.names[101] = "Sensor1";
chips.names[102] = "Sensor2";
chips.names[103] = "Sensor3";
chips.names[104] = "CrsShld1";
chips.names[105] = "CrsShld2";
chips.names[106] = "CrsShld3";
chips.names[107] = "Geyser";
chips.names[108] = "PoisMask";
chips.names[109] = "PoisFace";
chips.names[110] = "Shake1";
chips.names[111] = "Shake2";
chips.names[112] = "Shake3";
chips.names[113] = "BigWave";
chips.names[114] = "Volcano";
chips.names[115] = "Condor";
chips.names[116] = "Burning";
chips.names[117] = "FireRatn";
chips.names[118] = "Guard";
chips.names[119] = "PanlOut1";
chips.names[120] = "PanlOut3";
chips.names[121] = "Recov10";
chips.names[122] = "Recov30";
chips.names[123] = "Recov50";
chips.names[124] = "Recov80";
chips.names[125] = "Recov120";
chips.names[126] = "Recov150";
chips.names[127] = "Recov200";
chips.names[128] = "Recov300";
chips.names[129] = "PanlGrab";
chips.names[130] = "AreaGrab";
chips.names[131] = "Snake";
chips.names[132] = "Team1";
chips.names[133] = "MetaGel1";
chips.names[134] = "MetaGel2";
chips.names[135] = "MetaGel3";
chips.names[136] = "GrabBack";
chips.names[137] = "GrabRvng";
chips.names[138] = "Geddon1";
chips.names[139] = "Geddon2";
chips.names[140] = "Geddon3";
chips.names[141] = "RockCube";
chips.names[142] = "Prism";
chips.names[143] = "Wind";
chips.names[144] = "Fan";
chips.names[145] = "RockArm1";
chips.names[146] = "RockArm2";
chips.names[147] = "RockArm3";
chips.names[148] = "NoBeam1";
chips.names[149] = "NoBeam2";
chips.names[150] = "NoBeam3";
chips.names[151] = "Pawn";
chips.names[152] = "Knight";
chips.names[153] = "Rook";
chips.names[154] = "Needler1";
chips.names[155] = "Needler2";
chips.names[156] = "Needler3";
chips.names[157] = "SloGauge";
chips.names[158] = "FstGauge";
chips.names[159] = "Repair";
chips.names[160] = "Invis";
chips.names[161] = "Hole";
chips.names[162] = "Mole1";
chips.names[163] = "Mole2";
chips.names[164] = "Mole3";
chips.names[165] = "Shadow";
chips.names[166] = "Mettaur";
chips.names[167] = "Bunny";
chips.names[168] = "AirShoes";
chips.names[169] = "Team2";
chips.names[170] = "Fanfare";
chips.names[171] = "Discord";
chips.names[172] = "Timpani";
chips.names[173] = "Barrier";
chips.names[174] = "Barr100";
chips.names[175] = "Barr200";
chips.names[176] = "Aura";
chips.names[177] = "NrthWind";
chips.names[178] = "HolyPanl";
chips.names[179] = "LavaStge";
chips.names[180] = "IceStage";
chips.names[181] = "GrassStg";
chips.names[182] = "SandStge";
chips.names[183] = "MetlStge";
chips.names[184] = "Snctuary";
chips.names[185] = "Swordy";
chips.names[186] = "Spikey";
chips.names[187] = "Mushy";
chips.names[188] = "Jelly";
chips.names[189] = "KillrEye";
chips.names[190] = "AntiNavi";
chips.names[191] = "AntiDmg";
chips.names[192] = "AntiSwrd";
chips.names[193] = "AntiRecv";
chips.names[194] = "CopyDmg";
chips.names[195] = "Atk+10";
chips.names[196] = "Fire+30";
chips.names[197] = "Aqua+30";
chips.names[198] = "Elec+30";
chips.names[199] = "Wood+30";
chips.names[200] = "Navi+20";
chips.names[201] = "LifeAura";
chips.names[202] = "Muramasa";
chips.names[203] = "Guardian";
chips.names[204] = "Anubis";
chips.names[205] = "Atk+30";
chips.names[206] = "Navi+40";
chips.names[207] = "HeroSwrd";
chips.names[208] = "ZeusHamr";
chips.names[209] = "GodStone";
chips.names[210] = "OldWood";
chips.names[211] = "FullCust";
chips.names[212] = "Meteors";
chips.names[213] = "Poltrgst";
chips.names[214] = "Jealousy";
chips.names[215] = "StandOut";
chips.names[216] = "WatrLine";
chips.names[217] = "Ligtning";
chips.names[218] = "GaiaSwrd";
chips.names[219] = "Roll V1";
chips.names[220] = "Roll V2";
chips.names[221] = "Roll V3";
chips.names[222] = "GutsMan V1";
chips.names[223] = "GutsMan V2";
chips.names[224] = "GutsMan V3";
chips.names[225] = "GutsMan V4";
chips.names[226] = "GutsMan V5";
chips.names[227] = "ProtoMan V1";
chips.names[228] = "ProtoMan V2";
chips.names[229] = "ProtoMan V3";
chips.names[230] = "ProtoMan V4";
chips.names[231] = "Protoman V5";
chips.names[232] = "FlashMan V1";
chips.names[233] = "FlashMan V2";
chips.names[234] = "FlashMan V3";
chips.names[235] = "FlashMan V4";
chips.names[236] = "FlashMan V5";
chips.names[237] = "BeastMan V1";
chips.names[238] = "BeastMan V2";
chips.names[239] = "BeastMan V3";
chips.names[240] = "BeastMan V4";
chips.names[241] = "BeastMan V5";
chips.names[242] = "BubblMan V1";
chips.names[243] = "BubblMan V2";
chips.names[244] = "BubblMan V3";
chips.names[245] = "BubblMan V4";
chips.names[246] = "BubblMan V5";
chips.names[247] = "DesrtMan V1";
chips.names[248] = "DesrtMan V2";
chips.names[249] = "DesrtMan V3";
chips.names[250] = "DesrtMan V4";
chips.names[251] = "DesrtMan V5";
chips.names[252] = "PlantMan V1";
chips.names[253] = "PlantMan V2";
chips.names[254] = "PlantMan V3";
chips.names[255] = "PlantMan V4";
chips.names[256] = "PlantMan V5";
chips.names[257] = "FlamMan V1";
chips.names[258] = "FlamMan V2";
chips.names[259] = "FlamMan V3";
chips.names[260] = "FlamMan V4";
chips.names[261] = "FlamMan V5";
chips.names[262] = "DrillMan V1";
chips.names[263] = "DrillMan V2";
chips.names[264] = "DrillMan V3";
chips.names[265] = "DrillMan V4";
chips.names[266] = "DrillMan V5";
chips.names[267] = "MetalMan V1";
chips.names[268] = "MetalMan V2";
chips.names[269] = "MetalMan V3";
chips.names[270] = "MetalMan V4";
chips.names[271] = "MetalMan V5";
chips.names[272] = "Punk";
chips.names[273] = "Salamndr";
chips.names[274] = "Fountain";
chips.names[275] = "Bolt";
chips.names[276] = "GaiaBlad";
chips.names[277] = "KingMan V1";
chips.names[278] = "KingMan V2";
chips.names[279] = "KingMan V3";
chips.names[280] = "KingMan V4";
chips.names[281] = "KingMan V5";
chips.names[282] = "MistMan V1";
chips.names[283] = "MistMan V2";
chips.names[284] = "MistMan V3";
chips.names[285] = "MistMan V4";
chips.names[286] = "MistMan V5";
chips.names[287] = "BowlMan V1";
chips.names[288] = "BowlMan V2";
chips.names[289] = "BowlMan V3";
chips.names[290] = "BowlMan V4";
chips.names[291] = "BowlMan V5";
chips.names[292] = "DarkMan V1";
chips.names[293] = "DarkMan V2";
chips.names[294] = "DarkMan V3";
chips.names[295] = "DarkMan V4";
chips.names[296] = "DarkMan V5";
chips.names[297] = "JapanMan V1";
chips.names[298] = "JapanMan V2";
chips.names[299] = "JapanMan V3";
chips.names[300] = "JapanMan V4";
chips.names[301] = "JapanMan V5";
chips.names[302] = "DeltaRay";
chips.names[303] = "FoldrBak";
chips.names[304] = "NavRcycl";
chips.names[305] = "AlphArmSigma";
chips.names[306] = "Bass";
chips.names[307] = "Serenade";
chips.names[308] = "Balance";
chips.names[309] = "DarkAura";
chips.names[310] = "AlphArmOmega";
chips.names[311] = "Bass+";
chips.names[312] = "BassGS";
chips.names[320] = "Z-Canon1";
chips.names[321] = "Z-Canon2";
chips.names[322] = "Z-Canon3";
chips.names[323] = "Z-Punch";
chips.names[324] = "Z-Strght";
chips.names[325] = "Z-Impact";
chips.names[326] = "Z-Varibl";
chips.names[327] = "Z-Yoyo1";
chips.names[328] = "Z-Yoyo2";
chips.names[329] = "Z-Yoyo3";
chips.names[330] = "Z-Step1";
chips.names[331] = "Z-Step2";
chips.names[332] = "TimeBom+";
chips.names[333] = "H-Burst";
chips.names[334] = "BubSprd";
chips.names[335] = "HeatSprd";
chips.names[336] = "LifeSwrd";
chips.names[337] = "ElemSwrd";
chips.names[338] = "EvilCut";
chips.names[339] = "2xHero";
chips.names[340] = "HyperRat";
chips.names[341] = "EverCrse";
chips.names[342] = "GelRain";
chips.names[343] = "PoisPhar";
chips.names[344] = "BodyGrd";
chips.names[345] = "500Barr";
chips.names[346] = "BigHeart";
chips.names[347] = "GtsShoot";
chips.names[348] = "DeuxHero";
chips.names[349] = "MomQuake";
chips.names[350] = "PrixPowr";
chips.names[351] = "MstrStyl";
-- Various Buster Shots & Special Attacks
chips.names[384] = "Backup";

return chips;

