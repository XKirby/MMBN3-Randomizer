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
        global CPRICE_VARIANCE
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
        global FREE_SHOPS
        global IGNORE_LIMITS
        global ZENNY_MULTIPLIER
        global RANKCHECK
        
        global INPUT_FILE
        global OUTPUT_FILE
        
        #Argument Parser
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--input", help="Type in values manually.", action="count", default=0)
        parser.add_argument("-in", "--infile", help="The input filepath for your clean rom.", default="")
        parser.add_argument("-cdm", "--chipdamagemult", help="Chip/PA Damage Multiplier, float.", type=float, default=1.0)
        parser.add_argument("-cdv", "--chipdamagevar", help="Chip/PA Damage Variance, float.", type=float, default=0.0)
        parser.add_argument("-cpv", "--chippricevar", help="Chip Price Variance, float.", type=float, default=0.0)
        parser.add_argument("-edm", "--enemydamagemult", help="Virus/Navi HP Multiplier, float.", type=float, default=1.0)
        parser.add_argument("-edv", "--enemydamagevar", help="Virus/Navi HP Variance, float.", type=float, default=0.0)
        parser.add_argument("-cr", "--coderoulettemode", help="Chip Code Roulette Mode, integer.", type=int, choices=[0,1,2,3], default=0)
        parser.add_argument("-cn", "--chipnames", help="Chip/PA Name Randomizer, boolean.", type=int, choices=[0,1], default=0)
        parser.add_argument("-en", "--enemynames", help="Virus/Navi Name Randomizer, boolean.", type=int, choices=[0,1], default=0)
        parser.add_argument("-ncp", "--progshapes", help="NCP Shape Randomizer, boolean.", type=int, choices=[0,1], default=0)
        parser.add_argument("-elem", "--elements", help="Element Randomizer, integer.", type=int, choices=[0,1,2,3], default=0)
        parser.add_argument("-om", "--omegamode", help="Omega Mode, integer.", type=int, choices=[0,1,2,3,4,5,6,7], default=0)
        parser.add_argument("-hm", "--hellmode", help="Hell Mode, integer.", type=int, choices=[0,1,2,3], default=0)
        parser.add_argument("-rm", "--regmem", help="RegMem Randomizer, integer. (1-99 for randomized)", type=int, default=0)
        parser.add_argument("-navi", "--randomnavi", help="Randomize Navi Encounters, integer.", type=int, choices=[0,1], default=0)
        parser.add_argument("-bf", "--battlefields", help="Randomize Battlefield Stages, integer.", type=int, choices=[0,1,2], default=0)
        parser.add_argument("-fl", "--folderlock", help="Folder Lock Mode, integer.", type=int, choices=[0,1,2,3,4,5,6], default=0)
        parser.add_argument("-tut", "--tutorial", help="Skip Tutorial Randomization, boolean.", type=int, choices=[0,1], default=1)
        parser.add_argument("-fs", "--fillshops", help="Fill Shops, boolean.", type=int, choices=[0,1], default=1)
        parser.add_argument("-fc", "--freechips", help="Free Chips in Shops, boolean.", type=int, choices=[0,1], default=1)
        parser.add_argument("-bo", "--battleobjects", help="Randomize Battle Objects, boolean.", type=int, choices=[0,1], default=0)
        parser.add_argument("-zen", "--zennymult", help="Zenny Multiplier, float.", type=float, default=1.5)
        parser.add_argument("-rank", "--droprank", help="Chip Drop Ranks, int.", type=float, default=5)
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
        FREE_SHOPS = args.freechips
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
        ZENNY_MULTIPLIER = args.zennymult
        RANKCHECK = args.droprank
        CPRICE_VARIANCE = args.chippricevar
        
        #Variable Input
        if args.input >= 1:
                INPUT_FILE = str(input("The input filepath to your clean rom.> "))
                ZENNY_MULTIPLIER = float(input("Input Zenny Multiplier Float> "))
                RANKCHECK = int(input("Input Chip Drop Rank> ")) % 11
                P_MULTIPLIER = float(input("Input Damage Multiplier Float> "))
                P_VARIANCE = float(input("Input Damage Variance Float> "))
                CPRICE_VARIANCE = float(input("Input Chip Price Variance Float> "))
                V_MULTIPLIER = float(input("Input Enemy HP Multiplier Float> "))
                VH_VARIANCE = float(input("Input Enemy HP Variance Float> "))
                C_ALLSTARMODE = int(input("Input Chip Code Roulette Mode [0-3]> ")) % 4
                CP_NAMERANDOMIZER = int(input("Randomize Chip/PA Names? [0-1]> ")) % 2
                VN_NAMERANDOMIZER = int(input("Randomize Enemy Names? [0-1]> ")) % 2
                NC_SHAPERANDOMIZER = int(input("Randomize NaviCust Shapes? [0-1]> ")) % 2
                BF_PANELRANDOMIZER = int(input("Randomize Battlefield Stages? [0-2]> ")) % 3
                ELEMENT_MODE = int(input("Randomize Elements? [0-3]> ")) % 4
                RANDOM_NAVIS = int(input("Randomize Navis? [0-1]> ")) % 2
                FOLDER_MODE = int(input("Enable Folder Lock Mode? [0-4]> ")) % 7
                OMEGA_MODE = int(input("Enable Omega Mode? [0-3]> ")) % 8
                REGMEM_MODE = int(input("Randomize Regular Memory Values? [0-99]> ")) % 100
                HELL_MODE = int(input("Enable Hell Mode? [0-3]> ")) % 4
                TUTORIAL_SKIP = int(input("Disable Tutorial Randomization? [0-1]> ")) % 2
                FILL_SHOPS = int(input("Fill Shops? [0-1]> ")) % 2
                FREE_SHOPS = int(input("Free Shops? [0-1]> ")) % 2
                RANDOM_OBSTACLES = int(input("Randomized Battle Objects? [0-1]> ")) % 2
                ALLOW_FOLDERS = int(input("Allow Folder Randomization? [0-1]> ")) % 2
                ALLOW_GMD = int(input("Allow GMD Randomization? [0-1]> ")) % 2
                ALLOW_BMD = int(input("Allow BMD Randomization? [0-1]> ")) % 2
                ALLOW_SHOPS = int(input("Allow Shop Randomization? [0-1]> ")) % 2
                ALLOW_CHIPS = int(input("Allow Chip Randomization? [0-1]> ")) % 2
                ALLOW_VIRUSES = int(input("Allow Enemy Randomization? [0-1]> ")) % 2
                ALLOW_TRADES = int(input("Allow Trade Randomization? [0-1]> ")) % 2
                ALLOW_DAILY = int(input("Is this a Daily Run? [0-1]> ")) % 2
                SEED = str(input("Input Seed?> "))
                OUTPUTLOG = int(input("Enable Output Log? [0-1]> ")) % 2
                IGNORE_LIMIT = int(input("Ignore HP/Damage Multiplier Limits? [0-1]> ")) % 2
        import bn3random
        bn3random.randomizerom(INPUT_FILE, SEED, P_MULTIPLIER, P_VARIANCE, V_MULTIPLIER, VH_VARIANCE, C_ALLSTARMODE, CP_NAMERANDOMIZER, VN_NAMERANDOMIZER, RANDOM_NAVIS, ELEMENT_MODE, REGMEM_MODE, NC_SHAPERANDOMIZER, OMEGA_MODE, HELL_MODE, BF_PANELRANDOMIZER, FOLDER_MODE, OUTPUTLOG, RANDOM_OBSTACLES, FILL_SHOPS, FREE_SHOPS, ALLOW_FOLDERS, ALLOW_GMD, ALLOW_BMD, ALLOW_SHOPS, ALLOW_CHIPS, ALLOW_VIRUSES, ALLOW_TRADES, ALLOW_DAILY, TUTORIAL_SKIP, IGNORE_LIMITS, CPRICE_VARIANCE, ZENNY_MULTIPLIER, RANKCHECK)

if __name__ == '__main__':
        main()
