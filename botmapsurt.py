__version__ = '3.0'
__author__  = 'LouK' #

import b3, time, threading
import b3.events
import b3.plugin
import shutil
import os
    
class BotmapsurtPlugin(b3.plugin.Plugin):
    _botmaps = {}
    _clients = []
    _addmapsmap = "ut4_sanc"
    _remmapsmap = "ut4_prague"
    _botstart = True
    _botminplayers = 6
    _neededplayers = 6
    _clients = 0
    _time_addbotsFFA = 10
    
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
            
    def onLoadConfig(self):
        self.loadBotstuff()
        
    def loadBotstuff(self):
        try:
            self._botminplayers = self.config.getint('settings', 'bot_minplayers')
            if self._botminplayers > 16:
                self._botminplayers = 16
            elif self._botminplayers < 0:
                self._botminplayers = 0
        except:
            self._botminplayers = 4
            self.debug('Using default value (%s) for bot minimum players', self._botminplayers)
        try:
            botmaps = self.config.get('settings', 'botmaps')
            botmaps = maps.split(', ')
            self._botmaps = botmaps
        except:
            self._botmaps = {}
        try:
            self._time_addbotsFFA = self.config.getint('settings', 'add_bots_FFA')
        except:
            self._time_addbotsFFA = 10
        try:
            self._neededplayers = self.config.getint('settings', 'needed_players')
        except:
            self._neededplayers = 6
        try:
            self._neededplayers = self.config.getint('settings', 'needed_players')
        except:
            self._neededplayers = 6
        try:
            self._neededplayers = self.config.getint('settings', 'needed_players')
        except:
            self._neededplayers = 6
        try:
            self._neededplayers = self.config.getint('settings', 'needed_players')
        except:
            self._neededplayers = 6
        try:
            self._neededplayers = self.config.getint('settings', 'needed_players')
        except:
            self._neededplayers = 6
        try:
            self._neededplayers = self.config.getint('settings', 'needed_players')
        except:
            self._neededplayers = 6
        map = self.console.getNextMap()
        if (map in self._botmaps and self._botstart):
            self.console.write('set bot_enable 1')
            self.debug('Enabling bots on %s' % map)
        else:
            self.console.write('set bot_enable 0')
            self.debug('Disabling bots on %s' % map)
            
    def addBots(self, event):
        if self._botstart:
            gametype = self.console.getCvar('g_gametype').getInt()
            if gametype == 0:
                self.console.write("kick allbots")
                self.console.write('bot_minplayers "0"')
                t = threading.Timer(self._time_addbotsFFA, self.FFAbots)
                t.start() 
            else:
                self.console.write('bot_minplayers "%s"' self._botminplayers)
            
    def FFAbots(self):
        self._clients = int(self.console.clients.getList())
        for c in self.console.clients.getClientsByLevel():
            if c.bot:
                self._clients -= 1
                
        if self._clients >= self._neededplayers:
            self.console.write('bot_minplayers "0"')
        else:
            self.console.write("exec botsFFA.cfg")
                
    def addMaps(self, event):
        nextmap = self.console.getNextMap()
        mapname = self.console.getCvar('mapname').getString()
        mapcycle = self.console.getCvar('g_mapcycle').getString()
        if (mapname == self._remmapsmap):
            i = 0
            for path in self._botmaps
                os.remove('%s/%s.pk3' % (self._sourcepath, self._botmaps[i]))
                i += 1
            i = 0
            os.remove('%s/%s2.txt' % (self.sourcepath, self._newmapcycle)
            self.console.write("g_mapcycle %s.txt" % self._oldmapcycle)
            self.console.write("bot_enable 1")
            self._botstart = False
            self.console.write("map %s" % self._addbotscyclemap)
        elif (mapname == self._addmapsmap):
            i = 0
            for path in self._botmaps
                shutil.copy('%s/%s.pk3' % (self._sourcepath, self._botmaps[i]), self._destpath)
                i += 1
            i = 0
            shutil.copyfile('%s/%s.txt' % (self.sourcepath, self._newmapcycle), '%s/%s2.txt' % (self._destpath, self._newmapcycle))
            self.console.write("g_mapcycle %s2.txt" % self._destpath)
            self.console.write("bot_enable 0")
            self._botstart = False
            self.console.write("map %s" % self._kickbotscyclemap)
        else:
            if mapcycle == ("%s2.txt" % self._newmapcycle):
                self.console.write("bot_enable 0")
            else:
                self.console.write("bot_enable 1")
            
            
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
