from builder import builder
import sys
from PyQt5 import QtWidgets, uic

# TODO:
# 1. Make stats config overview (Partially done, missing the effective x stuff)
# 2. PERMUTATION: solve least sp to use a build (holy shit finally done?? yep its done)
# 3. Damage Calculation !! LAST BECAUSE DEPENDANT !! (in progress)
# 4. Actually verify that everything is correct lol
# 5. Ask for testers
# 6. THEN move onto build synthesis
# 7. Actually verify that it is good
# 8. Ask for testers part 2: electric boogaloo
# 9. ???
# 10. Profit, or so.


class Application(QtWidgets.QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        self.window = uic.loadUi('mainwindow.ui', self)

        self.CLASSTOCBOXINDEX = {'Archer': 0, 'Mage': 1, 'Shaman': 2, 'Warrior': 3, 'Assassin': 4}

        for items in builder.db['items']:
            if 'displayName' in items:
                items['name'] = items['displayName']
            if 'type' in items:
                if 'helmet' in items['type']:
                    self.window.cbox_helmet.addItem(items['name'])
                elif 'chestplate' in items['type']:
                    self.window.cbox_chestplate.addItem(items['name'])
                elif 'leggings' in items['type']:
                    self.window.cbox_leggings.addItem(items['name'])
                elif 'boots' in items['type']:
                    self.window.cbox_boots.addItem(items['name'])
                elif 'ring' in items['type']:
                    self.window.cbox_ring1.addItem(items['name'])
                    self.window.cbox_ring2.addItem(items['name'])
                elif 'bracelet' in items['type']:
                    self.window.cbox_bracelet.addItem(items['name'])
                elif 'necklace' in items['type']:
                    self.window.cbox_necklace.addItem(items['name'])
                elif 'weapon' in items['category']:
                    self.window.cbox_weapon.addItem(items['name'])

        self.window.btn_calc.clicked.connect(lambda: self.calculatebuild())

        self.show()

    def calculatebuild(self):
        query = [self.window.cbox_helmet.currentText(),
                 self.window.cbox_chestplate.currentText(),
                 self.window.cbox_leggings.currentText(),
                 self.window.cbox_boots.currentText(),
                 self.window.cbox_ring1.currentText(),
                 self.window.cbox_ring2.currentText(),
                 self.window.cbox_bracelet.currentText(),
                 self.window.cbox_necklace.currentText(),
                 self.window.cbox_weapon.currentText()]

        powders = {
            'helmet': self.window.input_powder_helmet.text(),
            'chestplate': self.window.input_powder_chestplate.text(),
            'leggings': self.window.input_powder_leggings.text(),
            'boots': self.window.input_powder_boots.text(),
            'weapon': self.window.input_powder_weapon.text()
        }

        level = self.window.spin_level.value()

        # Overview
        builder.readitem(query, powders, level)
        self.window.spin_total_hp.setValue(builder.totalstats['totalhp'])
        # add effective HP
        # add effective HP w/o Agi

        self.window.spin_hpr.setValue(builder.totalstats['totalhprRaw'])
        activeSet = ''
        if builder.totalstats['activeSet']:
            for setname, count in builder.totalstats['activeSet'].items():
                activeSet += f'{setname}: {count} | '
                print(activeSet)

        self.window.label_activeSet.setText(activeSet)
        # total :eledefs:
        self.window.spin_total_edef.setValue(builder.totalstats['totaleDef'])
        self.window.spin_total_tdef.setValue(builder.totalstats['totaltDef'])
        self.window.spin_total_wdef.setValue(builder.totalstats['totalwDef'])
        self.window.spin_total_fdef.setValue(builder.totalstats['totalfDef'])
        self.window.spin_total_adef.setValue(builder.totalstats['totalaDef'])

        # SP
        self.window.spin_sp_str.setValue(builder.totalstats['str'])
        self.window.spin_sp_dex.setValue(builder.totalstats['dex'])
        self.window.spin_sp_int.setValue(builder.totalstats['int'])
        self.window.spin_sp_def.setValue(builder.totalstats['def'])
        self.window.spin_sp_agi.setValue(builder.totalstats['agi'])

        # ElemDmg%
        self.window.spin_elemdmg_earth.setValue(builder.totalstats['eDamPct'])
        self.window.spin_elemdmg_thunder.setValue(builder.totalstats['tDamPct'])
        self.window.spin_elemdmg_water.setValue(builder.totalstats['wDamPct'])
        self.window.spin_elemdmg_fire.setValue(builder.totalstats['fDamPct'])
        self.window.spin_elemdmg_air.setValue(builder.totalstats['aDamPct'])

        # Neutral others
        self.window.spin_neutral_spellperc.setValue(builder.totalstats['sdPct'])
        self.window.spin_neutral_spellraw.setValue(builder.totalstats['sdRaw'])
        self.window.spin_neutral_meleeperc.setValue(builder.totalstats['mdPct'])
        self.window.spin_neutral_meleeraw.setValue(builder.totalstats['mdRaw'])

        # Mana/spellcost
        self.window.spin_mana_regen.setValue(builder.totalstats['mr'])
        self.window.spin_mana_steal.setValue(builder.totalstats['ms'])

        self.window.spin_1st_raw.setValue(builder.totalstats['spRaw1'])
        self.window.spin_1st_perc.setValue(builder.totalstats['spPct1'])

        self.window.spin_2nd_raw.setValue(builder.totalstats['spRaw2'])
        self.window.spin_2nd_perc.setValue(builder.totalstats['spPct2'])

        self.window.spin_3rd_raw.setValue(builder.totalstats['spRaw3'])
        self.window.spin_3rd_perc.setValue(builder.totalstats['spPct3'])

        self.window.spin_4th_raw.setValue(builder.totalstats['spRaw4'])
        self.window.spin_4th_perc.setValue(builder.totalstats['spPct4'])

        # HP-related Defensive stats
        self.window.spin_health_regen.setValue(builder.totalstats['hprRaw'])
        self.window.spin_health_regenperc.setValue(builder.totalstats['hprPct'])
        self.window.spin_health_bonus.setValue(builder.totalstats['hpBonus'])
        self.window.spin_health_steal.setValue(builder.totalstats['ls'])

        # :eledefs:
        self.window.spin_elemdef_earth.setValue(builder.totalstats['eDefPct'])
        self.window.spin_elemdef_thunder.setValue(builder.totalstats['tDefPct'])
        self.window.spin_elemdef_water.setValue(builder.totalstats['wDefPct'])
        self.window.spin_elemdef_fire.setValue(builder.totalstats['fDefPct'])
        self.window.spin_elemdef_air.setValue(builder.totalstats['aDefPct'])

        # movement
        self.window.spin_move_ws.setValue(builder.totalstats['ws'])
        self.window.spin_move_jh.setValue(builder.totalstats['jh'])
        self.window.spin_move_sprint.setValue(builder.totalstats['sprint'])
        self.window.spin_move_sprintregen.setValue(builder.totalstats['sprintReg'])

        # thorn/ref/expd
        self.window.spin_util_thorns.setValue(builder.totalstats['thorns'])
        self.window.spin_util_ref.setValue(builder.totalstats['ref'])
        self.window.spin_util_expd.setValue(builder.totalstats['expd'])

        # other util
        self.window.spin_other_lb.setValue(builder.totalstats['lb'])
        self.window.spin_other_xpb.setValue(builder.totalstats['xpb'])
        self.window.spin_other_spr.setValue(builder.totalstats['spRegen'])

        # equip order
        order = ''
        for i in range(len(builder.wearorder)):
            order += f'{builder.wearorder[i]}\n'
        self.window.label_equiporder.setText(order)

        # skill points assignment
        self.window.cbox_class.setCurrentIndex(self.CLASSTOCBOXINDEX[builder.currentclass])

        self.window.spin_req_str.setValue(builder.totalstats['strassign'])
        self.window.spin_req_dex.setValue(builder.totalstats['dexassign'])
        self.window.spin_req_int.setValue(builder.totalstats['intassign'])
        self.window.spin_req_def.setValue(builder.totalstats['defassign'])
        self.window.spin_req_agi.setValue(builder.totalstats['agiassign'])


app = QtWidgets.QApplication(sys.argv)
GUI = Application()
sys.exit(app.exec_())
