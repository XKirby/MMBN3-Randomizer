import argparse

def main():
        global ALLOW_FOLDERS
        global ALLOW_GMD
        global ALLOW_BMD
        global ALLOW_SHOPS
        global ALLOW_CHIPS
        global ALLOW_VIRUSES
        global ALLOW_TRADES
        
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
        global BASEHP
        global REGMEM_MODE
        global FOLDER_MODE
        global OUTPUTLOG

        global TUTORIAL_SKIP
        global RANDOM_OBSTACLES
        global FILL_SHOPS
        global IGNORE_LIMITS
        
        global INPUT_FILE
        global OUTPUT_FILE
        
        #Argument Parser
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--input", help="Type in values manually.", action="count", default=0)
        parser.add_argument("-in", "--infile", help="The input filepath for your clean rom.", default="")
        parser.add_argument("-out", "--outfile", help="The output filepath for your randomized rom.", default="")
        parser.add_argument("-v", "--version", help="Rom Version, character.", choices=["w", "b", "W", "B"], default="w")
        parser.add_argument("-cdm", "--chipdamagemult", help="Chip/PA Damage Multiplier, float.", type=float, default=1.0)
        parser.add_argument("-cdv", "--chipdamagevar", help="Chip/PA Damage Variance, float.", type=float, default=0.0)
        parser.add_argument("-edm", "--enemydamagemult", help="Virus/Navi HP Multiplier, float.", type=float, default=1.0)
        parser.add_argument("-edv", "--enemydamagevar", help="Virus/Navi HP Variance, float.", type=float, default=0.0)
        parser.add_argument("-cr", "--coderoulettemode", help="Chip Code Roulette Mode, integer.", type=int, choices=[0,1,2,3], default=0)
        parser.add_argument("-cn", "--chipnames", help="Chip/PA Name Randomizer, boolean.", type=int, choices=[0,1], default=0)
        parser.add_argument("-en", "--enemynames", help="Virus/Navi Name Randomizer, boolean.", type=int, choices=[0,1], default=0)
        parser.add_argument("-ncp", "--progshapes", help="NCP Shape Randomizer, boolean.", type=int, choices=[0,1], default=0)
        parser.add_argument("-elem", "--elements", help="Element Randomizer, integer.", type=int, choices=[0,1,2,3], default=0)
        parser.add_argument("-om", "--omegamode", help="Omega Mode, integer.", type=int, choices=[0,1,2,3], default=0)
        parser.add_argument("-hm", "--hellmode", help="Hell Mode, integer.", type=int, choices=[0,1,2,3], default=0)
        parser.add_argument("-rm", "--regmem", help="RegMem Randomizer, integer. (1-99 for randomized)", type=int, default=0)
        parser.add_argument("-navi", "--randomnavi", help="Randomize Navi Encounters, integer.", type=int, choices=[0,1], default=0)
        parser.add_argument("-bf", "--battlefields", help="Randomize Battlefield Stages, integer.", type=int, choices=[0,1,2], default=0)
        parser.add_argument("-fl", "--folderlock", help="Folder Lock Mode, integer.", type=int, choices=[0,1,2,3,4], default=0)
        parser.add_argument("-tut", "--tutorial", help="Skip Tutorial Randomization, boolean.", type=int, choices=[0,1], default=1)
        parser.add_argument("-fs", "--fillshops", help="Fill Shops, boolean.", type=int, choices=[0,1], default=1)
        parser.add_argument("-bo", "--battleobjects", help="Randomize Battle Objects, boolean.", type=int, choices=[0,1], default=0)
        parser.add_argument("--allowfolder", help="Allow Folder Randomization, boolean.", type=int, choices=[0,1], default=1)
        parser.add_argument("--allowgmd", help="Allow Green Mystery Data Randomization, boolean.", type=int, choices=[0,1], default=1)
        parser.add_argument("--allowbmd", help="Allow Blue Mystery Data Randomization, boolean.", type=int, choices=[0,1], default=1)
        parser.add_argument("--allowshop", help="Allow Shop Randomization, boolean.", type=int, choices=[0,1], default=1)
        parser.add_argument("--allowchip", help="Allow Battle Chip Randomization, boolean.", type=int, choices=[0,1], default=1)
        parser.add_argument("--allowvirus", help="Allow Enemy Navi/Virus Randomization, boolean.", type=int, choices=[0,1], default=1)
        parser.add_argument("--allowtrades", help="Allow Trade Randomization, boolean.", type=int, choices=[0,1], default=1)
        parser.add_argument("--daily", help="Perform today's Daily Run, integer.", type=int, choices=[0,1], default=0)
        parser.add_argument("--seed", help="Game Seed, string.", default="")
        parser.add_argument("--log", help="Output Log, boolean. Turn on for expanded seed info.", type=int, choices=[0,1], default=0)
        parser.add_argument("-lb", "--limitbreak", help="Uncaps Multipliers on HP and Damage, boolean.", type=int, choices=[0,1], default=0)
        args = parser.parse_args()
        
        #Variable Defaults based on Arguments
        INPUT_FILE = args.infile
        OUTPUT_FILE = args.outfile
        ROMVERSION = args.version
        P_MULTIPLIER = args.chipdamagemult
        P_VARIANCE = args.chipdamagevar
        V_MULTIPLIER = args.enemydamagemult
        VH_VARIANCE = args.enemydamagevar
        C_ALLSTARMODE = args.coderoulettemode
        CP_NAMERANDOMIZER = args.chipnames
        VN_NAMERANDOMIZER = args.enemynames
        NC_SHAPERANDOMIZER = args.progshapes
        BF_PANELRANDOMIZER = args.battlefields
        ELEMENT_MODE = args.elements
        OMEGA_MODE = args.omegamode
        HELL_MODE = args.hellmode
        REGMEM_MODE = args.regmem
        RANDOM_NAVIS = args.randomnavi
        FOLDER_MODE = args.folderlock
        TUTORIAL_SKIP = args.tutorial
        FILL_SHOPS = args.fillshops
        RANDOM_OBSTACLES = args.battleobjects
        ALLOW_FOLDERS = args.allowfolder
        ALLOW_GMD = args.allowgmd
        ALLOW_BMD = args.allowbmd
        ALLOW_SHOPS = args.allowshop
        ALLOW_CHIPS = args.allowchip
        ALLOW_VIRUSES = args.allowvirus
        ALLOW_TRADES = args.allowtrades
        ALLOW_DAILY = args.daily
        SEED = args.seed
        OUTPUTLOG = args.log
        IGNORE_LIMITS = args.limitbreak
        
        #Variable Input
        if args.input >= 1:
                INPUT_FILE = str(raw_input("The input filepath to your clean rom.> "))
                OUTPUT_FILE = str(raw_input("The output filepath of the randomized rom.> "))
                ROMVERSION = str(raw_input("Which Version? [W/B]> "))
                P_MULTIPLIER = float(raw_input("Input Damage Multiplier Float> "))
                P_VARIANCE = float(raw_input("Input Damage Variance Float> "))
                V_MULTIPLIER = float(raw_input("Input Enemy HP Multiplier Float> "))
                VH_VARIANCE = float(raw_input("Input Enemy HP Variance Float> "))
                C_ALLSTARMODE = int(raw_input("Input Chip Code Roulette Mode [0-3]> ")) % 4
                CP_NAMERANDOMIZER = int(raw_input("Randomize Chip/PA Names? [0-1]> ")) % 2
                VN_NAMERANDOMIZER = int(raw_input("Randomize Enemy Names? [0-1]> ")) % 2
                NC_SHAPERANDOMIZER = int(raw_input("Randomize NaviCust Shapes? [0-1]> ")) % 2
                BF_PANELRANDOMIZER = int(raw_input("Randomize Battlefield Stages? [0-2]> ")) % 3
                ELEMENT_MODE = int(raw_input("Randomize Elements? [0-3]> ")) % 4
                RANDOM_NAVIS = int(raw_input("Randomize Navis? [0-1]> ")) % 2
                FOLDER_MODE = int(raw_input("Enable Folder Lock Mode? [0-4]> ")) % 5
                OMEGA_MODE = int(raw_input("Enable Omega Mode? [0-3]> ")) % 4
                REGMEM_MODE = int(raw_input("Randomize Regular Memory Values? [0-99]> ")) % 100
                HELL_MODE = int(raw_input("Enable Hell Mode? [0-3]> ")) % 4
                TUTORIAL_SKIP = int(raw_input("Disable Tutorial Randomization? [0-1]> ")) % 2
                FILL_SHOPS = int(raw_input("Fill Shops? [0-1]> ")) % 2
                RANDOM_OBSTACLES = int(raw_input("Randomized Battle Objects? [0-1]> ")) % 2
                ALLOW_FOLDERS = int(raw_input("Allow Folder Randomization? [0-1]> ")) % 2
                ALLOW_GMD = int(raw_input("Allow GMD Randomization? [0-1]> ")) % 2
                ALLOW_BMD = int(raw_input("Allow BMD Randomization? [0-1]> ")) % 2
                ALLOW_SHOPS = int(raw_input("Allow Shop Randomization? [0-1]> ")) % 2
                ALLOW_CHIPS = int(raw_input("Allow Chip Randomization? [0-1]> ")) % 2
                ALLOW_VIRUSES = int(raw_input("Allow Enemy Randomization? [0-1]> ")) % 2
                ALLOW_TRADES = int(raw_input("Allow Trade Randomization? [0-1]> ")) % 2
                ALLOW_DAILY = int(raw_input("Is this a Daily Run? [0-1]> ")) % 2
                SEED = str(raw_input("Input Seed?> "))
                OUTPUTLOG = int(raw_input("Enable Output Log? [0-1]> ")) % 2
                IGNORE_LIMIT = int(raw_input("Ignore HP/Damage Multiplier Limits? [0-1]> ")) % 2
        if len(ROMVERSION) != 1:
                return
        ROMVERSION = ROMVERSION.lower()
        if ROMVERSION != "b" and ROMVERSION != "w":
                return
        if len(INPUT_FILE) < 1 or len(OUTPUT_FILE) < 1:
                return
        import bn3random
        bn3random.randomizerom(INPUT_FILE, OUTPUT_FILE, ROMVERSION, SEED, P_MULTIPLIER, P_VARIANCE, V_MULTIPLIER, VH_VARIANCE, C_ALLSTARMODE, CP_NAMERANDOMIZER, VN_NAMERANDOMIZER, RANDOM_NAVIS, ELEMENT_MODE, REGMEM_MODE, NC_SHAPERANDOMIZER, OMEGA_MODE, HELL_MODE, BF_PANELRANDOMIZER, FOLDER_MODE, OUTPUTLOG, RANDOM_OBSTACLES, FILL_SHOPS, ALLOW_FOLDERS, ALLOW_GMD, ALLOW_BMD, ALLOW_SHOPS, ALLOW_CHIPS, ALLOW_VIRUSES, ALLOW_TRADES, ALLOW_DAILY, TUTORIAL_SKIP, IGNORE_LIMITS)

if __name__ == '__main__':
        main()
