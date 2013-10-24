__version__ = '2.0'
__author__  = 'LouK' #

import b3, time, threading
import b3.events
import b3.plugin
import shutil
import os  
    
class BotstartPlugin(b3.plugin.Plugin):
    requiresConfigFile = False
    time_kikcbots = 13
    
    def onStartup(self):
        self.registerEvent(b3.events.EVT_GAME_ROUND_START)
        self._adminPlugin = self.console.getPlugin('admin')
        self._randommapPlugin = self.console.getPlugin('randommapurt_guns')
        self.query = self.console.storage.query
     
        if not self._adminPlugin:
            self.error('No se pudo encontrar el plugin en Admin')
            return
        
        self._adminPlugin.registerCommand(self, 'kickbots', 40, self.cmd_kickbots, 'kbots')
        self._adminPlugin.registerCommand(self, 'addbots', 40, self.cmd_addbots, 'abots')
    
    def onEvent(self, event):
        if event.type == b3.events.EVT_GAME_ROUND_START:
            self.addBots(event)
            self.addMaps(event)
            
    def addBots(self, event):
        cursor = self.console.storage.query('SELECT swap_num FROM `bots` WHERE `id` = "1"')
        r = cursor.getRow()
        swap_num = r['swap_num']
        if swap_num==1:
            clients = self.console.clients.getList()
            gametype = self.console.getCvar('g_gametype').getInt()
            if gametype==0:
                self.console.write("kick allbots")
                self.console.write('bot_minplayers "0"')
                time.sleep(6)
                if len(clients)>=6:
                    self.console.write('bot_minplayers "0"')
                else:
                    self.console.write("exec botsFFA.cfg")
            elif gametype==3:
                self.console.write('bot_minplayers "8"')
                
    def addMaps(self, event):
        nextmap = self.console.getNextMap()
        mapname = self.console.getCvar('mapname').getString()
        if (mapname == "ut4_sanc"):
            os.remove('/var/urt/guns/q3ut4/ut4_arena1.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_arena2.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_aztec_b3.pk3')
            os.remove('/var/urt/guns/q3ut4/chronic.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_dreary_b6.pk3')
            os.remove('/var/urt/guns/q3ut4/CubeLaser03.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_dust2_v2.pk3')
            os.remove('/var/urt/guns/q3ut4/Cube02.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_ricochet.pk3')
            os.remove('/var/urt/guns/q3ut4/ut_streets3-daybeta3.pk3')
            os.remove('/var/urt/guns/q3ut4/cube_hell_ff_b2.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_commune.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_greatwall_beta5.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_littletown3.pk3')
            os.remove('/var/urt/guns/q3ut4/ut_forrest.pk3')
            os.remove('/var/urt/guns/q3ut4/ut_hamunaptra.pk3')
            os.remove('/var/urt/guns/q3ut4/cube07.pk3')
            os.remove('/var/urt/guns/q3ut4/cube08.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_village_classic_rc4.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_exhibition_a24.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_monopoly_beta2.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_rctf12.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_rctf4.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_nin.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_arena7.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_cambridge_fixed.pk3')
            os.remove('/var/urt/guns/q3ut4/ut4_orbital_sl.pk3')
            os.remove('/var/urt/guns/q3ut4/mapcycle2.txt')
            self.console.write("bot_enable 1")
            self.console.write("g_mapcycle mapcycle.txt")
            self.console.write("map ut4_abbey")
            self.console.storage.query('UPDATE `bots` SET swap_num="1" WHERE `id` = "1"')
            self.console.write("g_nextmap ut4_austria")
            self.console.write("g_gametype 0")
            self._randommapPlugin._rmonoff = "off"
            return False
        elif (mapname == "ut4_prague"):
            shutil.copy('/var/urt/Guns/q3ut4/ut4_arena1.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_arena2.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_aztec_b3.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/chronic.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_dreary_b6.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/CubeLaser03.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_dust2_v2.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/Cube02.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_ricochet.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut_streets3-daybeta3.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/cube_hell_ff_b2.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_commune.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_greatwall_beta5.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_littletown3.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut_forrest.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut_hamunaptra.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/cube07.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/cube08.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_village_classic_rc4.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_exhibition_a24.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_monopoly_beta2.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_rctf12.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_rctf4.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_nin.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_arena7.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_cambridge_fixed.pk3', '/var/urt/guns/q3ut4')
            shutil.copy('/var/urt/Guns/q3ut4/ut4_orbital_sl.pk3', '/var/urt/guns/q3ut4')
            shutil.copyfile('/var/urt/Guns/q3ut4/mapcycle.txt', '/var/urt/guns/q3ut4/mapcycle2.txt')
            self.console.write("bot_enable 0")
            self.console.write("map ut4_turnpike")
            self.console.write("g_mapcycle mapcycle2.txt")
            self.console.storage.query('UPDATE `bots` SET swap_num="2" WHERE `id` = "1"')
            self._randommapPlugin._rmonoff = "on"
            return False
        else:
            self.console.say("Nextmap: ^2%s" % nextmap)
            mapcycle = self.console.getCvar('g_mapcycle').getString()
            if mapcycle == "mapcycle2.txt":
                self.console.write("bot_enable 0")
            else:
                self.console.write("bot_enable 1")
            return True
            
            
    def cmd_kickbots(self, data, client, cmd=None):
        """\
        kick all bots in the server
        """
        input = self._adminPlugin.parseUserCmd(data)
        
        if not input:
            self.console.storage.query('UPDATE `bots` SET swap_num="1" WHERE `id` = "1"')
            self.console.write("kick allbots")
            self.console.write('bot_minplayers "0"')
            client.message('^7You ^1kicked ^7all bots in the server.')
            return True

        if input[0] == 'perm' or input[0] == 'permanent' or input[0] == 'foreva' or input[0] == 'lock':
            self.console.storage.query('UPDATE `bots` SET swap_num="2" WHERE `id` = "1"')
            self.console.write("kick allbots")
            self.console.write('bot_minplayers "0"')
            client.message('^7You ^1kicked ^7all bots in the server and they wont be added each map.')
            
        elif input[0] == 'maps' or input[0] == 'disable' or input[0] == 'addmaps':
            if (client.maxLevel >= 80):
                self.console.storage.query('UPDATE `bots` SET swap_num="2" WHERE `id` = "1"')
                self.console.write("kick allbots")
                self.console.write("g_gametype 3")
                self.console.write('bot_minplayers "0"')
                self.console.write("g_nextmap ut4_prague")
                client.message('^7You ^1kicked ^7all bots in the server and added custom maps(maps will be added after turnpike).')
            else:
                client.message('^7Hmm I think you are not Vega or LouK..')
        
    def cmd_addbots(self, data, client, cmd=None):
        """\
        Add bots to the server
        """
        input = self._adminPlugin.parseUserCmd(data)
        
        if not input:
            gametype = self.console.getCvar('g_gametype').getInt()
            self.console.storage.query('UPDATE `bots` SET swap_num="1" WHERE `id` = "1"')
            client.message('^7Bots ^2added^7')
            if gametype==0:
                self.console.write("exec botsFFA.cfg")
            elif gametype==3:
                self.console.write('bot_minplayers "8"')
                return True
        elif input[0] == 'perm' or input[0] == 'enable' or input[0] == 'remmaps':
            if (client.maxLevel >= 80):
                self.console.storage.query('UPDATE `bots` SET swap_num="1" WHERE `id` = "1"')
                self.console.write('bot_enable 1')
                self.console.write("g_nextmap ut4_sanc")
                self.console.write("g_gametype 3")
                client.message('^7Bots ^2added^7 permanently(will be added at map change)')
            else:
                client.message('^7Hmm I think you are not Vega or LouK..')
