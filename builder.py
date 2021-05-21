import json
import math
from itertools import permutations
import numpy as np
from collections import Counter


def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


def round_tonoteven(x, d=0):
    p = 10 ** d
    if x > 0:
        return int(float(math.floor((x * p) + 0.5)) / p)
    else:
        return int(float(math.ceil((x * p) - 0.5)) / p)


def neutralconversion(neutral_base, neutral, pct_convert):
    convert = min(neutral, neutral_base * pct_convert)
    elemental = math.floor(convert)
    new_neutral = math.floor(neutral - convert)
    return elemental, new_neutral


def skillpoints_topercentage(sp):
    return clamp((-0.0000000066695 * math.pow(math.e, -0.00924033 * sp + 18.9) + 1.0771), 0.00, 0.808)


def level_tobasehp(level):
    if level < 1:
        return level_tobasehp(1)
    elif level > 106:
        return level_tobasehp(106)
    else:
        return 5 * level + 5


def powderparse(powders):
    powders = powders.lower()
    count = Counter(powders)
    for chars in count:
        if chars not in ['1', '2', '3', '4', '5', '6', 'e', 't', 'w', 'f', 'a']:
            return ''
    if len(powders) % 2 != 0:
        return ''
    else:
        parsedpowders = []
        for i in range(len(powders) // 2):
            parsedpowders.append(powders[i * 2: i * 2 + 2])
        return parsedpowders


class Builder:
    def __init__(self):
        readfile = open('compress.json')
        self.db = json.load(readfile)
        readfile.close()

        self.UNROLLABLES = {'hp', 'eDef', 'tDef', 'wDef', 'fDef', 'aDef', 'str', 'dex', 'int', 'def', 'agi'}

        self.WEAPONDAMAGE = {'nDam', 'eDam', 'tDam', 'wDam', 'fDam', 'aDam'}

        self.ELEMENTALDEF = {'eDef', 'tDef', 'wDef', 'fDef', 'aDef'}

        self.SPELLCOSTSPCT = {'spPct1', 'spPct2', 'spPct3', 'spPct4'}
        self.SPELLCOSTSRAW = {'spRaw1', 'spRaw2', 'spRaw3', 'spRaw4'}

        self.WEAPONTOCLASS = {'bow': 'Archer',
                              'dagger': 'Assassin',
                              'spear': 'Warrior',
                              'relik': 'Shaman',
                              'wand': 'Mage'}

        self.SKILLPOINTS = ['str', 'dex', 'int', 'def', 'agi']

        self.ELEMTOSTAT = {'e': ['eDef', 'eDam'],
                           't': ['tDef', 'tDam'],
                           'w': ['wDef', 'wDam'],
                           'f': ['fDef', 'fDam'],
                           'a': ['aDef', 'aDam']}

        self.equipments = {'helmet': None,
                           'chestplate': None,
                           'leggings': None,
                           'boots': None,
                           'ring1': None,
                           'ring2': None,
                           'bracelet': None,
                           'necklace': None,
                           'weapon': None}

        self.rawstats = {'hp': 0,
                         'nDam': '',
                         'eDam': '',
                         'tDam': '',
                         'wDam': '',
                         'fDam': '',
                         'aDam': '',
                         'eDef': 0,
                         'tDef': 0,
                         'wDef': 0,
                         'fDef': 0,
                         'aDef': 0,
                         'str': 0,
                         'dex': 0,
                         'int': 0,
                         'def': 0,
                         'agi': 0,
                         'eDamPct': 0,
                         'tDamPct': 0,
                         'wDamPct': 0,
                         'fDamPct': 0,
                         'aDamPct': 0,
                         'sdPct': 0,
                         'sdRaw': 0,
                         'mdPct': 0,
                         'mdRaw': 0,
                         'atkTier': 0,
                         'poison': 0,
                         'mr': 0,
                         'ms': 0,
                         'spRaw1': 0,
                         'spRaw2': 0,
                         'spRaw3': 0,
                         'spRaw4': 0,
                         'spPct1': 0,
                         'spPct2': 0,
                         'spPct3': 0,
                         'spPct4': 0,
                         'hprRaw': 0,
                         'hprPct': 0,
                         'hpBonus': 0,
                         'ls': 0,
                         'eDefPct': 0,
                         'tDefPct': 0,
                         'wDefPct': 0,
                         'fDefPct': 0,
                         'aDefPct': 0,
                         'ws': 0,
                         'jh': 0,
                         'sprint': 0,
                         'sprintReg': 0,
                         'thorns': 0,
                         'ref': 0,
                         'expd': 0,
                         'lb': 0,
                         'xpb': 0,
                         'spRegen': 0
                         }

        self.sets, self.setbonus, self.totalstats = ({} for i in range(3))

        self.assignedSP = {'str': 0, 'dex': 0, 'int': 0, 'def': 0, 'agi': 0}

        self.currentclass = 'Mage'

        self.wearorder = []

        # ---------------------- dmg calc relateds ------------------------------

        self.SPELL_TABLE = {
            'wand': [
                {'title': 'Heal', 'cost': 6, 'parts': [
                    {'subtitle': 'First Pulse', 'type': 'heal', 'strength': 0.12},
                    {'subtitle': 'Second and Third Pulses', 'type': 'heal', 'strength': 0.06},
                    {'subtitle': 'Total Heal', 'type': 'heal', 'strength': 0.24, 'summary': True},
                    {'subtitle': 'First Pulse (Ally)', 'type': 'heal', 'strength': 0.2},
                    {'subtitle': 'Second and Third Pulses (Ally)', 'type': 'heal', 'strength': 0.1},
                    {'subtitle': 'Total Heal (Ally)', 'type': 'heal', 'strength': 0.4},
                ]},
                {'title': 'Teleport', 'cost': 4, 'parts': [
                    {'subtitle': 'Total Damage', 'type': 'damage', 'multiplier': 100,
                     'conversion': [60, 0, 40, 0, 0, 0], 'summary': True},
                ]},
                {'title': 'Meteor', 'cost': 8, 'parts': [
                    {'subtitle': 'Blast Damage', 'type': 'damage', 'multiplier': 500,
                     'conversion': [40, 30, 0, 0, 30, 0], 'summary': True},
                    {'subtitle': 'Burn Damage', 'type': 'damage', 'multiplier': 125,
                     'conversion': [100, 0, 0, 0, 0, 0]},
                ]},
                {'title': 'Ice Snake', 'cost': 4, 'parts': [
                    {'subtitle': 'Total Damage', 'type': 'damage', 'multiplier': 70, 'conversion': [50, 0, 0, 50, 0, 0],
                     'summary': True},
                ]},
            ],
            'spear': [
                {'title': 'Bash', 'cost': 6, 'parts': [
                    {'subtitle': 'First Damage', 'type': 'damage', 'multiplier': 130,
                     'conversion': [60, 40, 0, 0, 0, 0]},
                    {'subtitle': 'Explosion Damage', 'type': 'damage', 'multiplier': 130,
                     'conversion': [100, 0, 0, 0, 0, 0]},
                    {'subtitle': 'Total Damage', 'type': 'total', 'factors': [1, 1], 'summary': True},
                ]},
                {'title': 'Charge', 'cost': 4, 'variants': {
                    'DEFAULT': [
                        {'subtitle': 'Total Damage', 'type': 'damage', 'multiplier': 150,
                         'conversion': [60, 0, 0, 0, 40, 0], 'summary': True},
                    ],
                    'RALLY': [
                        {'subtitle': 'Self Heal', 'type': 'heal', 'strength': 0.1, 'summary': True},
                        {'subtitle': 'Ally Heal', 'type': 'heal', 'strength': 0.15},
                    ],
                }},
                {'title': 'Uppercut', 'cost': 9, 'parts': [
                    {'subtitle': 'First Damage', 'type': 'damage', 'multiplier': 300,
                     'conversion': [70, 20, 10, 0, 0, 0]},
                    {'subtitle': 'Fireworks Damage', 'type': 'damage', 'multiplier': 50,
                     'conversion': [60, 0, 40, 0, 0, 0]},
                    {'subtitle': 'Crash Damage', 'type': 'damage', 'multiplier': 50,
                     'conversion': [80, 0, 20, 0, 0, 0]},
                    {'subtitle': 'Total Damage', 'type': 'total', 'factors': [1, 1, 1], 'summary': True},
                ]},
                {'title': 'War Scream', 'cost': 6, 'parts': [
                    {'subtitle': 'Area Damage', 'type': 'damage', 'multiplier': 50, 'conversion': [0, 0, 0, 0, 75, 25],
                     'summary': True},
                    {'subtitle': 'Air Shout (Per Hit)', 'type': 'damage', 'multiplier': 30,
                     'conversion': [0, 0, 0, 0, 75, 25]},
                ]},
            ],
            "bow": [
                {'title': "Arrow Storm", 'cost': 6, 'variants': {
                    'DEFAULT': [
                        {'subtitle': "Total Damage", 'type': "damage", 'multiplier': 600,
                         'conversion': [60, 0, 25, 0, 15, 0], 'summary': True},
                        {'subtitle': "Per Arrow (60)", 'type': "damage", 'multiplier': 10,
                         'conversion': [60, 0, 25, 0, 15, 0]}
                    ],
                    'HAWKEYE': [
                        {'subtitle': "Total Damage (Hawkeye)", 'type': "damage", 'multiplier': 400,
                         'conversion': [60, 0, 25, 0, 15, 0], 'summary': True},
                        {'subtitle': "Per Arrow (5)", 'type': "damage", 'multiplier': 80,
                         'conversion': [60, 0, 25, 0, 15, 0]}
                    ],
                }},
                {'title': "Escape", 'cost': 3, 'parts': [
                    {'subtitle': "Landing Damage", 'type': "damage", 'multiplier': 100,
                     'conversion': [50, 0, 0, 0, 0, 50], 'summary': True},
                ]},
                {'title': "Bomb Arrow", 'cost': 8, 'parts': [
                    {'subtitle': "Total Damage", 'type': "damage", 'multiplier': 250,
                     'conversion': [60, 25, 0, 0, 15, 0], 'summary': True},
                ]},
                {'title': "Arrow Shield", 'cost': 10, 'parts': [
                    {'subtitle': "Shield Damage", 'type': "damage", 'multiplier': '100',
                     'conversion': [70, 0, 0, 0, 0, 30], 'summary': True},
                    {'subtitle': "Arrow Rain Damage", 'type': "damage", 'multiplier': '200',
                     'conversion': [70, 0, 0, 0, 0, 30]},
                ]},
            ],
            "dagger": [
                {'title': "Spin Attack", 'cost': 6, 'parts': [
                    {'subtitle': "Total Damage", 'type': "damage", 'multiplier': 150,
                     'conversion': [70, 0, 30, 0, 0, 0], 'summary': True},
                ]},
                {'title': "Vanish", 'cost': 2, 'parts': [
                    {'subtitle': "No Damage", 'type': "none", 'summary': True}
                ]},
                {'title': "Multihit", 'cost': 8, 'parts': [
                    {'subtitle': "1st to 10th Hit", 'type': "damage", 'multiplier': 27,
                     'conversion': [100, 0, 0, 0, 0, 0]},
                    {'subtitle': "Fatality", 'type': "damage", 'multiplier': 120, 'conversion': [20, 0, 30, 50, 0, 0]},
                    {'subtitle': "Total Damage", 'type': "total", 'factors': [10, 1], 'summary': True},
                ]},
                {'title': "Smoke Bomb", 'cost': 8, 'variants': {
                    'DEFAULT': [
                        {'subtitle': "Tick Damage (10 max)", 'type': "damage", 'multiplier': 60,
                         'conversion': [50, 25, 0, 0, 0, 25]},
                        {'subtitle': "Total Damage", 'type': "damage", 'multiplier': 600,
                         'conversion': [50, 25, 0, 0, 0, 25], 'summary': True},
                    ],
                    'CHERRY_BOMBS': [
                        {'subtitle': "Total Damage (Cherry Bombs)", 'type': "damage", 'multiplier': 330,
                         'conversion': [50, 25, 0, 0, 0, 25], 'summary': True},
                        {'subtitle': "Per Bomb", 'type': "damage", 'multiplier': 110,
                         'conversion': [50, 25, 0, 0, 0, 25]}
                    ]
                }},
            ],
            "relik": [
                {'title': "Totem", 'cost': 4, 'parts': [
                    {'subtitle': "Smash Damage", 'type': "damage", 'multiplier': 100,
                     'conversion': [80, 0, 0, 0, 20, 0]},
                    {'subtitle': "Damage Tick", 'type': "damage", 'multiplier': 20, 'conversion': [80, 0, 0, 0, 0, 20]},
                    {'subtitle': "Heal Tick", 'type': "heal", 'strength': 0.03, 'summary': True},
                ]},
                {'title': "Haul", 'cost': 1, 'parts': [
                    {'subtitle': "Total Damage", 'type': "damage", 'multiplier': 100,
                     'conversion': [80, 0, 20, 0, 0, 0], 'summary': True},
                ]},
                {'title': "Aura", 'cost': 8, 'parts': [
                    {'subtitle': "One Wave", 'type': "damage", 'multiplier': 200, 'conversion': [70, 0, 0, 30, 0, 0],
                     'summary': True},
                ]},
                {'title': "Uproot", 'cost': 6, 'parts': [
                    {'subtitle': "Total Damage", 'type': "damage", 'multiplier': 100,
                     'conversion': [70, 30, 0, 0, 0, 0], 'summary': True},
                ]},
            ],
            "powder": [
                {'title': "Quake", 'cost': 0, 'parts': [
                    {'subtitle': "Total Damage", 'type': "damage", 'multiplier': [155, 220, 285, 350, 415],
                     'conversion': [0, 100, 0, 0, 0, 0], 'summary': True},
                ]},
                {'title': "Chain Lightning", 'cost': 0, 'parts': [
                    {'subtitle': "Total Damage", 'type': "damage", 'multiplier': [200, 225, 250, 275, 300],
                     'conversion': [0, 0, 100, 0, 0, 0], 'summary': True},
                ]},
                {'title': "Courage", 'cost': 0, 'parts': [
                    {'subtitle': "Total Damage", 'type': "damage", 'multiplier': [75, 87.5, 100, 112.5, 125],
                     'conversion': [0, 0, 0, 0, 100, 0], 'summary': True},
                ]},
            ]
        }

        self.POWDER_TABLE = {
            'e1': {'damage_min': 3, 'damage_max': 6, 'convert': 17, 'defense_inc': 2, 'defense_dec': ['a', 1]},
            'e2': {'damage_min': 6, 'damage_max': 9, 'convert': 21, 'defense_inc': 4, 'defense_dec': ['a', 2]},
            'e3': {'damage_min': 8, 'damage_max': 14, 'convert': 25, 'defense_inc': 8, 'defense_dec': ['a', 3]},
            'e4': {'damage_min': 11, 'damage_max': 16, 'convert': 31, 'defense_inc': 14, 'defense_dec': ['a', 5]},
            'e5': {'damage_min': 15, 'damage_max': 18, 'convert': 38, 'defense_inc': 22, 'defense_dec': ['a', 9]},
            'e6': {'damage_min': 18, 'damage_max': 22, 'convert': 46, 'defense_inc': 30, 'defense_dec': ['a', 13]},

            't1': {'damage_min': 1, 'damage_max': 8, 'convert': 9, 'defense_inc': 3, 'defense_dec': ['e', 1]},
            't2': {'damage_min': 1, 'damage_max': 13, 'convert': 11, 'defense_inc': 5, 'defense_dec': ['e', 1]},
            't3': {'damage_min': 2, 'damage_max': 18, 'convert': 13, 'defense_inc': 9, 'defense_dec': ['e', 2]},
            't4': {'damage_min': 3, 'damage_max': 24, 'convert': 17, 'defense_inc': 14, 'defense_dec': ['e', 4]},
            't5': {'damage_min': 3, 'damage_max': 32, 'convert': 22, 'defense_inc': 20, 'defense_dec': ['e', 7]},
            't6': {'damage_min': 5, 'damage_max': 40, 'convert': 28, 'defense_inc': 28, 'defense_dec': ['e', 10]},

            'w1': {'damage_min': 3, 'damage_max': 4, 'convert': 13, 'defense_inc': 3, 'defense_dec': ['t', 1]},
            'w2': {'damage_min': 4, 'damage_max': 7, 'convert': 15, 'defense_inc': 6, 'defense_dec': ['t', 1]},
            'w3': {'damage_min': 6, 'damage_max': 10, 'convert': 17, 'defense_inc': 11, 'defense_dec': ['t', 2]},
            'w4': {'damage_min': 8, 'damage_max': 12, 'convert': 21, 'defense_inc': 18, 'defense_dec': ['t', 4]},
            'w5': {'damage_min': 11, 'damage_max': 14, 'convert': 26, 'defense_inc': 28, 'defense_dec': ['t', 7]},
            'w6': {'damage_min': 13, 'damage_max': 17, 'convert': 32, 'defense_inc': 40, 'defense_dec': ['t', 10]},

            'f1': {'damage_min': 2, 'damage_max': 5, 'convert': 14, 'defense_inc': 3, 'defense_dec': ['w', 1]},
            'f2': {'damage_min': 4, 'damage_max': 8, 'convert': 16, 'defense_inc': 5, 'defense_dec': ['w', 2]},
            'f3': {'damage_min': 6, 'damage_max': 10, 'convert': 19, 'defense_inc': 9, 'defense_dec': ['w', 3]},
            'f4': {'damage_min': 9, 'damage_max': 13, 'convert': 24, 'defense_inc': 16, 'defense_dec': ['w', 5]},
            'f5': {'damage_min': 12, 'damage_max': 16, 'convert': 30, 'defense_inc': 25, 'defense_dec': ['w', 9]},
            'f6': {'damage_min': 15, 'damage_max': 19, 'convert': 37, 'defense_inc': 36, 'defense_dec': ['w', 13]},

            'a1': {'damage_min': 2, 'damage_max': 6, 'convert': 11, 'defense_inc': 3, 'defense_dec': ['f', 1]},
            'a2': {'damage_min': 4, 'damage_max': 9, 'convert': 14, 'defense_inc': 6, 'defense_dec': ['f', 2]},
            'a3': {'damage_min': 7, 'damage_max': 10, 'convert': 17, 'defense_inc': 10, 'defense_dec': ['f', 3]},
            'a4': {'damage_min': 9, 'damage_max': 13, 'convert': 22, 'defense_inc': 16, 'defense_dec': ['f', 5]},
            'a5': {'damage_min': 13, 'damage_max': 17, 'convert': 28, 'defense_inc': 24, 'defense_dec': ['f', 9]},
            'a6': {'damage_min': 16, 'damage_max': 18, 'convert': 35, 'defense_inc': 34, 'defense_dec': ['f', 13]},
        }

    def readitem(self, query=None, powders=None, level=106):
        # Get items from DB
        if powders is None:
            powders = {}
        if query is None:
            query = []

        setcount, uniqueset = ([] for i in range(2))

        self.sets, self.setbonus = ({} for i in range(2))

        netelemdefs = {'e': 0, 't': 0, 'w': 0, 'f': 0, 'a': 0}

        for k, v in self.equipments.items():
            self.equipments[k] = None
        for k, v in self.rawstats.items():
            self.rawstats[k] = 0

        for keyword in query:
            for item in self.db['items']:
                if keyword == item['name']:
                    if 'ring' in item['type'] and not self.equipments['ring1']:
                        self.equipments['ring1'] = item
                    elif 'ring' in item['type']:
                        self.equipments['ring2'] = item
                    elif 'weapon' in item['category']:
                        self.equipments['weapon'] = item
                    else:
                        self.equipments[item['type']] = item
                    if 'set' in item:
                        setcount.append(item['set'])

        # Determining sets
        uniqueset = [x for x in setcount if x not in uniqueset]
        if uniqueset:
            for i in uniqueset:
                self.sets[i] = setcount.count(i)
            for setname, count in self.sets.items():
                # print(setname)
                # print(setdata[setname]['bonuses'][count - 1])
                self.setbonus[setname] = self.db['sets'][setname]['bonuses']
                for k in self.rawstats.keys():
                    if k in self.setbonus[setname][count - 1]:
                        self.rawstats[k] = self.setbonus[setname][count - 1][k]

        print(f'ACTIVE SET {self.sets}')
        print(self.setbonus)

        # Calculating total stats w/ max rolls for each item
        for item in self.equipments.values():
            if item:
                # parsing armor powders
                print(item)
                print('item found, adding')
                for k, v in self.rawstats.items():
                    if k in item:
                        if k in self.WEAPONDAMAGE:
                            self.rawstats[k] = item[k]
                        elif k in self.UNROLLABLES or 'fixID' in item:
                            self.rawstats[k] += item[k]
                        elif k in self.SPELLCOSTSPCT:
                            self.rawstats[k] += round_tonoteven(item[k] * 1.3)
                        elif k in self.SPELLCOSTSRAW:
                            self.rawstats[k] += round_tonoteven(item[k] * 1.3)
                        elif item[k] < 0:
                            self.rawstats[k] += round_tonoteven(item[k] * 0.7)
                        else:
                            self.rawstats[k] += round_tonoteven(item[k] * 1.3)

        for itemtype, powdering in powders.items():
            if 'weapon' in itemtype:
                continue
            else:
                parsedpowders = powderparse(powdering)
                powdercount = dict(Counter(parsedpowders))
                for powdertype, count in powdercount.items():
                    netelemdefs[powdertype[0]] += self.POWDER_TABLE[powdertype]['defense_inc'] * count
                    netelemdefs[self.POWDER_TABLE[powdertype]['defense_dec'][0]] -= \
                        self.POWDER_TABLE[powdertype]['defense_dec'][1] * count

        for eledefs in self.ELEMENTALDEF:
            self.rawstats[eledefs] += netelemdefs[eledefs[0]]

        print(self.rawstats)
        # actually making total stats using hpb, hpr% and eledef%
        self.totalstats = self.rawstats
        self.totalstats['totalhp'] = self.totalstats['hp'] + self.totalstats['hpBonus'] + level_tobasehp(level)
        self.totalstats['totalhprRaw'] = round(self.totalstats['hprRaw'] * ((self.totalstats['hprPct'] / 100) + 1))
        self.totalstats['totalaDef'] = round(self.totalstats['aDef'] * ((self.totalstats['aDefPct'] / 100) + 1))
        self.totalstats['totalfDef'] = round(self.totalstats['fDef'] * ((self.totalstats['fDefPct'] / 100) + 1))
        self.totalstats['totalwDef'] = round(self.totalstats['wDef'] * ((self.totalstats['wDefPct'] / 100) + 1))
        self.totalstats['totaltDef'] = round(self.totalstats['tDef'] * ((self.totalstats['tDefPct'] / 100) + 1))
        self.totalstats['totaleDef'] = round(self.totalstats['eDef'] * ((self.totalstats['eDefPct'] / 100) + 1))
        self.totalstats['activeSet'] = self.sets

        self.solveskillpoints()

    def solveskillpoints(self):
        # Skillpoints Calculation

        # define vars
        # ALLREQS: dict contains [type of item : [[sp requirements], [bonus sp]]
        allreqs, itemset = ({} for i in range(2))
        # noreqsp contains all bonus sp from no req pieces
        # weapon sp dont count towards reqs
        noreqsp, weaponsp, bestsp = (np.array([0, 0, 0, 0, 0]) for i in range(3))
        # bestsp and bestreq holds... best sp and best reqs respectively
        bestreq = None
        # equiporder holds the final equip order
        equiporder = []

        # cycle thru and place equipment type/req, sp in a dict (allreqs)
        for slot, item in self.equipments.items():
            if item is not None:
                itemreq = np.array([item['strReq'], item['dexReq'], item['intReq'], item['defReq'], item['agiReq']])
                itemsp = np.array([item['str'], item['dex'], item['int'], item['def'], item['agi']])
                netsp = np.array(
                    [itemreq[0] - itemsp[0], itemreq[1] - itemsp[1], itemreq[2] - itemsp[2], itemreq[3] - itemsp[3],
                     itemreq[4] - itemsp[4]])

                if 'weapon' in slot:
                    weaponsp = itemsp
                    itemsp = np.array([0, 0, 0, 0, 0])
                    self.currentclass = self.WEAPONTOCLASS[item['type']]
                if 'set' in item:
                    itemset[slot] = item['set']

                    # print(itemset)
                if sum(itemreq) == 0 and not sum(itemsp) < 0:
                    for i in range(5):
                        noreqsp[i] += itemsp[i]
                    equiporder.append(slot)
                    continue
            else:
                continue
            allreqs[slot] = [itemreq, itemsp, netsp]

        # print(f'All item for permute: {allreqs}')
        # algorithm optimization

        # sort by net sp
        netsp_sort = np.sort(
            np.array([sum(allreqs[itemtype][2]) for itemtype in allreqs.keys() if 'weapon' not in itemtype],
                     dtype='object'))
        if 'weapon' in allreqs:
            netsp_sort = np.append(netsp_sort, sum(allreqs['weapon'][2]))

        for itemtype, skp in allreqs.items():
            for i in range(len(netsp_sort)):
                if sum(skp[2]) == netsp_sort[i]:
                    netsp_sort[i] = itemtype

        # permutation take 3
        # create permute
        buildpermute = np.array(list(permutations(netsp_sort)))

        for possibleorder in buildpermute:
            # print('NEW ATTEMPT')
            # refreshing vars each run
            assigned = np.array([0, 0, 0, 0, 0])

            total, skillpoints, max_min_req = (np.copy(noreqsp) for i in range(3))

            itemsetcount, itemsetsp = ({} for i in range(2))

            equipattempt = []
            equipattempt.extend(equiporder)

            for itemtype in possibleorder:
                if itemtype in itemset:
                    # print('this item is in a set')

                    if itemset[itemtype] not in itemsetcount:
                        # print('set currently not exist, creating')
                        itemsetcount[itemset[itemtype]] = 0
                        itemsetsp[itemset[itemtype]] = [0, 0, 0, 0, 0]

                    # MAKE THIS LOOK BETTER, somehow... (partially better)

                    for bonustype, bonusamount in self.setbonus[itemset[itemtype]][
                        itemsetcount[itemset[itemtype]]].items():
                        if bonustype in self.SKILLPOINTS:
                            skillpoints[self.SKILLPOINTS.index(bonustype)] -= \
                                itemsetsp[itemset[itemtype]][self.SKILLPOINTS.index(bonustype)]

                            itemsetsp[itemset[itemtype]][self.SKILLPOINTS.index(bonustype)] += \
                                abs(itemsetsp[itemset[itemtype]][self.SKILLPOINTS.index(bonustype)] - bonusamount)

                            skillpoints[self.SKILLPOINTS.index(bonustype)] += \
                                itemsetsp[itemset[itemtype]][self.SKILLPOINTS.index(bonustype)]

                    itemsetcount[itemset[itemtype]] += 1

                    # print(f'SP FROM SET {itemsetsp}')

                for i in range(5):

                    # if current total sp is lower than req
                    if total[i] < allreqs[itemtype][0][i]:
                        # blame self feeding scenario
                        if total[i] >= 0:
                            assigned[i] += abs(total[i] - allreqs[itemtype][0][i])
                        # blame negative sp scenario
                        else:
                            assigned[i] += abs(assigned[i] - allreqs[itemtype][0][i])
                        total[i] = assigned[i]

                    # set all bonus sp (incl pos and negs) into the var
                    skillpoints[i] += allreqs[itemtype][1][i]
                    # calculate total with assigned + bonus
                    total[i] = assigned[i] + skillpoints[i]

                    # get the minimum reqs required for wearing (max item req + item sp)
                    max_min_req[i] = max(max_min_req[i], allreqs[itemtype][0][i] + allreqs[itemtype][1][i])

                    # max_min_req = 0 meaning it does not count to reqs
                    # the other one is blame 0 sp assigned scenario
                    if max_min_req[i] == 0 or (assigned[i] == 0 and total[i] == 0):
                        pass
                    # compensate sp if the total is lower than the minimum needed to wear
                    elif total[i] < max_min_req[i]:
                        assigned[i] += abs(total[i] - max_min_req[i])
                        total[i] += abs(total[i] - max_min_req[i])
                        # print('----\nreassigning\n----\n')

                    # add weapon sp to final

                    # print(f'ASSIGNED: {assigned}')
                    # print(f'TOTAL: {total}')
                    # print(f'SKILLPOINTS: {skillpoints}')
                    # print(f'MAX MIN REQ: {max_min_req}\n\n')

                # if current assigned sp is larger than best, drop a run
                # print(f'EQUIP ORDER: {equipattempt}')
                if bestreq is not None and sum(assigned) > sum(bestreq):
                    # print(f'\nABORTING\n')
                    break

                # get best results
                equipattempt.append(itemtype)

            if bestreq is None or sum(assigned) < sum(bestreq):
                bestreq = assigned
                bestsp = total
                for i in range(5):
                    if 'weapon' in itemtype:
                        bestsp[i] += weaponsp[i]
                    self.assignedSP[self.SKILLPOINTS[i]] = bestsp[0]
                self.wearorder = equipattempt

        for i in range(5):
            self.totalstats[self.SKILLPOINTS[i]] = bestsp[i]
            self.totalstats[f'{self.SKILLPOINTS[i]}assign'] = bestreq[i]

        print(f'FINAL RESULT: \nBEST REQS: {bestreq}\nTOTAL SP: {bestsp}\nWEAR ORDER: {self.wearorder}')

        # print(self.setbonus)

        self.damagecalculation()

    def damagecalculation(self):
        if self.equipments['weapon']:
            # weaponbasedamage = {min: {type: amount}, max: {type: amount}}
            weaponbasedamage = {
                'min': {'nDam': 0, 'eDam': 0, 'tDam': 0, 'wDam': 0, 'fDam': 0, 'aDam': 0},
                'max': {'nDam': 0, 'eDam': 0, 'tDam': 0, 'wDam': 0, 'fDam': 0, 'aDam': 0}
            }

            for k, v in self.equipments['weapon'].items():
                if k in self.WEAPONDAMAGE:
                    weaponbasedamage['min'][k] = int(v[0:v.index('-')])
                    weaponbasedamage['max'][k] = int(v[v.index('-') + 1:])

            print(f'WEAPON BASE: {weaponbasedamage}')

        else:
            return None


builder = Builder()
