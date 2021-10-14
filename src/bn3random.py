import re
import random
import struct
import copy
import argparse
from collections import defaultdict
from pprint import pprint

compressed_data_end = 0
N_CHIPS = 312
N_PAS = 32
DATA_PATH="data/"

# Battle Obstacle List
obstacles = ["Mega Man", "Virus", "Rock", "RockCube", "MetalCube", "IceCube", "Guardian", "BlackBomb", "N/A", "Flag", "N/A", "MetalGear"]

# Chip Codes List
chip_codes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "*"]

# Virus Lists
# Weak: Mettaur, Canodumb, Fishy, Swordy, Shrimpy, Spikey, Bunny, Beetle, Trumpy, Quaker
weak_viruses = [1,2,3,4, 5,6,7,8, 9,10,11,12, 13,14,15,16, 29,30,31,32, 33,34,35,36, 37,38,39,40, 75,76,77,78, 123,124,125,126, 131,132,133,134]
# Med: Ratty, HardHead, Windbox, Metrid, Momogra, Pengi, Slimer, Eleball, Totem, Boomer
med_viruses = [17,18,19,20, 21,22,23,24, 41,42,43,44, 79,80,81,82, 91,92,93,94, 103,104,105,106, 111,112,113,114, 139,140,141,142, 147,148,149,150, 155,156,157,158]
# Strong: Puffball, Mushy, SnowBlow, Heavy, Needler, Volcano
strong_viruses = [45,46,47,48, 49,50,51,52, 83,84,85,86, 99,100,101,102, 119,120,121,122, 143,144,145,146]
# Powerful: Jelly, Yort, Brushman, KillerEye, Viney
powerful_viruses = [25,26,27,28, 57,58,59,60, 65,66,67,68, 87,88,89,90, 107,108,109,110]
# Dangerous: Dominerd, Basher, Elebee, AlphaBug, N.O
dangerous_viruses = [53,54,55,56, 95,96,97,98, 115,116,117,118, 127,128,129,130, 135,136,137,138]
# Banned: Shadow, Scuttle, Twins, Number, Number-M, Number-G
banned_viruses = [61,62,63,64, 69,70,71,72,73,74, 151,152,153,154, 159,160,161, 162,163,164, 165,166,167]
# Chaos Virus Exclusions: Banned
allviruses = [1,2,3,4, 5,6,7,8, 9,10,11,12, 13,14,15,16, 29,30,31,32, 33,34,35,36, 37,38,39,40, 75,76,77,78, 123,124,125,126, 131,132,133,134, 17,18,19,20, 21,22,23,24, 41,42,43,44, 79,80,81,82, 91,92,93,94, 103,104,105,106, 111,112,113,114, 139,140,141,142, 147,148,149,150, 155,156,157,158, 45,46,47,48, 49,50,51,52, 83,84,85,86, 99,100,101,102, 119,120,121,122, 143,144,145,146, 25,26,27,28, 57,58,59,60, 65,66,67,68, 87,88,89,90, 107,108,109,110, 53,54,55,56, 95,96,97,98, 115,116,117,118, 127,128,129,130, 135,136,137,138]
#allviruses = [1,5,9,13,29,33,37,75,123,131,17,21,41,79,91,103,111,139,147,155,45,49,83,99,119,143,25,57,65,87,107,53,95,115,127,135]

# Potentially Required NPC Trades
required_trades = [[0x20, 4], [0x3a, 2], [136, 10], [46, 21], [81, 0], [122, 26], [0x8f, 26], [0x45, 6], [0x19, 12], [45, 22], [14, 2], [125, 18], [110, 12], [110, 18], [33, 15], [31, 2], [88, 7], [165, 9], [99, 13], [46, 21]]
tradechiplist = []

# Navi Lists for Navi Randomizations
weak_navis = [0,4,32,40]
mid_navis = [8,20,48,52,56]
strong_navis = [12,16,24]
post_navis = [36,60,64]
allnavis = [0,4,8,12,16,20,24,32,36,40,44,48,52,56,60,64]
chosen_navis = list()
for i in range(0, 76):
    chosen_navis.append(-1)

special_virus_level = {
    168: 1,
    169: 2,
    170: 3,
    171: 4,
    172: 1,
    173: 2,
    174: 3,
    175: 4,
    176: 1,
    177: 2,
    178: 3,
    179: 4,
    180: 1,
    181: 2,
    182: 3,
    183: 4,
    184: 1,
    185: 2,
    186: 3,
    187: 4,
    188: 1,
    189: 2,
    190: 3,
    191: 4,
    192: 1,
    193: 2,
    194: 3,
    195: 4,
    196: 1,
    197: 2,
    198: -1,
    199: -1,
    200: 1,
    201: 2,
    202: 3,
    203: 4,
    204: 1,
    205: 2,
    206: 3,
    207: 4,
    208: 1,
    209: 2,
    210: 3,
    211: 4,
    212: 1,
    213: 2,
    214: 3,
    215: 4,
    216: 1,
    217: 2,
    218: 3,
    219: 4,
    220: 1,
    221: 2,
    222: 3,
    223: 4,
    224: 1,
    225: 2,
    226: 3,
    227: 4,
    228: 1,
    229: 2,
    230: 3,
    231: 4,
    232: 1,
    233: 2,
    234: 3,
    235: 4,
    236: 1,
    237: 2,
    238: 3,
    239: 4,
    240: 1,
    241: 2,
    242: 3,
    243: 4,
}

chip_hex = {
    1: 0x01,
    2: 0x02,
    3: 0x03,
    4: 0x04,
    5: 0x05,
    6: 0x06,
    7: 0x07,
    8: 0x08,
    9: 0x09,
    10: 0x72,
    11: 0x0A,
    12: 0x0B,
    13: 0x0C,
    14: 0x0D,
    15: 0x0E,
    16: 0x0F,
    17: 0x10,
    18: 0x11,
    19: 0x12,
    20: 0x13,
    21: 0x14,
    22: 0x15,
    23: 0x16,
    24: 0x17,
    25: 0x18,
    26: 0x19,
    27: 0x1A,
    28: 0x1B,
    29: 0x1C,
    30: 0x1D,
    31: 0x1E,
    32: 0x1F,
    33: 0x20,
    34: 0x21,
    35: 0x22,
    36: 0x23,
    37: 0x24,
    38: 0x25,
    39: 0x26,
    40: 0x2A,
    41: 0x27,
    42: 0x28,
    43: 0x2B,
    44: 0x2C,
    45: 0x2D,
    46: 0x2E,
    47: 0x71,
    48: 0x2F,
    49: 0x30,
    50: 0x31,
    51: 0x35,
    52: 0x36,
    53: 0x73,
    54: 0x74,
    55: 0x42,
    56: 0x43,
    57: 0x44,
    58: 0x5A,
    59: 0x5B,
    60: 0x5C,
    61: 0x45,
    62: 0x46,
    63: 0x47,
    64: 0x32,
    65: 0x33,
    66: 0x34,
    67: 0x60,
    68: 0x61,
    69: 0x62,
    70: 0x3A,
    71: 0x3B,
    72: 0x3C,
    73: 0x75,
    74: 0x3D,
    75: 0x3E,
    76: 0x3F,
    77: 0x41,
    78: 0x48,
    79: 0x49,
    80: 0x4A,
    81: 0x6E,
    82: 0x6F,
    83: 0x70,
    84: 0x94,
    85: 0x95,
    86: 0x96,
    87: 0x40,
    88: 0x6B,
    89: 0x4E,
    90: 0x4F,
    91: 0x50,
    92: 0x54,
    93: 0x55,
    94: 0x56,
    95: 0x6C,
    96: 0x6D,
    97: 0x91,
    98: 0x92,
    99: 0x93,
    100: 0x68,
    101: 0x69,
    102: 0x6A,
    103: 0x51,
    104: 0x52,
    105: 0x53,
    106: 0x5D,
    107: 0x5E,
    108: 0x5F,
    109: 0x57,
    110: 0x58,
    111: 0x59,
    112: 0x9A,
    113: 0x9B,
    114: 0x9C,
    115: 0x37,
    116: 0x38,
    117: 0x39,
    118: 0x65,
    119: 0x66,
    120: 0x67,
    121: 0x85,
    122: 0x86,
    123: 0x87,
    124: 0x97,
    125: 0x98,
    126: 0x99,
    127: 0x84,
    128: 0xA9,
    129: 0x63,
    130: 0x64,
    131: 0x4B,
    132: 0x83,
    133: 0x76,
    134: 0x77,
    135: 0x78,
    136: 0x81,
    137: 0x82,
    138: 0x88,
    139: 0x89,
    140: 0x8D,
    141: 0x8E,
    142: 0x8F,
    143: 0x90,
    144: 0xAA,
    145: 0xAB,
    146: 0xAC,
    147: 0x79,
    148: 0x7A,
    149: 0x7B,
    150: 0x7C,
    151: 0x7D,
    152: 0x7E,
    153: 0x7F,
    154: 0x80,
    155: 0x9F,
    156: 0x9D,
    157: 0x9E,
    158: 0x29,
    159: 0x8A,
    160: 0x8B,
    161: 0x8C,
    162: 0xC2,
    163: 0xA0,
    164: 0xA5,
    165: 0xA2,
    166: 0xA3,
    167: 0xA4,
    168: 0xA8,
    169: 0xAD,
    170: 0xAE,
    171: 0xAF,
    172: 0xB0,
    173: 0xB1,
    174: 0xA6,
    175: 0xA7,
    176: 0xBA,
    177: 0xB9,
    178: 0xBC,
    179: 0xBB,
    180: 0x4D,
    181: 0xBD,
    182: 0x4C,
    183: 0xA1,
    184: 0xB2,
    185: 0xB3,
    186: 0xB4,
    187: 0xB5,
    188: 0xB6,
    189: 0xB7,
    190: 0xB8,
    191: 0xBF,
    192: 0xC0,
    193: 0xBE,
    194: 0xC1,
    195: 0xC3,
    196: 0xC4,
    197: 0xC5,
    198: 0xC6,
    199: 0xC7,
    200: 0xC8,
    
    201: 0xC9,
    202: 0xCA,
    203: 0xCB,
    204: 0xCC,
    205: 0xCD,
    206: 0xCE,
    207: 0xCF,
    208: 0xD0,
    209: 0xD1,
    210: 0xD2,
    211: 0xD3,
    212: 0xD4,
    213: 0xD5,
    214: 0xD6,
    215: 0xD7,
    216: 0xD8,
    217: 0xD9,
    218: 0xDA,
    219: 0xDB,
    220: 0xDC,
    221: 0xDD,
    222: 0xDE,
    223: 0xDF,
    224: 0xE0,
    225: 0xE1,
    226: 0xE2,
    227: 0xE3,
    228: 0xE4,
    229: 0xE5,
    230: 0xE6,
    231: 0xE7,
    232: 0xE8,
    233: 0xE9,
    234: 0xEA,
    235: 0xEB,
    236: 0xEC,
    237: 0xED,
    238: 0xEE,
    239: 0xEF,
    240: 0xF0,
    241: 0xF1,
    242: 0xF2,
    243: 0xF3,
    244: 0xF4,
    245: 0xF5,
    246: 0xF6,
    247: 0xF7,
    248: 0xF8,
    249: 0xF9,
    250: 0xFA,
    251: 0xFB,
    252: 0xFC,
    253: 0xFD,
    254: 0xFE,
    255: 0xFF,
    256: 0x0100,
    257: 0x0101,
    258: 0x0102,
    259: 0x0103,
    260: 0x0104,
    261: 0x0105,
    262: 0x0106,
    263: 0x0107,
    264: 0x0108,
    265: 0x0109,
    266: 0x010A,
    267: 0x010B,
    268: 0x010C,
    269: 0x010D,
    270: 0x010E,
    271: 0x010F,
    272: 0x0110,
    273: 0x0110,
    274: 0x0111,
    275: 0x0112,
    276: 0x0113,
    277: 0x0114,
    278: 0x0115,
    279: 0x0116,
    280: 0x0118,
    281: 0x0119,
    282: 0x011A,
    283: 0x011B,
    284: 0x011C,
    285: 0x011D,
    286: 0x011E,
    287: 0x011F,
    288: 0x0120,
    289: 0x0121,
    290: 0x0122,
    291: 0x0123,
    292: 0x0124,
    293: 0x0125,
    294: 0x0126,
    295: 0x0127,
    296: 0x0128,
    297: 0x0129,
    298: 0x012A,
    299: 0x012B,
    300: 0x012C,
    301: 0x012D,
    302: 0x012E,
    303: 0x012F,
    304: 0x0130,
    305: 0x0131,
    306: 0x0132,
    307: 0x0133,
    308: 0x0134,
    309: 0x0135,
    310: 0x0136,
    311: 0x0137,
    312: 0x0138,
}

