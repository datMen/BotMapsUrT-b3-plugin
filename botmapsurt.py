__version__ = '3.0'
__author__  = 'LouK' #

import b3, time, threading
import b3.events
import b3.plugin
import shutil
import os
    
class BotmapsurtPlugin(b3.plugin.Plugin):
    _botmaps = {}
    _clients = 0
    _addmapsmap = ""
    _remmapsmap = ""
    _sourcepath = ""
    _destpath = ""
    _newmapcycle = ""
    _oldmapcycle = ""
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
        self._oldmapcycle = self.console.getCvar('g_mapcycle').getString()
     
        if not self._adminPlugin:
            self.error('No se pudo encontrar el plugin en Admin')
            return
        
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = self.getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

    
    def onEvent(self, event):
        if event.type == b3.events.EVT_GAME_ROUND_START:
            self.addBots(event)
            self.addMaps(event)
            
    def onLoadConfig(self):
        self.loadBotstuff()
        
    def getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func

        return None
        
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
            maps = self.config.get('settings', 'bot_maps')
            maps = maps.split(', ')
            self._botmaps = maps
        except:
            self._botmaps = {}
            self.debug('No maps for botsupport...')
        try:
            self._time_addbotsFFA = self.config.getint('settings', 'add_bots_FFA')
        except:
            self._time_addbotsFFA = 10
        try:
            self._neededplayers = self.config.getint('settings', 'needed_players')
        except:
            self._neededplayers = 6
        try:
            self._addmapsmap = self.config.get('settings', 'add_custom_maps_map')
        except:
            self._addmapsmap = "ut4_prague"
        try:
            self._remmapsmap = self.config.get('settings', 'add_bots_map')
        except:
            self._remmapsmap = "ut4_sanc"
        try:
            self._botminplayers = self.config.getint('settings', 'bot_minplayers')
        except:
            self._botminplayers = 6
        try:
            self._time_addbotsFFA = self.config.getint('settings', 'time_addbots_FFA')
        except:
            self._time_addbotsFFA = 10
        try:
            self._sourcepath = self.config.get('settings', 'source_path')
        except:
            self._sourcepath = ""
        try:
            self._destpath = self.config.get('settings', 'destination_path')
        except:
            self._destpath = ""
        try:
            self._newmapcycle = self.config.get('settings', 'new_mapcycle')
        except:
            self.newmapcycle = ""
            
    def addBots(self, event):
        if self._botstart:
            gametype = self.console.getCvar('g_gametype').getInt()
            if gametype == 0:
                self.console.write('bot_minplayers "0"')
                self.debug('Enabling bots on %s' % map)
                t = threading.Timer(self._time_addbotsFFA, self.FFAbots)
                t.start() 
            else:
                self.console.write('bot_minplayers "%s"' % self._botminplayers)
        else:
            self.console.write("kick allbots")
            self.debug('Disabling bots on %s' % map)
            
    def FFAbots(self):
        i = 0
        while i <= len(self.console.clients.getClientsByLevel()):
            self.debug('%s clients' % self._clients)
            self._clients += 1
            for c in self.console.clients.getClientsByLevel():
                if c.bot:
                    self._clients -= 1
                    self.debug('Detected a bot, %s clients' % self._clients)
            i += 1
        i = 0
                
        if self._clients >= self._neededplayers:
            self.console.write('bot_minplayers "0"')
        else:
            self.console.write('bot_minplayers "0"')
            self.console.write("kick allbots")
            self.console.write("exec botsFFA.cfg")
                
    def addMaps(self, event):
        nextmap = self.console.getNextMap()
        mapname = self.console.getCvar('mapname').getString()
        mapcycle = self.console.getCvar('g_mapcycle').getString()
        if (mapname == self._remmapsmap):
            i = 0
            while i < len(self._botmaps):
                os.remove('%s/%s.pk3' % (self._destpath, self._botmaps[i]))
                self.debug('removed %s' % (self._botmaps[i]))
                i += 1
            i = 0
            os.remove('%s/%s2.txt' % (self._destpath, self._newmapcycle))
            self.console.setCvar('g_mapcycle', self._oldmapcycle)
            self.console.write("bot_enable 1")
            self._botstart = False
            self.console.write("cyclemap")
        elif (mapname == self._addmapsmap):
            i = 0
            while i < len(self._botmaps):
                shutil.copy('%s/%s.pk3' % (self._sourcepath, self._botmaps[i]), self._destpath)
                self.debug('Added %s to %s' % (self._botmaps[i], self._destpath))
                i += 1
            i = 0
            shutil.copyfile('%s/%s.txt' % (self._sourcepath, self._newmapcycle), '%s/%s2.txt' % (self._destpath, self._newmapcycle))
            newmapcycle = "%s2.txt" % self._newmapcycle
            self.console.setCvar('g_mapcycle', newmapcycle)
            self.console.write("bot_enable 0")
            self._botstart = False
            self.console.write("cyclemap")
        else:
            if mapcycle == ("%s2.txt" % self._newmapcycle):
                self.console.write("bot_enable 0")
            else:
                self.console.write("bot_enable 1")
            
           
           
    def cmd_addmaps(self, data, client, cmd=None):
        """\
        add maps to the server
        """
        self._botstart = False
        self.console.write("g_nextmap %s" % self._addmapsmap)
        client.message('^7You ^2 added ^7custom maps(will be added after %s).' % self._addmapsmap)
        
    def cmd_remmaps(self, data, client, cmd=None):
        """\
        Add bot maps to the server(and change mapcycle)
        """
        self._botstart = True
        self.console.write('bot_enable 1')
        self.console.write("g_nextmap %s" % self._remmapsmap)
        client.message('^7Custom maps ^1removed^7 (bots maps will be added at map change)')
            
    def cmd_kickbots(self, data, client, cmd=None):
        """\
        kick all bots in the server. <perm> to kick them until you use !addbots
        """
        input = self._adminPlugin.parseUserCmd(data)
        
        if not input:
            self._botstart = True
            self.console.write("kick allbots")
            self.console.write('bot_minplayers "0"')
            client.message('^7You ^1kicked ^7all bots in the server.')
            return True

        if input[0] == 'perm' or input[0] == 'permanent' or input[0] == 'lock':
            self._botstart = False
            self.console.write("kick allbots")
            self.console.write('bot_minplayers "0"')
            client.message('^7You ^1kicked ^7all bots in the server and they wont be added each map.')
        
    def cmd_addbots(self, data, client, cmd=None):
        """\
        Add bots to the server
        """
        client.message('^7%s' % (', '.join(self._botmaps)))
        client.message('^7%s' % (self._botmaps))
        mapcycle = self.console.getCvar('g_mapcycle').getString()
        if mapcycle == self._newmapcycle:
            client.message('^7You have to use !botmaps to add bots.')
            return False
            
        gametype = self.console.getCvar('g_gametype').getInt()
        self._botstart = True
        if gametype==0:
            self.console.write("exec botsFFA.cfg")
        elif gametype==3:
            self.console.write('bot_minplayers "8"')
        client.message('^7Bots ^2added^7')