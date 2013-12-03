__version__ = '3.0'
__author__  = 'LouK' # www.sniperjum.com

import b3, time, threading
import b3.events
import b3.plugin
import shutil
import os
    
class BotmapsurtPlugin(b3.plugin.Plugin):
    _allBots = []
    _custom_maps = {} # Maps to add
    _clients = 0 # Clients control at round_start
    _addmaps = False # Map where the plugin will copy the custom maps
    _remmaps = False # Map where the plugin will remove the custom maps
    _sourcepath = "" # Directory from where maps will be copied
    _destpath = "" # Directory where maps will be copied
    _newmapcycle = "" # Mapcycle with custom maps
    _oldmapcycle = "" # Mapcycle with bots
    _botstart = True # To control if the plugin has to to add bots or not
    _botminplayers = 6 # Bots control related with players
    _clients = 0 # Clients number
    _bots = 0 # bots number
    _i = 0
    _adding = False
    
    def onStartup(self):
        self.registerEvent(b3.events.EVT_GAME_ROUND_START)
        self.registerEvent(b3.events.EVT_CLIENT_AUTH)
        self.registerEvent(b3.events.EVT_CLIENT_DISCONNECT)
        self._adminPlugin = self.console.getPlugin('admin')
     
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return
        
        # Register commands
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
            mapcycle = self.console.getCvar('g_mapcycle').getString() # Get mapcycle
            if mapcycle != ("%s2.txt" % self._newmapcycle):
                # If mapcycle is not the one with custom maps set oldmapcycle as default mapcycle
                self._oldmapcycle = mapcycle
            self.addBots(event)
            self.addMaps(event, mapcycle) 
        elif event.type == b3.events.EVT_CLIENT_AUTH:
            sclient = event.client
            if 'BOT' not in sclient.guid:
                self.addBots() 
        elif event.type == b3.events.EVT_CLIENT_DISCONNECT:
            sclient = event.client
            if 'BOT' not in sclient.guid:
                self.addBots() 
            
    def onLoadConfig(self):
        self.loadBotstuff() # Get stuff from the .xml
        
    def getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func

        return None
        
    def loadBotstuff(self):
        for bot in self.config.get('bots/bot'):
            nameBot = bot.find('name').text
            charBot = bot.find('character').text
            lvlBot = bot.find('skill').text
            teamBot = bot.find('team').text
            pingBot = bot.find('ping').text
            self._allBots.insert(1, [charBot, lvlBot, teamBot, pingBot, nameBot])
            self.debug('Bot added: %s %s %s %s %s' % (nameBot, charBot, lvlBot, teamBot, pingBot))
                    
        try:
            self._botminplayers = self.config.getint('settings', 'bot_minplayers')
            if self._botminplayers < 0:
                self._botminplayers = 0
        except:
            self._botminplayers = 4
        try:
            maps = self.config.get('settings', 'custom_maps')
            maps = maps.split(', ')
            self._custom_maps = maps
        except:
            self._custom_maps = {}
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
            
    def addBots(self):
        self.debug('starting proceess to add/rem bots')
        self.debug('self._i = %s' % self._i)
        if self._botstart: # if bots are enabled
            self.console.write("bot_enable 1")
            for c in self.console.clients.getClientsByLevel(): # Get allplayers
                self._clients += 1
                
                if 'BOT' in c.guid:
                    self._clients -= 1
                    self._bots += 1
                    self.debug('loop bots = %s' % self._bots)
            
            clients = self._clients
            bots = self._bots
            bclients = self._botminplayers - clients - bots
            self.debug('bots = %s' % bots)
            self.debug('clients = %s' % clients)
            self.debug('bclients = %s' % bclients)
            if bclients == 0 or ((self._clients - self._bots) > self._botminplayers):
                self.debug('bclients = %s, stopping check' % bclients)
                self._bots = 0
                self._clients = 0
                self._adding = False
                return False
            # bclients = (bots + clients)

            if bclients > 0: # Check if we need to add bots
                self.debug('adding bots')
                if self._adding:
                    self._i += 1
                    self.debug('self._i += 1')
                    self.debug('self._i = %s' % self._i)

                while bclients > 0: # Add all the necessary bots
                    #if bclients == 0:
                    #    break
                    bclients -= 1
                    self.console.write('addbot %s %s %s %s %s' % (self._allBots[self._i][0], self._allBots[self._i][1], self._allBots[self._i][2], self._allBots[self._i][3], self._allBots[self._i][4]))
                    if self._i < (len(self._allBots) - 1):
                        self._i += 1
                        self.debug('self._i += 1')
                        self.debug('self._i = %s' % self._i)
                self._adding = True
                self._i -= 1
                self.debug('self._i -= 1')
                self.debug('self._i = %s' % self._i)
                    
            elif bclients < 0: # Check if we need to kick bots
                self.debug('kicking bots')
                while bclients < 0:
                    #if bclients == 0:
                    #    self.debug('BREAKED CAUSE ITS 0(kicking)')
                    #    break
                
                    self.debug('player = %s' % self._allBots[self._i][4])
                    self.debug('i(kick) = %s and i = %s' % (self._allBots[self._i][4], self._i))
                    bclients += 1
                    self.console.write('kick %s' % self._allBots[self._i][4])
                    if self._i > 0:
                        self._i -= 1

                self._adding = True

            self._bots = 0
            self._clients = 0
                
    def addMaps(self, event):
        mapcycle = self.console.getCvar('g_mapcycle').getString()
        nextmap = self.console.getNextMap()
        mapname = self.console.getCvar('mapname').getString()
        if self._remmaps:
            i = 0
            while i < len(self._custom_maps):
                os.remove('%s/%s.pk3' % (self._destpath, self._custom_maps[i])) # Remove maps from the q3ut4
                self.debug('removed %s' % (self._custom_maps[i]))
                i += 1
            i = 0
            os.remove('%s/%s2.txt' % (self._destpath, self._newmapcycle)) # Remove mapcycle from the q3ut4
            # Enable bots
            self.console.setCvar('g_mapcycle', self._oldmapcycle) # Set the bots mapcycle
            self.console.write("bot_enable 1")
            self._botstart = False
            self._remmaps = False
            self.console.write("cyclemap")
        elif self._addmaps:
            i = 0
            while i < len(self._custom_maps):
                shutil.copy('%s/%s.pk3' % (self._sourcepath, self._custom_maps[i]), self._destpath) # Add maps to the q3ut4
                self.debug('Added %s to %s' % (self._custom_maps[i], self._destpath))
                i += 1
            i = 0
            shutil.copyfile('%s/%s.txt' % (self._sourcepath, self._newmapcycle), '%s/%s2.txt' % (self._destpath, self._newmapcycle)) # Add mapcycle to the q3ut4
            newmapcycle = ("%s2.txt" % self._newmapcycle)
            self.console.setCvar('g_mapcycle', newmapcycle) # Set the new mapcycle
            # Disable bots
            self.console.write("bot_enable 0")
            self._botstart = False
            self._addmaps = False
            self.console.write("cyclemap")
        else:
            if mapcycle == ("%s2.txt" % self._newmapcycle):
                self.console.write("bot_enable 0") # If mapcycle is not the bots mapcycle disable bots
            else:
                self.console.write("bot_enable 1")
            
           
           
    def cmd_addmaps(self, data, client, cmd=None):
        """\
        add maps to the server
        """
        self._botstart = False
        self.console.write("bot_enable 0")
        self._addmaps = True
        client.message('^7You ^2 added ^7custom maps(will be added after nextmap).')
        
    def cmd_remmaps(self, data, client, cmd=None):
        """\
        Add bot maps to the server(and change mapcycle)
        """
        self._botstart = True
        self._remmaps = True
        client.message('^7Custom maps ^1removed^7 (bots maps will be added after nextmap).')
            
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
            return False

        if input[0] == 'perm' or input[0] == 'permanent' or input[0] == 'lock':
            self._botstart = False
            self.console.write("kick allbots")
            self.console.write('bot_minplayers "0"')
            client.message('^7You ^1kicked ^7all bots in the server and they wont be added each map.')
        
    def cmd_addbots(self, data, client, cmd=None):
        """\
        Add bots to the server
        """
        mapcycle = self.console.getCvar('g_mapcycle').getString()
        if mapcycle == ("%s2.txt" % self._newmapcycle):
            client.message('^7You have to use !remmaps before to add bots.')
            return False
            
        gametype = self.console.getCvar('g_gametype').getInt()
        self._botstart = True
        if gametype==0:
            self.console.write("exec botsFFA.cfg")
        elif gametype==3:
            self.console.write('bot_minplayers "%s"' % self._botminplayers)
        client.message('^7Bots ^2added^7')