# Text Characters
mmchars = [" ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "-", "[smallx]", "=", ":", "+", "[divide]", "[burst]", "*", "!", "?", "%", "&", ",", "[hollowbox]", ".", "[tinydot]", ";", "'", '"', "~", "/", "(", ")", "[leftJbracket]", "[rightJbracket]", "[V2]", "[V3]", "[V4]", "[V5]", "@", "[heart]", "[note]", "[MB]", "[box]", "_", "[circle1]", "[circle2]", "[cross1]", "[cross2]", "[bracket1]", "[bracket2]", "[ModTools1]", "[ModTools2]", "[ModTools3]", "[sigma]", "[omega]", "[alpha]", "[beta]", "#", "[ellipses]", ">", "<", "[weirdIthing]"]
chipnames_in_order = ["Cannon","HiCannon","M-Cannon","AirShot1","AirShot2","AirShot3","LavaCan1","LavaCan2","LavaCan3","ShotGun","V-Gun","SideGun","Spreader","Bubbler","Bub-V","BublSide","Heatshot","Heat-V","HeatSide","MiniBomb","SnglBomb","DublBomb","TrplBomb","CannBall","IceBall","LavaBall","BlkBomb1","BlkBomb2","BlkBomb3","Sword","WideSwrd","LongSwrd","FireSwrd","AquaSwrd","ElecSwrd","BambSwrd","CustSwrd","VarSwrd","StepSwrd","StepCros","Panic","AirSwrd","Slasher","ShockWav","SonicWav","DynaWave","GutPunch","GutStrgt","GutImpct","AirStrm1","AirStrm2","AirStrm3","DashAtk","Burner","Totem1","Totem2","Totem3","Ratton1","Ratton2","Ratton3","Wave","RedWave","MudWave","Hammer","Tornado","Zapring1","Zapring2","Zapring3","Yo-Yo1","Yo-Yo2","Yo-Yo3","Spice1","Spice2","Spice3","Lance","Scuttlst","Momogra","Rope1","Rope2","Rope3","Magnum1","Magnum2","Magnum3","Boomer1","Boomer2","Boomer3","RndmMetr","HoleMetr","ShotMetr","IceWave1","IceWave2","IceWave3","Plasma1","Plasma2","Plasma3","Arrow1","Arrow2","Arrow3","TimeBomb","Mine","Sensor1","Sensor2","Sensor3","CrsShld1","CrsShld2","CrsShld3","Geyser","PoisMask","PoisFace","Shake1","Shake2","Shake3","BigWave","Volcano","Condor","Burning","FireRatn","Guard","PanlOut1","PanlOut3","Recov10","Recov30","Recov50","Recov80","Recov120","Recov150","Recov200","Recov300","PanlGrab","AreaGrab","Snake","Team1","MetaGel1","MetaGel2","MetaGel3","GrabBack","GrabRvng","Geddon1","Geddon2","Geddon3","RockCube","Prism","Wind","Fan","RockArm1","RockArm2","RockArm3","NoBeam1","NoBeam2","NoBeam3","Pawn","Knight","Rook","Needler1","Needler2","Needler3","SloGauge","FstGauge","Repair","Invis","Hole","Mole1","Mole2","Mole3","Shadow","Mettaur","Bunny","AirShoes","Team2","Fanfare","Discord","Timpani","Barrier","Barr100","Barr200","Aura","NrthWind","HolyPanl","LavaStge","IceStage","GrassStg","SandStge","MetlStge","Snctuary","Swordy","Spikey","Mushy","Jelly","KillrEye","AntiNavi","AntiDmg","AntiSwrd","AntiRecv","CopyDmg","Atk+10","Fire+30","Aqua+30","Elec+30","Wood+30","Navi+20","LifeAura","Muramasa","Guardian","Anubis","Atk+30","Navi+40","HeroSwrd","ZeusHamr","GodStone","OldWood","FullCust","Meteors","Poltrgst","Jealousy","StandOut","WatrLine","Ligtning","GaiaSwrd","Roll","RollV2","RollV3","Gutsman","GutsmanV2","GutsmanV3","GustmanV4","GutsManV5","Protoman","ProtomnV2","ProtomnV3","ProtomnV4","ProtoMnV5","Flashman","FlashmnV2","FlashmnV3","FlashmnV4","FlashMnV5","Beastman","BeastmnV2","BeastmnV3","BeastmnV4","BeastMnV5","BubblMan","BubblMnV2","BubblMnV3","BubblMnV4","BubblMnV5","DesrtMan","DesrtMnV2","DesrtMnV3","DesrtMnV4","DesrtMnV5","PlantMan","PlantMnV2","PlantMnV3","PlantMnV4","PlantMnV5","FlamMan","FlamManV2","FlamManV3","FlamManV4","FlamManV5","DrillMan","DrillMnV2","DrillMnV3","DrillMnV4","DrillMnV5","MetalMan","MetalMnV2","MetalMnV3","MetalMnV4","MetalMnV5","Punk","Salamndr","Fountain","Bolt","GaiaBlad","KingMan","KingManV2","KingManV3","KingManV4","KingMnV5","MistMan","MistManV2","MistManV3","MistManV4","MistManV5","BowlMan","BowlManV2","BowlManV3","BowlManV4","BowlManV5","DarkMan","DarkManV2","DarkManV3","DarkManV4","DarkManV5","JapanMan","JapanMnV2","JapanMnV3","JapanMnV4","JapanMnV5","DeltaRay","FoldrBak","NavRcycl","AlphArmS","Bass","Serenade","Balance","DarkAura","AlphArmO","Bass+","BassGS"]

def checkval(val):
    if re.fullmatch(r"(?s)[\x00-\xff]?", str(val)) and not type(val) == int:
        return ord(val)
    return int(val)

def virus_level(virus):
    if virus == 0 or (virus >= 0x9f and virus < 168):
        return -1
    if virus in special_virus_level:
        return special_virus_level[virus]
    if virus < 0x45:
        return (virus + 3) % 4
    elif virus < 0x4a:
        return 3
    else:
        return (virus + 1) % 4

def init_custom_folders():
    global folder_data
    folder_data = open(DATA_PATH + 'folders_custom.txt', 'r').read().strip()
    folder_data = list(map(lambda s: list(map(lambda s2: navi_data_setup(s2), s.split(','))), folder_data.split('\n')))

def init_virus_data():
    global virus_data
    virus_data = open(DATA_PATH + 'virus_data.txt', 'r').read().strip()
    virus_data = list(map(lambda s: list(map(lambda s2: navi_data_setup(s2), s.split(' '))), virus_data.split('\n')))
    global navi_data
    navi_data = open(DATA_PATH + 'navi_data.txt', 'r').read().strip()
    navi_data = list(map(lambda s: list(map(lambda s2: navi_data_setup(s2), s.split(' '))), navi_data.split('\n')))
    
def navi_data_setup(args):
    value = args
    if args.find('0x') > -1:
        return int(value, 0)
    else:
        return str(value)

def init_rom_data(rom_path):
    global rom_data
    global randomized_data
    rom_data = ''.join(chr(x) for x in list(open(rom_path, 'rb').read()))
    randomized_data = list(map(lambda x: checkval(x), rom_data))
    return [rom_data, randomized_data]

def read_byte(offset):
    global rom_data
    return checkval(rom_data[offset])
def read_halfword(offset):
    global rom_data
    s = list(map(checkval, rom_data[offset:offset+2]))
    result = 0
    for i in range(len(s)):
        result += s[i] << (i*8)
    return result
def read_word(offset):
    global rom_data
    s = list(map(checkval, rom_data[offset:offset+4]))
    result = 0
    for i in range(len(s)):
        result += s[i] << (i*8)
    return result
def read_dblword(offset):
    global rom_data
    s = list(map(checkval, rom_data[offset:offset+8]))
    result = 0
    for i in range(len(s)):
        result += s[i] << (i*8)
        return result

def init_chip_data():
    s = 0x11530
    global chip_data
    global chip_names
    global chip_prices
    global allcodes
    chip_data = []
    sequence_pas = [1,2,3,13,14,15,16,17,18,19,38,39,40,47,48,49,69,70,71,99,133,134,135]
    specific_pas = [[14,15,16],[17,18,19],[30,31,32],[33,34,35,36],[39,207,40],[58,59,60],[104,105,106],[108,109,204],[190,191,202],[173,174,175],[128,178,219,220,221],[53,118,222,223,224,225],[38,37,43,227,228,229,230],[273,274,275,276]]
    allcodes = [[255 for x in range(6)] for y in range(N_CHIPS)]

    # Load in chip ranks from file
    chip_ranks = open(DATA_PATH +'chip_data.txt', 'r').read().strip()
    chip_ranks = list(map(int, chip_ranks.split('\n')))

    chip_names = open(DATA_PATH +'chip_names.txt', 'r').read().strip()
    chip_names = chip_names.split('\n')
    
    chip_prices = open(DATA_PATH +'chip_prices.txt', 'r').read().strip().split('\n')
    nameoffset = 0x704c09
    if ROMVERSION == "b":
        nameoffset = 0x7045F5
    
    chip_randnames = open(DATA_PATH +'chip_randomnames.txt', 'r').read().strip().split('\n')
    
    chip_attack = open(DATA_PATH +'chip_attackpower.txt', 'r').read().strip()
    chip_attack = chip_attack.split('\n')
    
    chip_reg = open(DATA_PATH +'regmem.txt','r').read().strip().split('\n')

    chip_data.append({})
    
    for i in range(N_CHIPS):
        code1, code2, code3, code4, code5, code6, element, filler, extra, regsize, chip_type, power, num = struct.unpack('<BBBBBBBBHBBHH', bytes(rom_data[s:s+16], encoding="raw_unicode_escape"))
        # chip_type seems to be a bitfield, only look at lsb for now
        is_attack = (chip_type & 1)
        codes = [code1, code2, code3, code4, code5, code6]
        while codes.count(255) > 0:
            codes.remove(255)
        purecodes = [code1, code2, code3, code4, code5, code6]
        
        rank = chip_ranks[i]
        name = chip_names[i]
        power = chip_attack[i]
        
        allcodes[i] = codes
        if ALLOW_CHIPS == 1:
            #Element Randomizer
            if ELEMENT_MODE >= 2:
                element = random.randint(0,4)
                write_data(chr(element),s+6)
            
            #RegMem Randomizer
            if REGMEM_MODE >= 1:
                regsize = random.randint(1, REGMEM_MODE)
                write_data(chr(regsize), s+10)
            else:
                regsize = int(chip_reg[i])
                write_data(chr(regsize), s+10)
            
            #All Stars Mode
            if C_ALLSTARMODE == int(0):
                allcodes[i] = purecodes
            if C_ALLSTARMODE == int(1):
                #codes = filter(lambda x : x != 255, [26,26,26,26,26,26])
                allcodes[i] = [26,26,26,26,26,26]
                #Reorganize Codes
                for j in range(len(purecodes)):
                    if purecodes[j] == 26:
                        purecodes[j] = 26
                    elif purecodes[j] == 255:
                        purecodes[j] = 255
                    else:
                        purecodes[j] = allcodes[i][j]
                allcodes[i] = purecodes
            #Simplified Mode
            if C_ALLSTARMODE == int(2):
                #codes = filter(lambda x : x != 255, [0,1,2,3,4,26])
                allcodes[i] = [0,1,2,3,4,26]
                # Make sure Trades are kept in-tact
                if ALLOW_TRADES == 0:
                    if num == 61:
                        allcodes[i][4] = 6
                    if num == 26:
                        allcodes[i][4] = 12
                if num > 200:
                    allcodes[i][0] = 26
                #Reorganize Codes
                for j in range(len(purecodes)):
                    if purecodes[j] == 26:
                        purecodes[j] = 26
                    elif purecodes[j] == 255:
                        purecodes[j] = 255
                    else:
                        purecodes[j] = allcodes[i][j]
                allcodes[i] = purecodes
            #Chaos Mode
            if C_ALLSTARMODE == int(3):
                # Make SURE no 2 codes are the same.
                newcodes = []
                while len(newcodes) < 6:
                    # Fix Program Advances
                    if i+1 in sequence_pas:
                        code = random.randint(0,21)
                        for j in range(5):
                            newcodes.append(code+j)
                    for j in specific_pas:
                        if i+1 in j:
                            for k in j:
                                if i+1 > k:
                                    if allcodes[k-1][0] in newcodes:
                                        continue
                                    newcodes.append(allcodes[k-1][0])
                    c = random.randint(0,25)
                    if c in newcodes:
                        continue
                    if len(newcodes) < 5:
                        newcodes.append(c)
                    if len(newcodes) == 5:
                        newcodes.append(26)
                allcodes[i] = newcodes
                # Make sure trades are kept in-tact.
                if ALLOW_TRADES == 0:
                    if num == 70:
                        allcodes[i][0] = 2
                    if num == 33:
                        allcodes[i][0] = 4
                    if num == 61:
                        allcodes[i][1] = 6
                    if num == 26:
                        allcodes[i][2] = 12
                if num > 200:
                    allcodes[i][0] = random.randint(0,26)
                #Reorganize Codes
                for j in range(len(purecodes)):
                    if purecodes[j] == 26:
                        purecodes[j] = 26
                    elif purecodes[j] == 255:
                        purecodes[j] = 255
                    else:
                        purecodes[j] = allcodes[i][j]
                allcodes[i] = purecodes
            
            #Write new Chip Codes
            write_data(chr(allcodes[i][0]), s)
            write_data(chr(allcodes[i][1]), s+1)
            write_data(chr(allcodes[i][2]), s+2)
            write_data(chr(allcodes[i][3]), s+3)
            write_data(chr(allcodes[i][4]), s+4)
            write_data(chr(allcodes[i][5]), s+5)
            # Fix the list, for some reason having all 6 codes for some chips breaks something later.
            while allcodes[i].count(255) > 0:
                allcodes[i].remove(255)
            
            old_power = power
            if int(power) > 0 and int(power) < 10000:
                power = int(float(power) * float(1 + (float(float(random.randint(-100,100)/100)) * P_VARIANCE)) * P_MULTIPLIER)
                power -= power % 5
                if power < 5:
                    power = 5
                #print 'New Power: ', power, (power // (2 ** 8) % 256 * 256) + (power % 256)
                write_data(chr(power % 256)+chr(power // (2 ** 8) % 256), s + 12)
            
            if ROMVERSION == "b" and nameoffset == 0x704e10 +1:
                nameoffset = 0x704f16
            if ROMVERSION == "w" and nameoffset == 0x705424 +1:
                nameoffset = 0x70552A
            
            # Chip Name Randomizer
            final_name = name
            if CP_NAMERANDOMIZER == 1:
                nameoffset, final_name = randomize_name(nameoffset, name, chip_randnames)
            
            #Output log stuff
            textcodes = []
            for j in purecodes:
                if j > 26:
                    textcodes.append("-")
                    continue
                textcodes.append(chip_codes[j])
            changelog_chip.append([name, final_name, old_power, power, str(textcodes), regsize])

            #if name == 'VarSwrd':
            #   power = 60
            #   write_data(chr(60), s + 12)

        # Conditional attacks
        is_conditional = name in ['Spice1', 'Spice2', 'Spice3', 'BlkBomb1', 'BlkBomb2', 'BlkBomb3', 'GrabBack', 'GrabRvng', 'Snake', 'Team1', 'Slasher', 'NoBeam1', 'NoBeam2', 'NoBeam3']
            
        chip = {
            'name' : name,
            'codes' : codes,
            'is_attack' : bool(is_attack),
            'is_conditional' : is_conditional,
            'regsize' : regsize,
            'power' : power,
            'num' : num,
            'rank' : rank,
        }

        chip_data.append(chip)
        s += 32

def init_pa_data():
    s = 0x13D10
    global pa_data
    global pa_names
    pa_data = []

    # Load in chip ranks from file
    pa_ranks = open(DATA_PATH +'pa_data.txt', 'r').read().strip()
    pa_ranks = list(map(int, pa_ranks.split('\n')))
    
    pa_names = open(DATA_PATH +'pa_names.txt', 'r').read().strip()
    pa_names = pa_names.split('\n')
    
    chip_randnames = open(DATA_PATH +'chip_randomnames.txt', 'r').read().strip().split('\n')
    nameoffset = 0x70571B
    if ROMVERSION == "b":
        nameoffset = 0x705107
    
    pa_attack = open(DATA_PATH +'pa_attackpower.txt', 'r').read().strip()
    pa_attack = pa_attack.split('\n')

    pa_data.append({})
    for i in range(N_PAS):
        code1, code2, code3, code4, code5, code6, element, filler, extra, regsize, chip_type, power, num = struct.unpack('<BBBBBBBBHBBHH', bytes(rom_data[s:s+16], encoding="raw_unicode_escape"))
        # chip_type seems to be a bitfield, only look at lsb for now
        is_attack = (chip_type & 1)
        codes = [code1, code2, code3, code4, code5, code6]
        while codes.count(255) > 0:
            codes.remove(255)
        rank = pa_ranks[i]
        name = pa_names[i]
        power = pa_attack[i]
        
        if ALLOW_CHIPS == 1:
            #Element Randomizer
            if ELEMENT_MODE >= 2:
                if element > 0:
                    element = random.randint(0,4)
                else:
                    element = random.randint(1,4)
                write_data(chr(element),s+6)
            
            #print 'Old Power: ', power
            old_power = power
            if int(power) > 0 and int(power) < 9999:
                power = int(float(power) * float(1 + (float(float(random.randint(-100,100)/100)) * P_VARIANCE)) * P_MULTIPLIER)
                power -= power % 5
                if power < 5:
                    power = 5
                if power > 9000:
                    power = 9000
                #print 'New: ', power, (power // (2 ** 8) % 256 * 256) + (power % 256)
                write_data(chr(power % 256)+chr(power // (2 ** 8) % 256), s + 12)
            
            
            # Chip Name Randomizer
            final_name = name
            if CP_NAMERANDOMIZER == 1:
                nameoffset, final_name = randomize_name(nameoffset, name, chip_randnames)
            changelog_chip.append([name, final_name, old_power, power, "N/A", "N/A"])
            
        # Conditional attacks
        is_conditional = name in ['Spice1', 'Spice2', 'Spice3', 'BlkBomb1', 'BlkBomb2', 'BlkBomb3', 'GrabBack', 'GrabRvng', 'Snake', 'Team1', 'Slasher', 'NoBeam1', 'NoBeam2', 'NoBeam3']
        
        chip = {
            'name' : name,
            'codes' : codes,
            'is_attack' : bool(is_attack),
            'is_conditional' : is_conditional,
            'regsize' : regsize,
            'power' : power,
            'num' : num,
            'rank' : rank,
        }

        pa_data.append(chip)
        s += 32

def fix_pas():
    s = 0xD684
    fixed_pas = []
    for i in range(0, 0x34):
        base_pa, pa_code_offset, chip = struct.unpack("<BBH", bytes(rom_data[s + i * 4 : s + 4 + i * 4], encoding="raw_unicode_escape"))
        old_code_offset = pa_code_offset
        if len(fixed_pas) > 0:
            count = 0
            for check in fixed_pas:
                if base_pa in check:
                    count += 1
            pa_code_offset = 0x1 + 0x2 * allcodes[chip-1][count]
            fixed_pas.append([base_pa, pa_code_offset])
        else:
            pa_code_offset = 0x1 + 0x2 * allcodes[chip-1][0]
            fixed_pas.append([base_pa, pa_code_offset])
        write_data(chr(pa_code_offset), s + 1 + i * 4)
        changelog_pas.append([base_pa, old_code_offset, pa_code_offset])
    

def mmbn3_text_parse(char):
    bn3c = ""
    for bn3c in mmchars:
        if char == bn3c:
            return chr(mmchars.index(bn3c))
    return ""

def write_data(s, offset):
    global randomized_data
    while offset + len(s) - len(randomized_data) > 0:
        randomized_data.append(chr(0xFF))
    for i in range(len(s)):
        randomized_data[offset + i] = s[i]

def decompress_data(offset):
    global compressed_data_end
    decompressed_size = read_word(offset) >> 8;
    offset += 4
    output = []
    while len(output) < decompressed_size:
        flags = read_byte(offset)
        offset += 1
        for i in range(8):
            is_special = bool(flags & 0x80)
            if is_special:
                a = read_byte(offset)
                b = read_byte(offset+1)
                x_len = (a >> 4) + 3
                x_offset = (b + ((a & 0xf) << 8))
                start = len(output) - 1 - x_offset
                for j in range(x_len):
                    output.append(output[start + j])
                offset += 2
            else:
                output.append(read_byte(offset))
                offset += 1
            flags <<= 1;
    output = output[:decompressed_size]
    compressed_data_end = offset
    return ''.join(list(map(lambda x : chr(x), output)))

def compress_data(raw_data):
    ops = []
    i = 0
    data_len = len(raw_data)
    while i < data_len:
        lo = 2
        hi = min(18, len(raw_data) - i)
        start = max(0, i - 4096)
        last_match_ind = -1
        while lo < hi:
            mid = int((lo + hi + 1) / 2)
            ss = raw_data[i : i + mid]
            t = raw_data.find(ss, start)
            if t < i:
                # match found
                last_match_ind = t
                lo = mid
            else:
                hi = mid - 1
        if lo < 3:
            ops.append((0, ord(raw_data[i])))
            i += 1
        else:
            ops.append((i - last_match_ind, lo))
            i += lo
    # Add some padding
    n_padding = (8 - (len(ops) % 8)) % 8
    for i in range(n_padding):
        ops.append((0, 0))
    # Encode the string
    output = [0x10, data_len & 0xff, (data_len >> 8) & 0xff, (data_len >> 16) & 0xff]
    for i in range(0, len(ops), 8):
        flags = 0
        for j in range(8):
            flags <<= 1
            if ops[i + j][0] > 0:
                flags |= 1
        output.append(flags)
        for j in range(8):
            if ops[i + j][0] == 0:
                output.append(ops[i + j][1])
            else:
                o, l = ops[i + j]
                o -= 1
                l -= 3
                output.append( ((l & 0xf) << 4) + ((o >> 8) & 0xf) )
                output.append(o & 0xff)
    return ''.join(list(map(chr, output)))

def randomize_gmds():
    global compressed_data_end

    # Works in Blue now.
    base_offset = 0x28810
    if ROMVERSION == "b":
        base_offset = 0x287f8
    free_space = 0x67c000
    map_data = {
        0x10: [0, 1, 2],
        0x11: [0, 1],
        0x12: [0, 1],
        0x13: [0, 1, 3],
        0x14: [0, 1, 2, 3, 4, 5, 6],
        0x15: [0, 1, 2]
    }
    new_scripts = {}
    area = 0x10
    subarea = 0x0
    chip_regex = re.compile(r'(?s)\xf1\x00\xfb\x04\x0f(.{32})')
    zenny_regex = re.compile(r'(?s)\xf1\x00\xfb\x00\x0f(.{64})')
    earliest_script = 999999999
    end_addr = -1
    chip_map = generate_chip_permutation()
    
    for (area, subareas) in list(map_data.items()):
        for subarea in subareas:
            script_ptr = read_word(base_offset + 4 * area) - 0x08000000 + 4 * subarea
            script_addr = read_word(script_ptr) - 0x08000000
            earliest_script = min(earliest_script, script_ptr)
            script_data = decompress_data(script_addr)
            end_addr = max(end_addr, compressed_data_end)
            new_data = list(map(ord, script_data))

            # Replace chip tables
            for match in chip_regex.finditer(script_data):
                match_offset = match.start() + 5
                x = list(map(lambda x : checkval(x), list(match.groups()[0])))
                for i in range(0, len(x), 2):
                    old_chip = x[i]
                    new_chip = chip_map[old_chip]
                    new_code = random.choice(allcodes[new_chip-1])
                    new_data[match_offset + i] = new_chip
                    new_data[match_offset + i+1] = new_code
                    changelog_gmd.append(["chip", old_chip, new_chip, new_code])

            # Multiply zenny tables
            for match in zenny_regex.finditer(script_data):
                match_offset = match.start() + 5
                zennys = list(struct.unpack('<IIIIIIIIIIIIIIII', bytes(match.groups()[0], encoding="raw_unicode_escape")))
                for i in range(16):
                    zennys[i] = (zennys[i] * 3) / 2
                zenny_str = struct.pack('<IIIIIIIIIIIIIIII', *(int(x) for x in zennys))
                for i in range(len(zenny_str)):
                    new_data[match_offset + i] = zenny_str[i]
                changelog_gmd.append(["zenny", zennys[0], zennys[1], zennys[2], zennys[3], zennys[4], zennys[5], zennys[6], zennys[7], zennys[8], zennys[9], zennys[10], zennys[11], zennys[12], zennys[13], zennys[14], zennys[15]])

            new_script = ''.join(list(map(chr, new_data)))
            new_scripts[script_ptr] = compress_data(new_script)

    # Get the missing scripts
    script_ptr = earliest_script
    while True:
        script_addr = read_word(script_ptr)
        if script_addr == 0:
            break
        if script_ptr not in new_scripts:
            script_addr -= 0x08000000
            script_data = compress_data(decompress_data(script_addr))
            new_scripts[script_ptr] = script_data
        script_ptr += 4

    start_addr = read_word(earliest_script) - 0x08000000
    # Write all the scripts back
    for (script_ptr, script_data) in list(new_scripts.items()):
        #print hex(script_ptr), hex(start_addr), hex(free_space)
        if start_addr + len(script_data) < end_addr:
            write_data(script_data, start_addr)
            write_data(struct.pack('<I', start_addr + 0x08000000), script_ptr)
            start_addr += len(script_data)
            # Pad up to multiple of 4
            start_addr += (4 - start_addr) % 4
        else:
            write_data(script_data, free_space)
            write_data(struct.pack('<I', free_space + 0x08000000), script_ptr)
            free_space += len(script_data)
            # Pad up to multiple of 4
            free_space += (4 - free_space) % 4
            
    print('randomized gmds')

def randomize_bmds_trades():
    global rom_data
    global randomized_data
    global tradechiplist
    global compressed_data_end
    old_data = rom_data
    rom_data = randomized_data
    
    if ALLOW_TRADES == 0 and ALLOW_BMD == 0:
        rom_data = old_data
        return
    
    # Works in Blue now.
    pattern_list = []
    tradechiplist = []
    samechiplist = []
    bmdchiplist = []
    
    available_chips = []
    for i in range(1,301):
        if i == 279:
            continue
        available_chips.append(i)
    
    free_space = len(old_data)
    if ROMVERSION == "b":
        base_offset = 0x28854
        pattern_list.append([0, 0x2664c])
    else:
        base_offset = 0x2886C
        pattern_list.append([0, 0x26664])
    new_scripts = []
    ptr = 0x0
    p = 0
    chip_regex = re.compile(r'(?s)\xf6\x10([\s\S][\x00-\x01])([\x00-\x1a])[\x01-\x03]')
    zenny_regex = re.compile(r'(?s)\xf6\x30([\s\S]{4})(\xff{3})((((\x16\x25\x32)|(\x17\x29\x2b\x25\x17\x25\x32))\x00(\x2b\x33\x38[\x00\x42]\xe8\x51))|([\s\S]{,40}?))([\x01-\x0a]{3,6})\x00\x24\x29\x32\x32\x3d\x37?\x51\x47\x47')
    bmdchiptext_regex = re.compile(r'(?s)\xF9[\x00-\xFF]([\s\S][\x01-\x02])\x00\xF9[\x00-\xFF]([\x00-\x1A])\x03')
    tradechipcheck_regex = re.compile(r'(?s)\xF6\x14([\s\S][\x00-\x03])([\x00-\x1A])\x01[\s\S]{3}')
    tradechipremove_regex = re.compile(r'(?s)\xF6\x11([\s\S][\x00-\x03])([\x00-\x1A])\x01')
    tradechiptext_regex = re.compile(r'(?s)\xF9[\x00-\xFF]([\s\S][\x01-\x02])\x00\xF9[\x00-\xFF]([\x00-\x1A])\x03')
    earliest_script = 0x10000000
    end_addr = -1
    chip_map = generate_chip_permutation(True)
    
    while ptr <= 0x24C:
        pattern_list.append([ptr, base_offset + ptr])
        ptr += 4
    
    for valcheck in range(0,2):
        for block in pattern_list:
            script_ptr = read_word(block[1])
            script_addr = 0x0
            if script_ptr == 0:
                continue
            elif script_ptr - 0x08000000 < 0x00600000:
                script_addr = script_ptr - 0x08000000
                continue
            else:
                script_addr = script_ptr - 0x08000000
            if script_addr < 1:
                continue
            earliest_script = min(earliest_script, script_ptr - 0x08000000)
            script_data = decompress_data(script_addr)
            p += 1
            if len(new_scripts) >= p and p > 0:
                if new_scripts[p-1][0] == block[1]:
                    script_data = new_scripts[p-1][1]
            end_addr = max(end_addr, compressed_data_end)
            new_data = list(map(ord, script_data))
            
            # Replace chip tables
            if valcheck == 0 and ALLOW_BMD == 1:
                for match in chip_regex.finditer(script_data):
                    match_offset = match.start()
                    old_chip = list(map(lambda old_chip : ord(old_chip), list(match.groups()[0])))[0]
                    old_code = list(map(lambda old_code : ord(old_code), list(match.groups()[1])))[0]
                    new_chip = chip_map[old_chip]
                    while new_chip == 279:
                        new_chip = random.choice(available_chips)
                    new_code = random.choice(allcodes[new_chip-1])
                    found = False
                    if [old_chip, old_code] in required_trades:
                        if ALLOW_TRADES == 1:
                            if len(samechiplist) > 0:
                                found = False
                                for i in range(len(samechiplist)):
                                    if old_chip == samechiplist[i][0] and old_code == samechiplist[i][1]:
                                        found = True
                                if found == False:
                                    samechiplist.append([old_chip, old_code, new_chip, new_code])
                            else:
                                samechiplist.append([old_chip, old_code, new_chip, new_code])
                        else:
                            new_chip = old_chip
                            new_code = allcodes[old_chip][chip_data[old_chip]['codes'].index(old_code)]
                    found = False
                    if len(bmdchiplist) > 0:
                        for i in range(len(bmdchiplist)):
                            if old_chip == bmdchiplist[i][0] and old_code == bmdchiplist[i][1]:
                                new_chip = bmdchiplist[i][2]
                                new_code = bmdchiplist[i][3]
                                found = True
                                break
                        
                    #Get Chip Command Offsets
                    new_data[match.start(1)] = new_chip % 256
                    new_data[match.start(1)+1] = int(new_chip / 256)
                    new_data[match.start(2)] = new_code
                    if not found:
                        bmdchiplist.append([old_chip, old_code, new_chip, new_code])
                    changelog_bmd.append(["chip", old_chip, old_code, new_chip, new_code, match_offset])

                # Multiply zenny tables
                for match in zenny_regex.finditer(script_data):
                    #match_found.append(match.start() + script_addr)
                    match_offset = match.start() + 2
                    zennys = list(struct.unpack('<I', bytes(match.groups()[0], encoding="raw_unicode_escape")))
                    text_offset = match.start(10) - match_offset
                    zennys[0] = int(zennys[0] * 3 / 2)
                    if len(str(match.group(10))) < len(str(zennys[0])):
                        zennys[0] = 9 * pow(10, len(str(match.group(10)))-1)
                    zenny_str = struct.pack('<I', *(int(x) for x in zennys))
                    for i in range(len(zenny_str)):
                        new_data[match_offset + i] = zenny_str[i]
                    for i in range(len(str(match.group(10)))):
                        #print i, int(zennys[0] / pow(10,len(str(match.group(3)))-(i+1)) % 10) + 1
                        new_data[match_offset + text_offset + i] = int(zennys[0] / pow(10,len(str(match.group(10)))-(i+1)) % 10) + 1
                    #print "Zenny found at", hex(script_addr), "!"
                    changelog_bmd.append(["zenny", list(struct.unpack('<I', bytes(match.groups()[0], encoding="raw_unicode_escape")))[0], zennys[0]])
                    
                for match in bmdchiptext_regex.finditer(script_data):
                    match_offset = match.start()
                    old_chip = list(map(lambda old_chip : ord(old_chip), list(match.groups()[0])))[0]
                    old_code = list(map(lambda old_code : ord(old_code), list(match.groups()[1])))[0]
                    for i in range(len(bmdchiplist)):
                        if old_chip == bmdchiplist[i][0] and old_code == bmdchiplist[i][1]:
                            new_chip = bmdchiplist[i][2]
                            new_code = bmdchiplist[i][3]
                            new_data[match.start(1)] = new_chip % 256
                            new_data[match.start(1)+1] = int(new_chip / 256) + 1
                            new_data[match.start(2)] = new_code
                            break
            
            if valcheck == 1 and ALLOW_TRADES == 1:
                for match in tradechipcheck_regex.finditer(script_data):
                    match_offset = match.start()
                    old_chip = list(map(lambda old_chip : ord(old_chip), list(match.groups()[0])))[0]
                    old_code = list(map(lambda old_code : ord(old_code), list(match.groups()[1])))[0]
                    new_chip = chip_map[old_chip]
                    while new_chip == 279:
                        new_chip = random.choice(available_chips)
                    new_code = random.choice(allcodes[new_chip-1])
                    if len(tradechiplist) > 0:
                        for i in range(len(tradechiplist)):
                            if old_chip == tradechiplist[i][0] and old_code == tradechiplist[i][1]:
                                new_chip = tradechiplist[i][2]
                                new_code = tradechiplist[i][3]
                                break
                    if ALLOW_BMD == 1 and len(bmdchiplist) > 0:
                        for i in range(len(bmdchiplist)):
                            if old_chip == bmdchiplist[i][0] and old_code == bmdchiplist[i][1]:
                                new_chip = bmdchiplist[i][2]
                                new_code = bmdchiplist[i][3]
                                break
                    new_data[match.start(1)] = new_chip % 256
                    new_data[match.start(1)+1] = int(new_chip / 256)
                    new_data[match.start(2)] = new_code
                    tradechiplist.append([old_chip, old_code, new_chip, new_code])
                    changelog_trades.append(["requirement", old_chip, old_code, new_chip, new_code, match_offset])
                    #print "Check: ", chip_names[list(list(chip_hex.keys()))[list(list(chip_hex.values())).index(new_data[match.start(1)] + new_data[match.start(1)+1] * 256)]-1], " ", chip_codes[new_data[match.start(2)]], " (", str(hex(script_addr)), ")"
                
                for match in tradechipremove_regex.finditer(script_data):
                    match_offset = match.start()
                    old_chip = list(map(lambda old_chip : ord(old_chip), list(match.groups()[0])))[0]
                    old_code = list(map(lambda old_code : ord(old_code), list(match.groups()[1])))[0]
                    for i in range(len(tradechiplist)):
                        if old_chip == tradechiplist[i][0] and old_code == tradechiplist[i][1]:
                            new_chip = tradechiplist[i][2]
                            new_code = tradechiplist[i][3]
                            if ALLOW_BMD == 1 and len(bmdchiplist) > 0:
                                for i in range(len(bmdchiplist)):
                                    if old_chip == bmdchiplist[i][0] and old_code == bmdchiplist[i][1]:
                                        new_chip = bmdchiplist[i][2]
                                        new_code = bmdchiplist[i][3]
                                        break
                            new_data[match.start(1)] = new_chip % 256
                            new_data[match.start(1)+1] = int(new_chip / 256)
                            new_data[match.start(2)] = new_code
                            break
                            
                for match in tradechiptext_regex.finditer(script_data):
                    match_offset = match.start()
                    old_chip = list(map(lambda old_chip : ord(old_chip), list(match.groups()[0])))[0]
                    old_code = list(map(lambda old_code : ord(old_code), list(match.groups()[1])))[0]
                    for i in range(len(tradechiplist)):
                        if old_chip == tradechiplist[i][0] and old_code == tradechiplist[i][1]:
                            new_chip = tradechiplist[i][2]
                            new_code = tradechiplist[i][3]
                            if ALLOW_BMD == 1 and len(bmdchiplist) > 0:
                                for i in range(len(bmdchiplist)):
                                    if old_chip == bmdchiplist[i][0] and old_code == bmdchiplist[i][1]:
                                        new_chip = bmdchiplist[i][2]
                                        new_code = bmdchiplist[i][3]
                                        break
                            new_data[match.start(1)] = new_chip % 256
                            new_data[match.start(1)+1] = int(new_chip / 256) + 1
                            new_data[match.start(2)] = new_code
                            break
                            
            new_script = ''.join(list(map(chr, new_data)))
            if len(new_scripts) >= p:
                new_scripts[p-1] = [block[1], new_script]
            else:
                new_scripts.insert(p-1, [block[1], new_script])
        ptr = 0x0
        p = 0
        earliest_script = 0x10000000
        end_addr = -1
    
    # Write all the scripts back
    for i in new_scripts:
        script_ptr = i[0]
        script_data = compress_data(i[1])
        start_addr = read_word(script_ptr) - 0x08000000
        write_data(script_data, free_space)
        write_data(struct.pack('<I', free_space + 0x08000000), script_ptr)
        free_space += len(script_data)
        free_space += (4 - free_space) % 4
    rom_data = old_data
    if ALLOW_BMD == 1 and not changelog_bmd == None:
        print('randomized bmds')
    if ALLOW_TRADES == 1 and not changelog_trades == None:
        print('randomized trades')

def virus_replace(ind):
    # Safety precaution
    if ind == 0 or ind in banned_viruses:
        return ind
    # Ignore navis by default.
    if ind >= 168:
        # Randomize Navi Battles
        if RANDOM_NAVIS == 1:
            if ind not in [196, 197, 198, 199, 220, 221, 222, 223, 224, 225, 226, 227, 236, 237, 238, 239, 240, 241, 242, 243]:
                # Shuffle Mode
                if OMEGA_MODE < 4:
                    # Easy Navis
                    if ind-168 in [0, 4, 32, 40] and chosen_navis[ind-168] < 0:
                        chosen_navis[ind-168] = random.choice(weak_navis)
                        chosen_navis[ind-168+1] = chosen_navis[ind-168]
                        chosen_navis[ind-168+2] = chosen_navis[ind-168]
                        chosen_navis[ind-168+3] = chosen_navis[ind-168]
                        weak_navis.remove(chosen_navis[ind-168])
                    
                    # Middle Navis
                    if ind-168 in [8, 20, 48, 52, 56] and chosen_navis[ind-168] < 0:
                        chosen_navis[ind-168] = random.choice(mid_navis)
                        chosen_navis[ind-168+1] = chosen_navis[ind-168]
                        chosen_navis[ind-168+2] = chosen_navis[ind-168]
                        chosen_navis[ind-168+3] = chosen_navis[ind-168]
                        mid_navis.remove(chosen_navis[ind-168])
                    
                    # Strong Navis
                    if ind-168 in [12, 16, 24] and chosen_navis[ind-168] < 0:
                        chosen_navis[ind-168] = random.choice(strong_navis)
                        chosen_navis[ind-168+1] = chosen_navis[ind-168]
                        chosen_navis[ind-168+2] = chosen_navis[ind-168]
                        chosen_navis[ind-168+3] = chosen_navis[ind-168]
                        strong_navis.remove(chosen_navis[ind-168])
                    
                    # Post-game Navis
                    if ind-168 in [36, 60, 64] and chosen_navis[ind-168] < 0:
                        chosen_navis[ind-168] = random.choice(post_navis)
                        chosen_navis[ind-168+1] = chosen_navis[ind-168]
                        chosen_navis[ind-168+2] = chosen_navis[ind-168]
                        chosen_navis[ind-168+3] = chosen_navis[ind-168]
                        post_navis.remove(chosen_navis[ind-168])
                    # Punk
                    if ind-168 == 44 and chosen_navis[ind-168] < 0:
                        chosen_navis[ind-168] = 44
                        chosen_navis[ind-168+1] = chosen_navis[ind-168]
                        chosen_navis[ind-168+2] = chosen_navis[ind-168]
                        chosen_navis[ind-168+3] = chosen_navis[ind-168]
                # Chaos Mode
                else:
                    if ind-168 in [0,4,8,12,16,20,24,32,36,40,44,48,52,56,60,64] and chosen_navis[ind-168] < 0:
                        chosen_navis[ind-168] = random.choice(allnavis)
                        chosen_navis[ind-168+1] = chosen_navis[ind-168]
                        chosen_navis[ind-168+2] = chosen_navis[ind-168]
                        chosen_navis[ind-168+3] = chosen_navis[ind-168]
                        allnavis.remove(chosen_navis[ind-168])
                
                new_ind = chosen_navis[ind-168] + 168 + virus_level(ind) - 1
                ind = new_ind
        if OMEGA_MODE % 4 >= 1:
            # Bass, ignore swap-out mechanic
            if ind in [240, 241, 242, 243]:
                return ind
            # Alpha, ignore swap-out mechanic
            elif ind in [196, 197]:
                return ind
            # Serenade, ignore swap-out mechanic
            elif ind in [236,237,238,239]:
                return ind
            else:
                if virus_level(ind) > virus_level(ind + (OMEGA_MODE % 4)):
                    return ind
                else:
                    return ind + (OMEGA_MODE % 4)
        else:
            return ind
    old_hp, old_attack, old_name = virus_data[ind]
    old_hp = int(old_hp)
    if old_hp == -1:
        return ind

    new_ind = -1
    if OMEGA_MODE < 4:
        if ind in weak_viruses:
            new_ind = weak_viruses[random.randint(0,(len(weak_viruses)-1))]
            new_ind = new_ind - virus_level(new_ind) + virus_level(ind)
        if ind in med_viruses:
            new_ind = med_viruses[random.randint(0,(len(med_viruses)-1))]
            new_ind = new_ind - virus_level(new_ind) + virus_level(ind)
        if ind in strong_viruses:
            new_ind = strong_viruses[random.randint(0,(len(strong_viruses)-1))]
            new_ind = new_ind - virus_level(new_ind) + virus_level(ind)
        if ind in powerful_viruses:
            new_ind = powerful_viruses[random.randint(0,(len(powerful_viruses)-1))]
            new_ind = new_ind - virus_level(new_ind) + virus_level(ind)
        if ind in dangerous_viruses:
            new_ind = dangerous_viruses[random.randint(0,(len(dangerous_viruses)-1))]
            new_ind = new_ind - virus_level(new_ind) + virus_level(ind)
    else:
        if ind - virus_level(ind) in allviruses:
            new_ind = allviruses[random.randint(0,(len(allviruses)-1))]
            new_ind = new_ind - virus_level(new_ind) + virus_level(ind)
    if new_ind not in banned_viruses:
        if OMEGA_MODE % 4 > 0:
            if virus_level(new_ind) > virus_level(new_ind + (OMEGA_MODE % 4)):
                return new_ind
            else:
                return new_ind + (OMEGA_MODE % 4)
        else:
            return new_ind
    return new_ind

def randomize_viruses():
    battle_regex = re.compile('(?s)\x00[\x01-\x03][\x01-\x03]\x00(?:.[\x01-\x06][\x01-\x03].)+\xff\x00\x00\x00')
    
    n_battles = 0
    #open('fights.txt','w').write("")
    #newviruslist = []
    #for i in range(0,244):
    #    newviruslist.append(virus_replace(i))
    
    for match in battle_regex.finditer(rom_data):
        # Sanity check
        if match.start() >= 0x22000:
            break
        n_battles += 1
        if n_battles <= 3 and TUTORIAL_SKIP == 1:
            continue
        for i in range(match.start(), match.end(), 4):
            if checkval(rom_data[i + 3]) == 1:
                virus_ind = checkval(rom_data[i])
                new_ind = virus_replace(virus_ind)
                if new_ind == -1:
                    new_ind = virus_ind
                write_data(chr(new_ind), i)         
                if virus_ind >= 168 and virus_ind < 244:
                    #open('fights.txt','a').write(navi_data[ord(rom_data[i])-168][2] + "(" + str(ord(rom_data[i+1])) + "," + str(ord(rom_data[i+2])) + "), ")
                    changelog_battles.append(["navi", n_battles, virus_ind-168, new_ind-168])
                elif virus_ind > 0 and virus_ind < 168:
                    #open('fights.txt','a').write(virus_data[ord(rom_data[i])][2] + "(" + str(ord(rom_data[i+1])) + "," + str(ord(rom_data[i+2])) + "), ")
                    changelog_battles.append(["virus", n_battles, virus_ind, new_ind])
            elif checkval(rom_data[i + 3]) in [2, 3, 4, 5, 6, 7, 11] and RANDOM_OBSTACLES == 1:
                old_obst = checkval(rom_data[i + 3])
                new_obst = random.choice([2,3,4,5,6,7,11])
                write_data(chr(new_obst), i + 3)
                changelog_battles.append(["obstacle", n_battles, old_obst, new_obst])
                #open('fights.txt','a').write(obstacles[ord(rom_data[i + 3])] + "(" + str(ord(rom_data[i+1])) + "," + str(ord(rom_data[i+2])) + "), ")
                
    #open('fights.txt','a').write("\n")
    print('randomized %d battles' % n_battles)
    
    virus_start = 0x19618
    
    # Virus Randomizer
    virus_randnames = open(DATA_PATH +'enemy_randomnames.txt', 'r').read().strip().split('\n')
    virus_namestart = 0x711B00
    if ROMVERSION == "b":
        virus_namestart = 0x7114EC
    for i in range(len(virus_data)):
        if i == 0:
            virus_start += 8
            continue
        virus_hp, virus_damage, virus_name = virus_data[i]
        returned_name = virus_name
        virus_hp = int(virus_hp)
        virus_damage = int(virus_damage) # Unused
        virus_hp = int(float(virus_hp) * float(1 + (float(float(random.randint(-100,100)/100)) * VH_VARIANCE)) * V_MULTIPLIER)
        virus_hp -= virus_hp % 5
        # Randomize Name
        if VN_NAMERANDOMIZER == 1 and len(virus_name) >= 3:
            virus_namestart, returned_name = randomize_name(virus_namestart, virus_name, virus_randnames)
        # Check if HP is less than or equal to zero.
        if virus_hp <= 0:
            virus_start += 8
            continue
        # Make a Hard Cap so that things don't get out of hand.
        if virus_hp < 10:
            virus_hp = 10
        if IGNORE_LIMITS == 1:
            if ELEMENT_MODE == 1 or ELEMENT_MODE == 3:
                write_data(chr(random.randint(1,4)), 0x680020+i)
            write_data(chr(virus_hp % 256)+chr(virus_hp // (2**8) % 256), virus_start)
        else:
            if virus_hp > 4000:
                virus_hp = 4000
            if ELEMENT_MODE == 1 or ELEMENT_MODE == 3:
                write_data(chr(virus_hp % 256)+chr((0x10 * random.randint(1,4)) + virus_hp // (2**8) % 256 % 0x10), virus_start)
            else:
                # Some bitflag in the enemy's HP value. It's their Element.
                if i-1 in [0x24, 0x25, 0x26, 0x27, 0x46, 0x56, 0x57, 0x58, 0x59, 0x72, 0x73, 0x74, 0x75, 0x8a, 0x8b, 0x8c, 0x8d]:
                    write_data(chr(virus_hp % 256)+chr(0x10 + virus_hp // (2**8) % 256 % 0x10), virus_start)
                elif i-1 in [0x09, 0x0b, 0x0d, 0x16, 0x19, 0x20, 0x21, 0x22, 0x23, 0x44, 0x4e, 0x4f, 0x50, 0x51, 0x5e, 0x5f, 0x60, 0x61, 0x8e, 0x8f, 0x90, 0x91, 0x92, 0x93, 0x94, 0x95]:
                    write_data(chr(virus_hp % 256)+chr(0x20 + virus_hp // (2**8) % 256 % 0x10), virus_start)
                elif i-1 in [0x0e, 0x15, 0x18, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f, 0x45, 0x66, 0x67, 0x68, 0x69, 0x6e, 0x6f, 0x70, 0x71]:
                    write_data(chr(virus_hp % 256)+chr(0x30 + virus_hp // (2**8) % 256 % 0x10), virus_start)
                elif i-1 in [0x1a, 0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x47, 0x6a, 0x6b, 0x6c, 0x6d]:
                    write_data(chr(virus_hp % 256)+chr(0x40 + virus_hp // (2**8) % 256 % 0x10), virus_start)
                # Everything else
                else:
                    write_data(chr(virus_hp % 256)+chr(virus_hp // (2**8) % 256), virus_start)
        #print 'Virus HP: ', virus_hp
        changelog_virus.append([virus_name, returned_name, virus_hp])
        virus_start += 8
    
    # Navi Randomizer
    for i in range(len(navi_data)):
        navi_offset, virus_hp, virus_name = navi_data[i]
        returned_name = virus_name
        virus_hp = int(virus_hp)
        virus_hp = int(float(virus_hp) * float(1 + (float(float(random.randint(-100,100)/100)) * VH_VARIANCE)) * V_MULTIPLIER)
        virus_hp -= virus_hp % 5
        if virus_hp < 10:
            virus_hp = 10
        if VN_NAMERANDOMIZER == 1 and len(virus_name) >= 3:
            virus_namestart, returned_name = randomize_name(virus_namestart, virus_name, virus_randnames)
        # Make a Hard Cap so that things don't get out of hand.
        if IGNORE_LIMITS == 1:
            # ... Unless you want it to, then go ahead, be my guest ;)
            if ELEMENT_MODE == 1 or ELEMENT_MODE == 3:
                write_data(chr(random.randint(1,4)), 0x680020+int((navi_offset - 0x19618) / 8))
            write_data(chr(virus_hp % 256)+chr(virus_hp // (2**8) % 256), navi_offset)
        else:
            if virus_hp > 4000:
                virus_hp = 4000
            if ELEMENT_MODE == 1 or ELEMENT_MODE == 3:
                write_data(chr(virus_hp % 256)+chr((0x10 * random.randint(1,4)) + virus_hp // (2**8) % 256 % 0x10), navi_offset)
            else:
                #Some bitflag in the navi's HP value. It's their Element.
                if navi_offset in [0x19b58, 0x19b60, 0x19b68, 0x19b70]:
                    write_data(chr(virus_hp % 256)+chr(0x10 + virus_hp // (2**8) % 256 % 0x10), navi_offset)
                elif navi_offset in [0x19bf8, 0x19c00, 0x19c08, 0x19c10]:
                    write_data(chr(virus_hp % 256)+chr(0x20 + virus_hp // (2**8) % 256 % 0x10), navi_offset)
                elif navi_offset in [0x19b98, 0x19ba0, 0x19ba8, 0x19bb0]:
                    write_data(chr(virus_hp % 256)+chr(0x30 + virus_hp // (2**8) % 256 % 0x10), navi_offset)
                elif navi_offset in [0x19bd8, 0x19be0, 0x19be8, 0x19bf0]:
                    write_data(chr(virus_hp % 256)+chr(0x40 + virus_hp // (2**8) % 256 % 0x10), navi_offset)
                else:
                    write_data(chr(virus_hp % 256)+chr(virus_hp // (2**8) % 256), navi_offset)
        #print 'Navi HP: ', virus_hp
        changelog_virus.append([virus_name, returned_name, virus_hp])
    
    print('randomized virus and navi HP')

def generate_chip_permutation(allow_conditional_attacks = False):
    all_chips = defaultdict(list)
    for chip_ind in range(1, N_CHIPS + 1):
        chip = chip_data[chip_ind]
        chip_id = chip['rank']
        # Treat standard attacking chips differently from standard nonattacking chips
        if chip['is_attack'] and (allow_conditional_attacks or not chip['is_conditional']) and chip['rank'] < 10:
            chip_id += 1000
        all_chips[chip_id].append(chip_ind)
    # Do the shuffling
    chip_map = {}
    for (key, chips) in list(all_chips.items()):
        keys = copy.copy(chips)
        random.shuffle(chips)
        for old_chip, new_chip in zip(keys, chips):
            chip_map[old_chip] = new_chip
    return chip_map

def get_new_code(old_chip, old_code, new_chip):
    if old_code == 26 and old_code in chip_data[new_chip]['codes']:
        return old_code
    try:
        old_code_ind = chip_data[old_chip]['codes'].index(old_code)
        new_codes = chip_data[new_chip]['codes']
        if C_ALLSTARMODE >= 1:
            new_codes = allcodes[new_chip-1]
        new_code_ind = old_code_ind % len(new_codes)
        return new_codes[new_code_ind]
    except ValueError:
        return old_code

def randomize_folders():
    s = 0xcbdc
    
    n_folders = 0
    permutations = []
    f = 0
    first = 0
    singlerandomfolder = []
    
    while True:
        if n_folders == 14:
            break
        folder_start = s
        
        if FOLDER_MODE > 0 and FOLDER_MODE < 3:
            if n_folders < 12:
                f = random.randint(0, len(folder_data)-1)
            if n_folders == 0:
                first = f
        
        # There are 14 folders, the last 3 are tutorial only
        n_folders += 1
        is_tutorial = (n_folders >= 12 and n_folders <= 14)
        if is_tutorial or ((FOLDER_MODE == 1 or FOLDER_MODE == 3) and n_folders > 1):
            chip_map = permutations[0]
        else:
            chip_map = generate_chip_permutation()
        permutations.append(chip_map)
        for i in range(30):
            old_chip, old_code = struct.unpack('<HH', bytes(rom_data[s:s+4], encoding="raw_unicode_escape"))
            new_chip = chip_map[old_chip]
            new_code = get_new_code(old_chip, old_code, new_chip)
                        
            # Folder Mode Setup
            if FOLDER_MODE > 0 and FOLDER_MODE < 3:
                c, o = folder_data[f][i].split(' ')
                new_chip = int(c, 10)
                new_code = get_new_code(new_chip, int(o, 10), new_chip)
                if n_folders == 1:
                    singlerandomfolder.append([new_chip, new_code])
                if (FOLDER_MODE == 1 and n_folders > 1) or (FOLDER_MODE == 2 and is_tutorial):
                    new_chip = singlerandomfolder[i][0]
                    new_code = singlerandomfolder[i][1]
                if is_tutorial:
                    new_code = 26
            
            # Need to determine code
            else:
                if is_tutorial:
                    # tutorial folder, dont change the code
                    new_code = 26
                else:
                    if C_ALLSTARMODE == 1:
                        new_code = 26
                    if C_ALLSTARMODE == 2 and allcodes[new_chip-1][0] == 26:
                        new_code = 26
            
            chipstr = struct.pack('<HH', new_chip, new_code)
            changelog_folders.append([n_folders, i, old_chip, old_code, new_chip, new_code])
            write_data(chipstr, s)
            s += 4
        
        # Pick a new Folder for Multi Folder Lock
        if FOLDER_MODE > 0:
            f = random.randint(0, len(folder_data)-1)
            if n_folders >= 11 and n_folders <= 13:
                f = first
    print('randomized %d folders' % n_folders)

def randomize_virus_drops():
    offset = 0x160a8
    chip_map = generate_chip_permutation(allow_conditional_attacks = True)
    for virus_ind in range(244):
        zenny_queue = []
        last_chip = None
        for i in range(28):
            if i % 14 == 0:
                last_chip = None
            reward = struct.unpack('<H', bytes(rom_data[offset:offset+2], encoding="raw_unicode_escape"))[0]
            # 0 = chip, 1 = zenny, 2 = health, 3 = should not happen (terminator)
            reward_type = reward >> 14;
            # Number from 0-6
            buster_rank = (i % 14) / 2
            if reward_type == 0:
                # Read the chip data
                old_code = (reward >> 9) & 0x1f;
                old_chip = reward & 0x1ff;
                last_chip = (old_chip, old_code)

                # Randomize the chip
                new_chip = chip_map[old_chip]
                new_code = get_new_code(old_chip, old_code, new_chip)
                new_reward = new_chip + (new_code << 9)
                changelog_drops.append([virus_ind, old_chip, old_code, new_chip, new_code])
                write_data(struct.pack('<H', new_reward), offset)

                # Discharge the queue
                for old_offset in zenny_queue:
                    new_chip = chip_map[old_chip]
                    new_code = get_new_code(old_chip, old_code, new_chip)
                    new_reward = new_chip + (new_code << 9)
                    changelog_drops.append([virus_ind, old_chip, old_code, new_chip, new_code])
                    write_data(struct.pack('<H', new_reward), old_offset)
                zenny_queue = []

            elif reward_type == 1:
                # Only turn lvl 5+ drops to chips
                if buster_rank >= 2:
                    if last_chip is None:
                        # No chip yet, queue it for later
                        zenny_queue.append( (offset) )
                    else:
                        old_chip, old_code = last_chip
                        new_chip = chip_map[old_chip]
                        new_code = get_new_code(old_chip, old_code, new_chip)
                        new_reward = new_chip + (new_code << 9)
                        changelog_drops.append([virus_ind, old_chip, old_code, new_chip, new_code])
                        write_data(struct.pack('<H', new_reward), offset)

            offset += 2
    print('randomized virus drops')

def randomize_shops():
    shop_regex = re.compile('(?s)[\x00-\x01]\x00\x00\x00...\x08...\x02.\x00\x00\x00')
    last_ind = 0
    n_shops = 0
    gigachips = [226,231,236,241,246,251,256,261,266,271,281,286,291,296,301]
    # Offsets
    item_data_offset = 0x44bc8
    if ROMVERSION == "b":
        item_data_offset = 0x44bb0
    
    chip_order_offset = 0x45148
    if ROMVERSION == "b":
        chip_order_offset = 0x45130
    
    global tradechiplist
    chip_map = generate_chip_permutation()
    
    # Chip Order Randomization
    if ALLOW_SHOPS == 1:
        while True:
            item_type, stock, chip, code, filler, price = struct.unpack('<BBHBBH', bytes(rom_data[chip_order_offset: chip_order_offset + 8], encoding="raw_unicode_escape"))
            if item_type == 0:
                break
            code = random.choice(allcodes[chip-1])
            if stock == 0:
                stock = 1
            price = int(float(chip_prices[chip-1]) * float(1 + (float(float(random.randint(-100,100)/100)) * CPRICE_VARIANCE)))
            if FREE_SHOPS == 1:
                price = 0
            new_item = struct.pack('<BBHBBH', item_type, stock, chip, code, filler, price)
            write_data(new_item, chip_order_offset)
            chip_order_offset += 8
            changelog_shops.append([n_shops, chip, code, price*100])
    
    first_shop = None
    for match in shop_regex.finditer(rom_data):
        shop_offset = match.start()
        n_shops += 1
        currency, filler, first_item, n_items = struct.unpack('<IIII', bytes(rom_data[shop_offset: shop_offset + 16], encoding="raw_unicode_escape"))
        if first_shop is None:
            first_shop = first_item
        # Convert RAM address to ROM address
        item_offset = first_item - first_shop + item_data_offset
        if ALLOW_SHOPS == 1 and (FILL_SHOPS == 1 or n_shops == 1):
            n_items = 8
        available_chips = []
        for i in range(1,301):
            if i == 279:
                continue
            available_chips.append(i)
        while True:
            #t = read_dblword(item_offset)
            if n_items <= 0:
                break
            item_type, stock, old_chip, old_code, filler, price = struct.unpack('<BBHBBH', bytes(rom_data[item_offset: item_offset + 8], encoding="raw_unicode_escape"))
            new_chip = -1
            new_code = 255
            # Only care about chips
            if item_type == 2 or item_type == 0:
                # Other Chips
                if (old_chip == 0 or item_type == 0):
                    if FILL_SHOPS == 1 or n_shops == 1:
                        item_type = 2
                        old_chip = random.choice(available_chips)
                    else:
                        item_offset += 8
                        n_items -= 1
                        continue
                new_chip = chip_map[old_chip]
                while new_chip == 279:
                    new_chip = random.choice(available_chips)
                new_code = random.choice(allcodes[new_chip-1])
                stock = 3
                price = int(float(chip_prices[new_chip-1]) * float(1 + (float(float(random.randint(-100,100)/100)) * CPRICE_VARIANCE)))
                if new_chip > 200:
                    stock = 1
                # Force Chips in ACDC 1 Shop to be Story Progression Chips
                if item_offset == item_data_offset + 0x10:
                    new_chip = 0x8f
                    new_code = allcodes[new_chip][chip_data[new_chip]['codes'].index(26)]
                    if ALLOW_TRADES == 1 and [new_chip, 26] in required_trades:
                        for i in range(len(tradechiplist)):
                            if new_chip == tradechiplist[i][0] and 26 == tradechiplist[i][1]:
                                new_chip = tradechiplist[i][2]
                                new_code = tradechiplist[i][3]
                                break
                    #new_code = 26
                    stock = 2
                    price = 1
                if item_offset == item_data_offset + 0x18:
                    new_chip = 0x45
                    new_code = allcodes[new_chip][chip_data[new_chip]['codes'].index(6)]
                    if ALLOW_TRADES == 1 and [new_chip, 6] in required_trades:
                        for i in range(len(tradechiplist)):
                            if new_chip == tradechiplist[i][0] and 6 == tradechiplist[i][1]:
                                new_chip = tradechiplist[i][2]
                                new_code = tradechiplist[i][3]
                                break
                    #new_code = 6
                    stock = 2
                    price = 1
                if item_offset == item_data_offset + 0x20:
                    new_chip = 0x19
                    new_code = allcodes[new_chip][chip_data[new_chip]['codes'].index(12)]
                    if ALLOW_TRADES == 1 and [new_chip, 12] in required_trades:
                        for i in range(len(tradechiplist)):
                            if new_chip == tradechiplist[i][0] and 12 == tradechiplist[i][1]:
                                new_chip = tradechiplist[i][2]
                                new_code = tradechiplist[i][3]
                                break
                    #new_code = 12
                    stock = 2
                    price = 1
                # Fix Giga Chip in Secret Area Shop to be version-agnostic
                if item_offset == item_data_offset + 0x2a8:
                    if ROMVERSION == "w":
                        new_chip = random.choice(gigachips)
                    if ROMVERSION == "b":
                        new_chip = random.choice(gigachips)
                    stock = 1
                    new_code = random.choice(allcodes[new_chip-1])
                # Free Shops check
                if FREE_SHOPS == 1:
                    price = 0
                new_item = struct.pack('<BBHBBH', item_type, stock, new_chip, new_code, filler, price)
                write_data(new_item, item_offset)
                changelog_shops.append([n_shops, new_chip, new_code, price*100])
            item_offset += 8
            n_items -= 1
        # Immediately break the loop if we're past the first shop and we don't want to randomize them
        if ALLOW_SHOPS == 0 and n_shops >= 1:
            break

    print('randomized %d shop(s)' % n_shops)

def randomize_number_trader():
    # 3e 45 cc 86 90 18 4f 09 61 e9
    reward_offset = 0x47910
    if ROMVERSION == "b":
        reward_offset = 0x478f8
    n_rewards = 0
    chip_map = generate_chip_permutation()
    while True:
        reward_type, old_code, old_chip, encrypted_number = struct.unpack('<BBH8s', bytes(rom_data[reward_offset : reward_offset + 12], encoding="raw_unicode_escape"))
        if reward_type == 0xff:
            break
        if reward_type == 0:
            new_chip = chip_map[old_chip]
            new_code = get_new_code(old_chip, old_code, new_chip)
            new_reward = struct.pack('<BBH8s', reward_type, new_code, new_chip, encrypted_number)
            write_data(new_reward, reward_offset)
            
            changelog_numbertrader.append([new_chip, new_code])
        reward_offset += 12
        n_rewards += 1
    print('randomized %d number trader rewards' % n_rewards)

def randomize_navicust():
    # White: 0x3A109
    #  Blue: 0x3A0F1
    
    banned_programs = ["Press", "EnergyChange", "AlphaScope", "BlackMind", "UnderShirt", "Attack+1", "Speed+1", "Charge+1"]
    ncp_programs = ["SuperArmor", "BreakBuster", "BreakCharge", "SetGreen", "SetIce", "SetLava", "SetSand", "SetMetal", "SetHoly", "Custom1", "Custom2", "MegaFolder1", "MegaFolder2", "Block", "Shield", "Reflect", "ShadowShoes", "FloatShoes", "AntiDamage", "Press", "EnergyChange", "AlphaScope", "SneakRun", "OilBody", "Fish", "Battery", "Jungle", "Collect", "AirShoes", "UnderShirt", "FastGauge", "Rush", "Beat", "Tango", "WeaponLevel+1", "HP+100", "HP+200", "HP+300", "HP+500", "Reg+5", "Attack+1", "Speed+1", "Charge+1", "BugStopper", "Humor", "BlackMind", "BusterMax", "GigaFolder1", "HubBatch", "DarkLicense"];
    
    ncp_data = open(DATA_PATH +"ncp_patterns.txt", "r").read().strip()
    ncp_data = ncp_data.split("\n")
    
    ncp_offset = 0x39468
    if ROMVERSION == "b":
        ncp_offset = 0x39450
    ncp_total = 0
    basencpoffset = ncp_offset
    while True:
        uncompressed = struct.unpack('<I', bytes(rom_data[ncp_offset: ncp_offset + 4], encoding="raw_unicode_escape"))[0] - 0x08000000
        compressed = struct.unpack('<I', bytes(rom_data[ncp_offset + 4: ncp_offset + 8], encoding="raw_unicode_escape"))[0] - 0x08000000
        if ncp_offset >= basencpoffset + 0xC80:
            break
        if ncp_programs[int((ncp_offset - basencpoffset) / 64)] not in banned_programs:
            #print "Old Patterns: ", pattern
            new_pattern = ncp_data[random.randint(0, len(ncp_data)-1)]
            i = 0
            write_pattern = []
            while i < 50:
                if new_pattern.find("0") == 0:
                    write_pattern.append(0)
                    new_pattern = new_pattern.replace("0", "", 1)
                if new_pattern.find("1") == 0:
                    write_pattern.append(1)
                    new_pattern = new_pattern.replace("1", "", 1)
                i += 1
            new_pattern = struct.pack('<BBBBBBBBBBBBBBBBBBBBBBBBB',write_pattern[0], write_pattern[1], write_pattern[2], write_pattern[3], write_pattern[4], write_pattern[5], write_pattern[6], write_pattern[7], write_pattern[8], write_pattern[9], write_pattern[10], write_pattern[11], write_pattern[12], write_pattern[13], write_pattern[14], write_pattern[15], write_pattern[16], write_pattern[17], write_pattern[18], write_pattern[19], write_pattern[20], write_pattern[21], write_pattern[22], write_pattern[23], write_pattern[24])
            write_data(new_pattern, uncompressed)
            new_pattern = struct.pack('<BBBBBBBBBBBBBBBBBBBBBBBBB',write_pattern[25], write_pattern[26], write_pattern[27], write_pattern[28], write_pattern[29], write_pattern[30], write_pattern[31], write_pattern[32], write_pattern[33], write_pattern[34], write_pattern[35], write_pattern[36], write_pattern[37], write_pattern[38], write_pattern[39], write_pattern[40], write_pattern[41], write_pattern[42], write_pattern[43], write_pattern[44], write_pattern[45], write_pattern[46], write_pattern[47], write_pattern[48], write_pattern[49])
            write_data(new_pattern, compressed)
            ncp_total += 1
            
            # Append to Changelog
            n1 = ""
            n2 = ""
            for i in range(len(write_pattern)):
                if i < 25:
                    n1 = n1 + str(write_pattern[i])
                else:
                    n2 = n2 + str(write_pattern[i])
            changelog_ncp.append([ncp_programs[int((ncp_offset - basencpoffset) / 64)], n1, n2])
        ncp_offset += 64
    print('randomized %d NaviCust Program Shapes' % ncp_total)

def randomize_name(nameoffset, name, randnames):
    foundfit = 0
    k = 0
    returnname = ""
    while foundfit == 0:
        nn = random.randint(0, len(randnames)-1)
        newname = ""
        nl = ""
        k = 1
        c = 0
        while k <= len(randnames[nn]):
            char = ""
            while nl == "" and k <= len(randnames[nn]):
                char = char + randnames[nn][k-1]
                if len(mmbn3_text_parse(char)) == 1:
                    nl = mmbn3_text_parse(char)
                    k = k + 1
                    break
                else:
                    k = k + 1
            if not nl == "":
                newname = newname + nl
                nl = ""
                c = len(newname)
            if k >= len(randnames[nn]):
                if len(newname) == len(name):
                    c = 0
                    k = 1
                    foundfit = 1
                    l = 0
                    while l < len(newname):
                        write_data(newname[l], nameoffset)
                        nameoffset = nameoffset + 1
                        l = l + 1
                    newname = ""
                    nameoffset = nameoffset + 1
                    returnname = randnames[nn]
                    break
                else:
                    c = 0
                    k = 1
                    newname = ""
                    break
    return nameoffset, returnname

def randomize_battlefields():
    # Same Offset for both games
    base_offset = 0xBFDC
    stage_data = open(DATA_PATH +"stages.txt","r").read().strip()
    stage_data = list(map(lambda s: list(map(lambda x : int(x), s.split(' '))), stage_data.split('\n')))
    for i in range(0, 127):
        new_field = stage_data[random.randint(0, len(stage_data)-1)]
        old_field = []
        for j in range(0, 23):
            old_field.append(read_byte(base_offset + (i * 24) + j))
            if j in [0, 7, 8, 15, 16, 23]:
                continue
            write_data(chr(new_field[j]), base_offset + (i * 24) + j)
        changelog_fields.append(["data", i+1, str(old_field), str(new_field)])
    print("randomized stage data")
    # Heavily Randomize Stages
    if BF_PANELRANDOMIZER == 2:
        # Fixed Stages 1
        battle_offset = 0x129F80
        if ROMVERSION == "b":
            battle_offset = 0x12A080
        for i in range(0, 15):
            character = random.randint(0, 127)
            write_data(chr(character), battle_offset + (i * 16) + 0xE)
            changelog_fields.append(["id", str(battle_offset + (i * 16) + 0xE), str(character)])
        # Fixed Stages 2
        battle_offset = 0x12BB98
        if ROMVERSION == "b":
            battle_offset = 0x12BC98
        for i in range(0, 86):
            character = random.randint(0, 127)
            write_data(chr(character), battle_offset + (i * 16) + 0xE)
            changelog_fields.append(["id", str(battle_offset + (i * 16) + 0xE), str(character)])
        # Fixed Stages 3
        battle_offset = 0x12DA0C
        if ROMVERSION == "b":
            battle_offset = 0x12DB0C
        for i in range(0, 0xA1):
            character = random.randint(0, 127)
            write_data(chr(character), battle_offset + (i * 16) + 0xC)
            changelog_fields.append(["id", str(battle_offset + (i * 16) + 0xC), str(character)])
        # Fixed Stages 4
        battle_offset = 0x12E530
        if ROMVERSION == "b":
            battle_offset = 0x12E630
        for i in range(0, 0xA1):
            character = random.randint(0, 127)
            write_data(chr(character), battle_offset + (i * 16) + 0xC)
            changelog_fields.append(["id", str(battle_offset + (i * 16) + 0xC), str(character)])
        # Random Encounter Stages Search
        stage_regex = re.compile(r'(?s)(?:[\x00-\x7f][\x20|\x50]....[\x01-\x02]\x08)+\xff\x00\x00\x00')
        for match in stage_regex.finditer(rom_data):
            stage_offset = match.start()
            if stage_offset <= 0x19D00:
                continue
            if stage_offset >= 0x21300:
                break
            for i in range(0, len(match.group(0))-5, 8):
                if stage_offset + i >= 0x21300:
                    break
                character = random.randint(0, 127)
                write_data(chr(character), stage_offset + i)
                changelog_fields.append(["id", str(stage_offset + i), str(character)])
        print("randomized stage ids")

def randomizerom(rom_path, output_path, versionValue = "w", versionSeed = "", fChipMult = 1.0, fChipVar = 0.0, fVirusMult = 1.0, fVirusVar = 0.0, iChipCode = 0, bChipNames = 0, bVirusNames = 0, bRandomBosses = 0, iRandomElements = 0, iRegularMemory = 0, bNCP = 0, iOmegaMode = 0, iHellMode = 0, iBattlefields = 0, iFolderMode = 0, bLog = 0, bRandomObjects = 0, bFillShops = 1, bFreeShops = 0, allowFolder = 1, allowGMD = 1, allowBMD = 1, allowShop = 1, allowChip = 1, allowVirus = 1, allowTrade = 1, allowDaily = 0, allowEasyTutorial = 1, ignoreLimits = 0, fPriceVariance = 0.0):
    global weak_navis
    weak_navis = [0,4,32,40]
    global mid_navis
    mid_navis = [8,20,48]
    global strong_navis
    strong_navis = [12,16,24]
    global post_navis
    post_navis = [36,60,64]
    global allnavis
    allnavis = [0,4,8,12,16,20,24,32,36,40,44,48,52,56,60,64]
    chosen_navis = list()
    for i in range(0, 76):
        chosen_navis.append(-1)
    
    global weak_viruses
    weak_viruses = [1,2,3,4, 5,6,7,8, 9,10,11,12, 13,14,15,16, 29,30,31,32, 33,34,35,36, 37,38,39,40, 75,76,77,78, 123,124,125,126, 131,132,133,134]
    global med_viruses
    med_viruses = [17,18,19,20, 21,22,23,24, 41,42,43,44, 79,80,81,82, 91,92,93,94, 103,104,105,106, 111,112,113,114, 139,140,141,142, 147,148,149,150, 155,156,157,158]
    global strong_viruses
    strong_viruses = [45,46,47,48, 49,50,51,52, 83,84,85,86, 99,100,101,102, 119,120,121,122, 143,144,145,146]
    global powerful_viruses
    powerful_viruses = [25,26,27,28, 57,58,59,60, 65,66,67,68, 87,88,89,90, 107,108,109,110]
    global dangerous_viruses
    dangerous_viruses = [53,54,55,56, 95,96,97,98, 115,116,117,118, 127,128,129,130, 135,136,137,138]
    global banned_viruses
    banned_viruses = [61,62,63,64, 69,70,71,72,73,74, 151,152,153,154, 159,160,161, 162,163,164, 165,166,167]
    global allviruses
    allviruses = [1,2,3,4, 5,6,7,8, 9,10,11,12, 13,14,15,16, 29,30,31,32, 33,34,35,36, 37,38,39,40, 75,76,77,78, 123,124,125,126, 131,132,133,134, 17,18,19,20, 21,22,23,24, 41,42,43,44, 79,80,81,82, 91,92,93,94, 103,104,105,106, 111,112,113,114, 139,140,141,142, 147,148,149,150, 155,156,157,158, 45,46,47,48, 49,50,51,52, 83,84,85,86, 99,100,101,102, 119,120,121,122, 143,144,145,146, 25,26,27,28, 57,58,59,60, 65,66,67,68, 87,88,89,90, 107,108,109,110, 53,54,55,56, 95,96,97,98, 115,116,117,118, 127,128,129,130, 135,136,137,138]
    #allviruses = [1,5,9,13,29,33,37,75,123,131,17,21,41,79,91,103,111,139,147,155,45,49,83,99,119,143,25,57,65,87,107,53,95,115,127,135]
    
    global P_MULTIPLIER
    global P_VARIANCE
    global V_MULTIPLIER
    global VH_VARIANCE
    global C_ALLSTARMODE
    global CP_NAMERANDOMIZER
    global VN_NAMERANDOMIZER
    global ROMVERSION
    global NC_SHAPERANDOMIZER
    global BF_PANELRANDOMIZER
    global RANDOM_NAVIS
    global OMEGA_MODE
    global ELEMENT_MODE
    global REGMEM_MODE
    global FOLDER_MODE
    global ALLOW_FOLDERS
    global ALLOW_GMD
    global ALLOW_BMD
    global ALLOW_SHOPS
    global ALLOW_CHIPS
    global ALLOW_VIRUSES
    global ALLOW_TRADES
    global ALLOW_DAILY
    global TUTORIAL_SKIP
    global RANDOM_OBSTACLES
    global FILL_SHOPS
    global FREE_SHOPS
    global OUTPUTLOG
    global IGNORE_LIMITS
    global CPRICE_VARIANCE
    
    # Changelog variables
    global changelog_bmd
    global changelog_gmd
    global changelog_battles
    global changelog_virus
    global changelog_chip
    global changelog_ncp
    global changelog_shops
    global changelog_drops
    global changelog_numbertrader
    global changelog_folders
    global changelog_fields
    global changelog_trades
    global changelog_pas
    
    # Data variables
    global rom_data
    global randomized_data
    
    changelog_bmd = []
    changelog_gmd = []
    changelog_virus = []
    changelog_chip = []
    changelog_ncp = []
    changelog_shops = []
    changelog_drops = []
    changelog_numbertrader = []
    changelog_folders = []
    changelog_battles = []
    changelog_fields = []
    changelog_trades = []
    changelog_pas = []
    
    ROMVERSION = versionValue;
    P_MULTIPLIER = fChipMult
    P_VARIANCE = fChipVar
    V_MULTIPLIER = fVirusMult
    VH_VARIANCE = fVirusVar
    C_ALLSTARMODE = iChipCode
    CP_NAMERANDOMIZER = bChipNames
    VN_NAMERANDOMIZER = bVirusNames
    NC_SHAPERANDOMIZER = bNCP
    BF_PANELRANDOMIZER = iBattlefields
    ELEMENT_MODE = iRandomElements
    OMEGA_MODE = iOmegaMode
    HELL_MODE = iHellMode
    REGMEM_MODE = iRegularMemory
    RANDOM_NAVIS = bRandomBosses
    RANDOM_OBSTACLES = bRandomObjects
    SEED = versionSeed
    FOLDER_MODE = iFolderMode
    ALLOW_FOLDERS = allowFolder
    ALLOW_GMD = allowGMD
    ALLOW_BMD = allowBMD
    ALLOW_SHOPS = allowShop
    ALLOW_CHIPS = allowChip
    ALLOW_VIRUSES = allowVirus
    ALLOW_TRADES = allowTrade
    ALLOW_DAILY = allowDaily
    TUTORIAL_SKIP = allowEasyTutorial
    FILL_SHOPS = bFillShops
    FREE_SHOPS = bFreeShops
    OUTPUTLOG = bLog
    IGNORE_LIMITS = ignoreLimits
    CPRICE_VARIANCE = fPriceVariance
    
    # Seed Info
    if len(SEED) < 1 and ALLOW_DAILY == 0:
        import datetime
        SEED = datetime.datetime.now().ctime()
    # Daily Seed
    elif ALLOW_DAILY == 1:
        import datetime
        SEED = datetime.datetime.today().replace(microsecond=0,second=0,minute=0,hour=0).ctime()
        ALLOW_TRADES = 1
        ALLOW_GMD = 1
        ALLOW_BMD = 1
        ALLOW_SHOPS = 1
        ALLOW_CHIPS = 1
        ALLOW_VIRUSES = 1
        ALLOW_FOLDERS = 1
        TUTORIAL_SKIP = 1
        FILL_SHOPS = 1
        FREE_SHOPS = 0
        random.seed(SEED)
        P_MULTIPLIER = float(random.randint(15,30)*5)/100
        P_VARIANCE = float(random.randint(0,15)*5)/100
        CPRICE_VARIANCE = float(random.randint(0,10)*5)/100
        V_MULTIPLIER = float(random.randint(15,30)*5)/100
        VH_VARIANCE = float(random.randint(0,15)*5)/100
        C_ALLSTARMODE = random.randint(0,3)
        NC_SHAPERANDOMIZER = random.choice([0,0,0,0,0,1])
        BF_PANELRANDOMIZER = random.choice([0,0,0,0,0,0,1,2])
        ELEMENT_MODE = random.choice([0,0,0,0,1,1,2,2,3])
        REGMEM_MODE = random.choice([0,0,0,random.randint(1,20),random.randint(1,20),random.randint(1,35),random.randint(1,55)])
        HELL_MODE = 0
        OMEGA_MODE = random.choice([0,0,0,0,0,1,4])
        RANDOM_NAVIS = random.choice([0,0,0,1])
        RANDOM_OBSTACLES = random.choice([0,0,0,0,0,0,1])
        FOLDER_MODE = random.choice([0,0,0,0,1,1,2,3,3,4])
        IGNORE_LIMITS = 0
    random.seed(SEED)
    
    if len(ROMVERSION) != 1:
        return
    ROMVERSION = ROMVERSION.lower()
    if ROMVERSION != "b" and ROMVERSION != "w":
        return
    if P_MULTIPLIER < 0.25:
        P_MULTIPLIER = 0.25
    if P_MULTIPLIER > 3 and IGNORE_LIMITS == 0:
        P_MULTIPLIER = 3
    if P_VARIANCE < 0:
        P_VARIANCE = 0
    if P_VARIANCE > 0.9:
        P_VARIANCE = 0.9
    if V_MULTIPLIER < 0.25:
        V_MULTIPLIER = 0.25
    if V_MULTIPLIER > 3 and IGNORE_LIMITS == 0:
        V_MULTIPLIER = 3
    if VH_VARIANCE < 0:
        VH_VARIANCE = 0
    if VH_VARIANCE > 0.9:
        VH_VARIANCE = 0.9
    if CPRICE_VARIANCE < 0:
        CPRICE_VARIANCE = 0
    if CPRICE_VARIANCE > 0.9:
        CPRICE_VARIANCE = 0.9
    
    x = init_rom_data(rom_path)
    rom_data = x[0]
    randomized_data = x[1]
    
    init_custom_folders()
    init_chip_data()
    init_pa_data()
    if ALLOW_CHIPS == 1 and C_ALLSTARMODE > 1:
        fix_pas()
    # Ignore Limits code
    if IGNORE_LIMITS == 1:
        # Relink Enemy Table Read
        write_data(struct.pack("<BBBBBBBBBBBB",0x84,0x46,0x13,0xF0,0x8A,0xFD,0x0A,0x1C,0xE0,0xF2,0x23,0xFF), 0x5AEE)
        
        # Ignore Element Byte in HP so it can be used AS HP
        write_data(struct.pack("<BBBB",0x00,0x23,0x00,0x23), 0x5AFE)
        write_data(struct.pack("<BBBB",0x00,0x23,0x00,0x23), 0x147BC)
        
        # Call to and from new Element Table
        write_data(struct.pack("<II", 0xF39946F0, 0x46C7FB5D), 0x2E6940)
        
        # Read Element Table
        write_data(struct.pack("<BBBBBBBBBBBBBB",0x07,0xA3,0x62,0x46,0x9B,0x18,0x0A,0x1C,0x1C,0x78,0xEC,0x75,0xF7,0x46),0x680000)
        
        # Write Element Table from Virus and Navi table
        elemtable = 0x680020
        for enemy in range(0, 244):
            element = read_byte(0x19618 + (enemy*8) + 1) >> 4
            write_data(chr(0), 0x19618 + (enemy*8) + 1)
            write_data(chr(element),0x680020 + (enemy))
    
    if ALLOW_VIRUSES == 1:
        init_virus_data()
        randomize_viruses()
        randomize_virus_drops()
    if ALLOW_FOLDERS == 1:
        randomize_folders()
    if ALLOW_GMD == 1:
        randomize_gmds()
    if ALLOW_BMD == 1 or ALLOW_TRADES == 1:
        randomize_bmds_trades()
    randomize_shops()
    if ALLOW_SHOPS == 1:
        randomize_number_trader()
    if NC_SHAPERANDOMIZER == 1:
        randomize_navicust()
    if BF_PANELRANDOMIZER >= 1:
        randomize_battlefields()
    
    # I don't suggest doing this if you're new.
    if HELL_MODE >= 1:
        hpups = 0x2b16a
        hpmem1 = 0x2b110
        hpmem2 = 0x473c8
        if ROMVERSION == "b":
            hpups = 0x2b152
            hpmem1 = 0x2b0f8
            hpmem2 = 0x473b0
        write_data(struct.pack('<I', 0x2164), hpups)
        # Trying this one? Your funeral.
        if HELL_MODE >= 2:
            write_data(chr(0), hpmem1)
        # If you can beat the game with this on, you're too good.
        if HELL_MODE >= 3:
            write_data(chr(5), 0x469c)
            write_data(struct.pack("<I", 0x2201), hpmem2)
            
    # Write hash at specific offset based on ROM version
    random.seed(SEED + "_" + str(ALLOW_DAILY) + str(ALLOW_GMD) + str(ALLOW_BMD) + str(ALLOW_CHIPS) + str(ALLOW_FOLDERS) + str(ALLOW_SHOPS) + str(ALLOW_TRADES) + str(ALLOW_VIRUSES) + str(RANDOM_OBSTACLES) + str(FILL_SHOPS) + str(FREE_SHOPS) + str(TUTORIAL_SKIP) + str(P_MULTIPLIER) + str(P_VARIANCE) + str(V_MULTIPLIER) + str(VH_VARIANCE) + str(RANDOM_NAVIS) + str(CP_NAMERANDOMIZER) + str(VN_NAMERANDOMIZER) + str(C_ALLSTARMODE) + str(NC_SHAPERANDOMIZER) + str(BF_PANELRANDOMIZER) + str(ELEMENT_MODE) + str(REGMEM_MODE) + str(OMEGA_MODE) + str(HELL_MODE) + str(FOLDER_MODE) + str(IGNORE_LIMITS) + str(CPRICE_VARIANCE))
    finalhash = ""
    seed_hash = ""
    i = 0
    
    # After Tutorial Intro Text Boxes
    textbox_string1 = "Hash:"
    for i in range(0,len(textbox_string1)-1):
        finalhash = finalhash + chr(mmchars.index(textbox_string1[i]))
    finalhash = finalhash + chr(0xe8)
    for i in range(1,20):
        if i % 4 == 0:
            seed_hash = seed_hash + "-"
            finalhash = finalhash + chr(0)
        else:
            hashchar = random.randint(0,len(mmchars)-1)
            seed_hash = seed_hash + format(hashchar, "x")
            if not i % 4 == 3:
                seed_hash = seed_hash + ","
            finalhash = finalhash + chr(hashchar)
    setintro = "\x02\x00\xED\x01\xF1\x00"
    if FOLDER_MODE > 0:
        write_data(struct.pack("H", 0x42A4), 0x198C)
        write_data(struct.pack("H", 0x42A4), 0x199E)
        setintro = setintro + "\xFB\x34\x01\xFB\x34\x0A\x10\x33\x30\x28\x29\x36\x00\x16\x33\x27\x2F\x00\x0B\x27\x38\x2D\x3A\x29\x4D\xE8"
        if ROMVERSION == "b":
            write_data(chr(5), 0x2DC4A)
        else:
            write_data(chr(5), 0x2DC62)
    setintro = setintro + finalhash + "\xEB\xE9"
    setintro = setintro + "\xF2\x00\x63\x01\xF2\x00\x64\x01\xF2\x00\x65\x01\xF2\x00\x66\x01\xF1\x01\xE7\x00"
    for i in range(0, len(setintro)-1):
        write_data(setintro[i], 0x778A40 + i)
    if ROMVERSION == "b":
        write_data(struct.pack("<I", 0x8778A40), 0xFECA4)
    else:
        write_data(struct.pack("<I", 0x8778A40), 0xFEBB4)
    
    # Enable Omega fights after the final boss
    # More textbox shenanigans mostly, just don't mess with it.
    setenableomega = "\x14\x00\x26\x00\x34\x00\xC1\x00\xDA\x00\x01\x01\x1D\x01\x7A\x01\x86\x01\xC4\x01\xF2\x00\x92\x01\xED\x00\x42\xF1\x00\x16\x4C\x16\x4C\x16\x25\x4C\xEB\xE7\xED\x00\x42\xF1\x00\x16\x25\x32\x47\xEB\xE9\xF5\x00\x02\xED\x00\x00\xF1\x00\x4C\x4C\x4C\x4C\xE8\x17\x29\x2B\x25\x17\x25\x32\x47\xEB\xE9\x1D\x33\x00\x38\x2C\x29\x00\x1A\x39\x30\x37\x29\xE8\x1E\x36\x25\x32\x37\x31\x2D\x37\x37\x2D\x33\x32\x00\x3B\x33\x36\x2F\x29\x28\x47\xEB\xE9\x13\x50\x31\x00\x2D\x32\x00\x0D\x3D\x26\x29\x36\x3B\x33\x36\x30\x28\x47\xEB\xE9\x13\x50\x3A\x29\x00\x32\x29\x3A\x29\x36\x00\x26\x29\x29\x32\x00\x25\x26\x30\x29\xE8\x38\x33\x00\x30\x33\x33\x2F\x00\x25\x38\x00\x3D\x33\x39\x00\x30\x2D\x2F\x29\xE8\x38\x2C\x2D\x37\x47\x00\x1E\x2C\x2D\x37\x00\x2D\x37\x00\x2B\x36\x29\x25\x38\x47\xEB\xE9\xF5\x00\x03\xED\x00\x42\xF1\x00\x13\x00\x25\x2B\x36\x29\x29\x47\x00\x13\x38\x00\x2D\x37\x47\xEB\xE9\xF5\x00\x04\xED\x00\x00\xF1\x00\x13\x38\x50\x37\x00\x25\x30\x31\x33\x37\x38\x00\x30\x2D\x2F\x29\x4C\xE8\x25\x00\x28\x36\x29\x25\x31\x4C\x18\x33\x47\xEB\xE9\xF5\x00\x05\xED\x00\x42\xF1\x00\x16\x25\x32\x48\x00\x21\x2C\x25\x38\x50\x37\x00\x3B\x36\x33\x32\x2B\x48\xEB\xE9\xF5\x00\x06\xED\x00\x00\xF1\x00\x18\x33\x4B\x32\x33\x38\x2C\x2D\x32\x2B\x4D\xE8\x18\x33\x38\x2C\x2D\x32\x2B\x00\x2D\x31\x34\x33\x36\x38\x25\x32\x38\x4D\xEB\xE9\x21\x2D\x30\x3D\x00\x2D\x37\x00\x38\x2C\x2D\x37\xE8\x3B\x25\x3D\x47\x00\x16\x29\x38\x50\x37\x00\x2B\x33\x00\x37\x25\x3A\x29\xE8\x38\x2C\x29\x00\x3B\x33\x36\x30\x28\x00\x38\x33\x2B\x29\x38\x2C\x29\x36\x47\xEB\xE9\xF5\x00\x07\xED\x00\x42\xF1\x00\x23\x29\x25\x2C\x47\xEB\xE7\xED\x00\x00\xF1\x00\x21\x29\x00\x28\x33\x32\x50\x38\x00\x2C\x25\x3A\x29\x00\x31\x39\x27\x2C\xE8\x38\x2D\x31\x29\x47\x00\x21\x29\x00\x2C\x25\x3A\x29\x00\x38\x33\xE8\x2A\x2D\x32\x28\x00\x21\x2D\x30\x3D\x00\x35\x39\x2D\x27\x2F\x47\xEB\xE9\xF5\x00\x09\xED\x00\x42\xF1\x00\x1C\x33\x2B\x29\x36\x47\x47\xEB\xE7"
    if ROMVERSION == "b":
        write_data(struct.pack("<I", len(randomized_data)+0x08000000),0x12647C)
    else:
        write_data(struct.pack("<I", len(randomized_data)+0x08000000),0x12637C)
    for i in range(0, len(setenableomega)-1):
        write_data(setenableomega[i], len(randomized_data))
    
    # Output Rom
    open(output_path + ".gba", 'wb').write(bytes(''.join((chr(checkval(x)) for x in randomized_data)), encoding="raw_unicode_escape"))
    print("Seed: " + str(SEED))
    print("Hash: " + seed_hash)
    print("ROM Output: \"" + output_path + "\".")
    
    #Spoiler Info
    open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'w').write("Seed: " + str(SEED) + "\nHash: " + seed_hash + "\n\nChip Damage Multiplier: " + str(P_MULTIPLIER) + "\nChip Damage Variance: " + str(P_VARIANCE) + "\nChip Price Variance: " + str(CPRICE_VARIANCE) + "\nEnemy HP Multiplier: " + str(V_MULTIPLIER) + "\nEnemy HP Variance: " + str(VH_VARIANCE) + "\nChip Codes Mode: " + str(C_ALLSTARMODE) + "\nRandomized Chip Names?: " + str(bool(CP_NAMERANDOMIZER)) + "\nRandomized Enemy Names?: " + str(bool(VN_NAMERANDOMIZER)) + "\nRandomized NaviCust Shapes?: " + str(bool(NC_SHAPERANDOMIZER)) + "\nRandom Battlefield Mode: " + str(int(BF_PANELRANDOMIZER)) + "\nRandom Element Mode: " + str(int(ELEMENT_MODE))+ "\nRandomize Navis?: " + str(bool(RANDOM_NAVIS))+ "\nFolder Lock Mode: " + str(FOLDER_MODE)+ "\nOMEGA Mode: " + str(OMEGA_MODE)+ "\nRegMem Max Range: " + str(int(REGMEM_MODE))+ "\nHELL Mode: " + str(HELL_MODE))
    open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("\n\nAllow Folders?: "+str(bool(ALLOW_FOLDERS))+"\nAllow Blue Mystery Data?: "+str(bool(ALLOW_BMD))+"\nAllow Green Mystery Data?: "+str(bool(ALLOW_GMD))+"\nAllow Shops?: "+str(bool(ALLOW_SHOPS))+"\nAllow Battle Chips?: "+str(bool(ALLOW_CHIPS))+"\nAllow Viruses?: "+str(bool(ALLOW_VIRUSES))+"\nAllow NPC Trades?: "+str(bool(ALLOW_TRADES)))
    open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("\n\nAllow Easy Tutorial?: "+str(bool(TUTORIAL_SKIP))+"\nRandomize Battle Objects?: "+str(bool(RANDOM_OBSTACLES))+"\nFree BattleChips in Shops?: "+str(bool(FREE_SHOPS))+"\nFill Shops?: "+str(bool(FILL_SHOPS))+"\nIgnore HP/Damage Limiters?: "+str(bool(IGNORE_LIMITS)))
    if OUTPUTLOG == 1:
        open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n!!!!!!!!!!!!!!\n!!!SPOILERS!!!\n!!!!!!!!!!!!!!\n\n")
        print("!!NOTE!! Writing detailed log to seedinfo.txt, this will take a few...")
        for i in range(len(changelog_chip)):
            open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write(changelog_chip[i][0] + " -> " + changelog_chip[i][1] + ", Power: " + str(changelog_chip[i][2]) + " -> " + str(changelog_chip[i][3]) + ", Codes: " + changelog_chip[i][4] + ", RegMem: " + str(changelog_chip[i][5]) + "\n")
        for i in range(0, len(changelog_pas)-1):
            open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("Sequence Program Advance Requirement #" + str(i) + ": " + hex(0x100 + changelog_pas[i][0]) + " - " + chip_codes[int((changelog_pas[i][1]-1)/2)] + " -> " + chip_codes[int((changelog_pas[i][2]-1)/2)] + "\n")
        for i in range(0, len(changelog_battles)-1):
            name1 = ""
            name2 = ""
            if changelog_battles[i][0] == "virus":
                hp1, damage1, name1 = virus_data[changelog_battles[i][2]]
                hp2, damage2, name2 = virus_data[changelog_battles[i][3]]
                open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("Battle #" + str(changelog_battles[i][1]) + ": " + name1 + " (" + str(changelog_battles[i][2]) + ") -> " + name2 + " (" + str(changelog_battles[i][3]) + ")\n")
            elif changelog_battles[i][0] == "navi":
                offset1, hp1, name1 = navi_data[changelog_battles[i][2]]
                offset2, hp2, name2 = navi_data[changelog_battles[i][3]]
                open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("Battle #" + str(changelog_battles[i][1]) + ": " + name1 + " (" + str(changelog_battles[i][2]+168) + ") -> " + name2 + " (" + str(changelog_battles[i][3]+168) + ")\n")
            elif changelog_battles[i][0] == "obstacle":
                name1 = obstacles[changelog_battles[i][2]]
                name2 = obstacles[changelog_battles[i][3]]
                open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("Battle #" + str(changelog_battles[i][1]) + ": " + name1 + " -> " + name2 + "\n")
        for i in range(0, len(changelog_fields)-1):
            if changelog_fields[i][0] == "data":
                open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("Stage #" + str(changelog_fields[i][1]) + ": " + changelog_fields[i][2] + " -> " + changelog_fields[i][3] + "\n")
            elif changelog_fields[i][0] == "id":
                open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("Stage ID Offset " + hex(int(changelog_fields[i][1])) + " changed to " + changelog_fields[i][2] + ".\n")
        for i in range(len(changelog_virus)):
            open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write(changelog_virus[i][0] + " -> " + changelog_virus[i][1] + ", HP: " + str(changelog_virus[i][2]) + "\n")
        for i in range(len(changelog_gmd)):
            if changelog_gmd[i][0] == "chip":
                open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("GMD #" + str(i) + " Data: " + chip_names[changelog_gmd[i][1]-1] + " (" + str(changelog_gmd[i][1]) + ") -> " + chip_names[changelog_gmd[i][2]-1] + " (" + str(changelog_gmd[i][2]) + ") " + chip_codes[changelog_gmd[i][3]] + "\n")
            elif changelog_gmd[i][0] == "zenny":
                open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("GMD #" + str(i) + " Data: " + str(changelog_gmd[i][1]) + ", " + str(changelog_gmd[i][2]) + ", " + str(changelog_gmd[i][3]) + ", " + str(changelog_gmd[i][4]) + ", " + str(changelog_gmd[i][5]) + ", " + str(changelog_gmd[i][6]) + ", " + str(changelog_gmd[i][7]) + ", " + str(changelog_gmd[i][8]) + ", " + str(changelog_gmd[i][9]) + ", " + str(changelog_gmd[i][10]) + ", " + str(changelog_gmd[i][11]) + ", " + str(changelog_gmd[i][12]) + ", " + str(changelog_gmd[i][13]) + ", " + str(changelog_gmd[i][14]) + ", " + str(changelog_gmd[i][15]) + ", " + str(changelog_gmd[i][16]) + "\n")
        for i in range(len(changelog_bmd)):
            if changelog_bmd[i][0] == "chip":
                open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("BMD #" + str(i) + " Data: " + chip_names[changelog_bmd[i][1]-1] + " (" + str(changelog_bmd[i][1]) + ") " + chip_codes[changelog_bmd[i][2]] + " -> " + chip_names[changelog_bmd[i][3]-1] + " (" + str(changelog_bmd[i][3]) + ") " + chip_codes[changelog_bmd[i][4]] + "\n")
            elif changelog_bmd[i][0] == "zenny":
                open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("BMD #" + str(i) + " Data: " + str(changelog_bmd[i][1]) + " -> " + str(changelog_bmd[i][2]) + "\n")
        for i in range(len(changelog_ncp)):
            open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write(changelog_ncp[i][0] + " Uncompressed: " + str(changelog_ncp[i][1]) + ", Compressed: " + str(changelog_ncp[i][2]) + "\n")
        for i in range(len(changelog_folders)):
            open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("Folder #" + str(changelog_folders[i][0]) + " Chip #" + str(changelog_folders[i][1]) + ": " + chipnames_in_order[changelog_folders[i][2]-1] + " (" + str(changelog_folders[i][2]) + ") " + chip_codes[changelog_folders[i][3]] + " -> " + chipnames_in_order[changelog_folders[i][4]-1] + " (" + str(changelog_folders[i][4]) + ") " + chip_codes[changelog_folders[i][5]] + "\n")
        for i in range(len(changelog_drops)):
            open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("Virus #" + str(changelog_drops[i][0]) + ": " + chip_names[changelog_drops[i][1]-1] + " (" + str(changelog_drops[i][1]) + ") " + chip_codes[changelog_drops[i][2]] + " -> " + chip_names[changelog_drops[i][3]-1] + " (" + str(changelog_drops[i][3]) + ") " + chip_codes[changelog_drops[i][4]] + "\n")
        for i in range(len(changelog_shops)):
            open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("Shop #" + str(changelog_shops[i][0]) + ": " + chip_names[changelog_shops[i][1]-1] + " (" + str(changelog_shops[i][1]) + ") " + chip_codes[changelog_shops[i][2]] + " - " + str(changelog_shops[i][3]) + " Zennys\n")
        for i in range(len(changelog_numbertrader)):
            open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("NumberTrader Chip #" + str(i) + ": " + chip_names[changelog_numbertrader[i][0]-1] + " (" + str(changelog_numbertrader[i][0]) + ") " + chip_codes[changelog_numbertrader[i][1]] + "\n")
        for i in range(len(changelog_trades)):
            open(output_path + ".gba.mmbn3." + ROMVERSION + ".log(" + seed_hash + ").txt", 'a').write("Trade #" + str(i) + " Requirement: " + chip_names[changelog_trades[i][1]-1] + " (" + str(changelog_trades[i][1]) + ") " + chip_codes[changelog_trades[i][2]] + " -> " + chip_names[changelog_trades[i][3]-1] + " (" + str(changelog_trades[i][3]) + ") " + chip_codes[changelog_trades[i][4]] + "\n")
        print("Output Log:", "mmbn3" + ROMVERSION + ".log(" + seed_hash + ").txt")
    print("### Done! Enjoy your game!")
    if ALLOW_DAILY == 1:
        print("\n!!NOTE!! Be sure to read this daily run's base output info!")
    #raw_input("Done! Press Enter to exit.")
