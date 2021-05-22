from builder import builder
import time

builder.readitem(['Cumulonimbus'])

if sum(builder.assignedSP.values()) == 90:
    print('passed normal SP calc')
else:
    print('failed normal SP calc')

start = time.time()
builder.readitem(['Morph-Stardust', 'Morph-Steel', 'Morph-Iron', 'Morph-Gold',
                  'Morph-Topaz', 'Morph-Emerald', 'Morph-Amethyst', 'Morph-Ruby'])
end = time.time()
if sum(builder.bonusSP) == 375:
    print('passed morph (set sp) test')
    print(f'Elapsed time: {end - start}')
else:
    print('failed morph (set sp) test')

builder.readitem(['', '', 'Elder Oak Roots', 'Dragon Dance'])
