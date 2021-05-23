from builder import builder
from builder2 import builder as builder2
import time

start = time.time()
builder.readitem(['Cancer֎', 'Boreal-Patterned Aegis', 'Cinderchain', 'Curador Boots', 'Yang', 'Diamond Hydro Ring', 'Diamond Hydro Bracelet', 'Tenuto', 'Black'])
end = time.time()
print(f'---------\n\nLoad time of cryoseism with hpp algo: {(end - start)}')

start = time.time()
builder2.readitem(['Cancer֎', 'Boreal-Patterned Aegis', 'Cinderchain', 'Curador Boots', 'Yang', 'Diamond Hydro Ring', 'Diamond Hydro Bracelet', 'Tenuto', 'Black'])
end = time.time()
print(f'---------\n\nLoad time of cryoseism with old algo: {(end - start)}')

builder.readitem(['Cumulonimbus'])

if sum(builder.assignedSP.values()) == 90:
    print('--------\n\npassed normal SP calc\n\n---------')
else:
    print('failed normal SP calc')

start = time.time()
builder.readitem(['Morph-Stardust', 'Morph-Steel', 'Morph-Iron', 'Morph-Gold',
                  'Morph-Topaz', 'Morph-Emerald', 'Morph-Amethyst', 'Morph-Ruby'])
end = time.time()
if sum(builder.bonusSP) == 375:
    print('--------\npassed morph (set sp) test')
    print(f'Elapsed time: {end - start}\n-----------')
else:
    print('failed morph (set sp) test')

builder.readitem(['', '', 'Elder Oak Roots', 'Paradox'])
if sum(builder.assignedSP.values()) == 319:
    print('---------\n\npassed negative SP/SP bug test 1\n\n----------')
else:
    print('failed negative SP/SP bug test 1')

builder.readitem(['Sparkweaver', 'Narima Pasukan', '', 'The Oppressors'])
if sum(builder.assignedSP.values()) == 91:
    print('---------\n\npassed negative SP/SP bug test 2\n\n----------')
else:
    print('failed negative SP/SP bug test 2')

builder.readitem(['', '', 'Hephaestus-Forged Greaves', 'Moontower'])
if sum(builder.assignedSP.values()) == 230:
    print('---------\n\npassed negative SP/SP bug test 3\n\n----------')
else:
    print('failed negative SP/SP bug test 3')

start = time.time()
builder.readitem(['Corsair', 'Golden Scarab', 'Demon Tide', 'Hephaestus-Forged Sabatons', 'Yang', 'Diamond Static Ring', 'Diamond Static Bracelet', 'Tenuto', 'Cataclysm'])
builder.readitem(['Brainwash', 'Sparkling Plate', 'Stalactite', 'Flashing Boots', 'Moon Pool Circlet', 'Diamond Fiber Ring', 'Momentum', 'Tenuto', 'Grandmother'])
builder.readitem(['Albacore', 'Insulated Plate Mail', 'Demon Tide', 'Paradox', 'Cold Wave', 'Yang', "Dragon's Eye Bracelet", 'Diamond Hydro Necklace', 'Pure'])
builder.readitem(['Cumulonimbus', 'Medeis', 'Adrenaline', 'Paradox', 'Yang', 'Yang', 'Diamond Hydro Bracelet', 'Tenuto', 'Cryoseism'])
builder.readitem(['Breakdown', 'Far Cosmos', 'Anxiolytic', 'Slayer', 'Diamond Hydro Ring', 'Diamond Solar Ring', 'Euouae', 'Tenuto', 'Az'])
end = time.time()
print(f'---------\n\nLoad time of 5 builds (average) with hpp algo: {(end - start) / 5}')

start = time.time()
builder2.readitem(['Corsair', 'Golden Scarab', 'Demon Tide', 'Hephaestus-Forged Sabatons', 'Yang', 'Diamond Static Ring', 'Diamond Static Bracelet', 'Tenuto', 'Cataclysm'])
builder2.readitem(['Brainwash', 'Sparkling Plate', 'Stalactite', 'Flashing Boots', 'Moon Pool Circlet', 'Diamond Fiber Ring', 'Momentum', 'Tenuto', 'Grandmother'])
builder2.readitem(['Albacore', 'Insulated Plate Mail', 'Demon Tide', 'Paradox', 'Cold Wave', 'Yang', "Dragon's Eye Bracelet", 'Diamond Hydro Necklace', 'Pure'])
builder2.readitem(['Cumulonimbus', 'Medeis', 'Adrenaline', 'Paradox', 'Yang', 'Yang', 'Diamond Hydro Bracelet', 'Tenuto', 'Cryoseism'])
builder2.readitem(['Breakdown', 'Far Cosmos', 'Anxiolytic', 'Slayer', 'Diamond Hydro Ring', 'Diamond Solar Ring', 'Euouae', 'Tenuto', 'Az'])
end = time.time()
print(f'---------\n\nLoad time of 5 builds (average) with original algo: {(end - start) / 5}')


