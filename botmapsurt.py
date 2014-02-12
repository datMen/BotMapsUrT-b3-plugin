__version__ = '3.0'
__author__  = 'LouK' # www.sniperjum.com

import b3, time, threading, re
import b3.events
import b3.plugin
import shutil
import os
    
class BotmapsurtPlugin(b3.plugin.Plugin):
    _allBots = []
    _custom_maps = {} # Maps to add
    _clients = 0 # Clients control at round_start
    _addmaps = False # Map where the plugin will copy the custom maps
    _putmap = False
    _remmaps = False # Map where the plugin will remove the custom maps
    _sourcepath = "" # Directory from where maps will be copied
    _destpath = "" # Directory where maps will be copied
    _newmapcycle = "" # Mapcycle with custom maps
    _oldmapcycle = "" # Mapcycle with bots
    _botstart = True # To control if the plugin has to to add bots or not
    _botstart2 = False
    _botminplayers = 6 # Bots control related with players
    _minmapplayers = 0
    _clients = 0 # Clients number
    _bots = 0 # bots number
    _mapbots = 0
    _i = 0
    _FFA = True
    _adding = False
    _first = True
    
    def onStartup(self):
        self.registerEvent(b3.events.EVT_GAME_ROUND_START)
        self.registerEvent(b3.events.EVT_GAME_EXIT)
        self.registerEvent(b3.events.EVT_CLIENT_AUTH)
        self.registerEvent(b3.events.EVT_CLIENT_DISCONNECT)
        self.registerEvent(b3.events.EVT_STOP)
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
            if self._first:
                self.addMaps()
                self.console.write('bot_minplayers "0"')
                gametype = self.console.getCvar('g_gametype').getInt()
                if gametype == 0:
                    if self._botstart:
                        if self._FFA:
                            self._bots = 0
                            self._clients = 0
                            self._i = 0
                            self._adding = False
                            self.console.write("kick allbots")
                            self.addBots()
                            self._FFA = False
                else:
                    self._FFA = True
                self._first == False
                #t = threading.Timer(10, self.addMaps) # Add bots
                #t.start()
            else:
                self._first = True
                #self._botstart2 = True

        elif event.type == b3.events.EVT_GAME_EXIT:
            if self._first:
                self.addMaps()
                if self._minmapplayers <= self._clients:
                    self._botstart = False
                    self.console.write("bot_enable 0")
                    self._addmaps = True
                    self.disableBots()
                    self.console.say("Custom maps will be added at nextmap!")
                if self._botstart:
                    self._botstart = False
                    self._botstart2 = True
                    self._mapbots = self._bots
                self._first == False
                #if self._putmap:
                 #   self.console.write('map %s' % self.console.getNextMap())
                  #  self._putmap = False
            else:
                self._first = True
        elif event.type == b3.events.EVT_CLIENT_AUTH:
            sclient = event.client
            if self._mapbots != False:
                if self._botstart:
                    self.addBots()
                else:
                    self._clients = 0
                    for c in self.console.clients.getClientsByLevel(): # Get allplayers
                        self._clients += 1
                    if (self._minmapplayers - self._botminplayers) > self._clients:
                        self._remmaps = True
                        self._addmaps = False
                        self.console.say("Custom maps will be removed at nextmap!") 
            elif 'BOT' not in sclient.guid:
                if self._botstart:
                    self.addBots()
                else:
                    self._clients = 0
                    for c in self.console.clients.getClientsByLevel(): # Get allplayers
                        self._clients += 1
                    if (self._minmapplayers - self._botminplayers) > self._clients:
                        self._remmaps = True
                        self._addmaps = False
                        self.console.say("Custom maps will be removed at nextmap!") 
        elif event.type == b3.events.EVT_CLIENT_DISCONNECT:
            sclient = event.client
            if 'BOT' not in sclient.guid:
                if self._botstart:
                    self.addBots() 
                else:
                    self._clients = 0
                    for c in self.console.clients.getClientsByLevel(): # Get allplayers
                        self._clients += 1
                    if (self._minmapplayers - self._botminplayers) > self._clients:
                        self._remmaps = True
                        self._addmaps = False
                        self.console.say("Custom maps will be removed at nextmap!") 
        elif event.type == b3.events.EVT_STOP:
            self.console.write("kick allbots")
            
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
            self._newmapcycle = self.config.get('settings', 'new_mapcycle')
        except:
            self._newmapcycle = ""
        try:
            self._minmapplayers = self.config.getint('settings', 'min_addmaps_players')
            if self._minmapplayers < 0:
                self._minmapplayers = 0
        except:
            self._minmapplayers = 0

        self._destpath = self.console.getCvar('fs_homepath').getString()
            
    def addBots(self):
        #self.debug('starting proceess to add/rem bots')
        #self.debug('self._i = %s' % self._i)
        self._bots = 0
        self._clients = 0
        if self._botstart: # if bots are enabled
            self.console.write("bot_enable 1")
            for c in self.console.clients.getClientsByLevel(): # Get allplayers
                self._clients += 1
                
                if 'BOT' in c.guid:
                    self._clients -= 1
                    self._bots += 1
                    #self.debug('loop bots = %s' % self._bots)
            
            clients = self._clients
            bots = self._bots
            bclients = self._botminplayers - clients - bots
            #self.debug('bots = %s' % bots)
            #self.debug('clients = %s' % clients)
            #self.debug('bclients = %s' % bclients)
            if bclients == 0 or ((self._clients - self._bots) > self._botminplayers):
                self.debug('bclients = %s, stopping check' % bclients)
                return False
            if self._mapbots > bots:
                self.debug('self._mapbots = %s, bots = %s. STOPPING' % (self._mapbots, bots))
                return False
            self._mapbots = False
            # bclients = (bots + clients)

            if bclients > 0: # Check if we need to add bots
                self.debug('adding bots')
                if self._adding:
                    self._i += 1
                    #self.debug('self._i += 1')
                    #self.debug('self._i = %s' % self._i)

                while bclients > 0: # Add all the necessary bots
                    #if bclients == 0:
                    #    break
                    bclients -= 1
                    if self._i == len(self._allBots):
                        break
                    self.console.write('addbot %s %s %s %s %s' % (self._allBots[self._i][0], self._allBots[self._i][1], self._allBots[self._i][2], self._allBots[self._i][3], self._allBots[self._i][4]))
                    self._bots += 1
                    if self._i < (len(self._allBots)):
                        self._i += 1
                        #self.debug('self._i += 1')
                        #self.debug('self._i = %s' % self._i)
                self._adding = True
                if self._i > 0:
                    self._i -= 1
                #self.debug('self._i -= 1')
                #self.debug('self._i = %s' % self._i)
                    
            elif bclients < 0: # Check if we need to kick bots
                self.debug('kicking bots')
                while bclients < 0:
                    #if bclients == 0:
                    #    self.debug('BREAKED CAUSE ITS 0(kicking)')
                    #    break
                
                    #self.debug('player = %s' % self._allBots[self._i][4])
                    #self.debug('i(kick) = %s and i = %s' % (self._allBots[self._i][4], self._i))
                    self._bots -= 1
                    bclients += 1
                    self.console.write('kick %s' % self._allBots[self._i][4])
                    self._i -= 1

                self._adding = True
                
    def addMaps(self):
        nextmap = self.console.getNextMap()
        #self.debug('Getting nextmap')
        mapname = self.console.getCvar('mapname').getString()
        #self.debug('Getting mapname')
        if self._remmaps:
            # os.remove('%s/%s2.txt' % (self._destpath, self._newmapcycle)) # Remove mapcycle from the q3ut4
            # Enable bots
            self.console.setCvar('g_mapcycle', self._oldmapcycle) # Set the bots mapcycle
            self.console.write("bot_enable 1")
            # self.disableBots()
            self._remmaps = False
            self._botstart2 = True
            self.console.write("cyclemap")
            i = 0
            while i < len(self._custom_maps):
                os.remove('%s/q3ut4/%s.pk3' % (self._destpath, self._custom_maps[i])) # Remove maps from the q3ut4
                self.debug('removed %s' % (self._custom_maps[i]))
                i += 1
        elif self._addmaps:
            # shutil.copyfile('%s/%s.txt' % (self._sourcepath, self._newmapcycle), '%s/%s2.txt' % (destpath, self._newmapcycle)) # Add mapcycle to the q3ut4
            # newmapcycle = ("%s2.txt" % self._newmapcycle)
            # Disable bots
            self.console.write("bot_enable 0")
            self._addmaps = False
            self._putmap = True
            i = 0
            while i < len(self._custom_maps):
                shutil.copy('%s/%s.pk3' % (self._sourcepath, self._custom_maps[i]), '%s/q3ut4' % self._destpath) # Add maps to the q3ut4
                self.debug('Added %s to %s' % (self._custom_maps[i], self._destpath))
                i += 1
            # self.console.write("cyclemap")
        else:
            if self.console.getCvar('g_mapcycle').getString() == self._newmapcycle or self._putmap:
                self.console.write("bot_enable 0") # If mapcycle is not the bots mapcycle disable bots
            else:
                self.console.write("bot_enable 1")
                self._oldmapcycle = self.console.getCvar('g_mapcycle').getString()
                #self.debug('Getting mapcycle')
            if self._botstart2:
                self._botstart = True
                self.addBots()
                self._botstart2 = False
            if self._putmap:
                self._putmap = False
                self.console.setCvar('g_mapcycle', self._newmapcycle)
                self.console.write("cyclemap")
            
           
    def enableBots(self):
        self.console.say('No-bots time finished, adding bots...')
        self._botstart = True
        self.addBots()

    def disableBots(self):
        self._botstart = False
        self._bots = 0
        self._clients = 0
        self._i = 0
        self._adding = False
        self._mapbots = False
        self.console.write("kick allbots")

    def cmd_addmaps(self, data, client, cmd=None):
        """\
        add maps to the server
        """
        input = self._adminPlugin.parseUserCmd(data)
        if not input:
            self._botstart = False
            self.console.write("bot_enable 0")
            self._addmaps = True
            self.disableBots()
            client.message('^7You ^2 added ^7custom maps(will be added after nextmap).')
            return False
        
        status = input[0]
        if status == 'now':
            self._botstart = False
            self.console.write("bot_enable 0")
            self._addmaps = True
            self.disableBots()
            self.addMaps()
            self.console.say('^7Cyclying map to add custom maps...')
            time.sleep(3)
            self.console.write("cyclemap")
        
    def cmd_remmaps(self, data, client, cmd=None):
        """\
        Add bot maps to the server(and change mapcycle)
        """
        if self._addmaps:
            self._botstart = True
            self._addmaps = False
            client.message('^1CANCELLED^7 addmaps.')
        else:
            self._remmaps = True
            client.message('^7Custom maps ^1removed^7 (bots maps will be added after nextmap).')

        input = self._adminPlugin.parseUserCmd(data)
        status = input[0]
        if status == 'now':
            self.console.say('^7Cyclying map to remove custom maps...')
            self.addMaps()
            
    def cmd_kickbots(self, data, client, cmd=None):
        """\
        kick all bots in the server. <perm> to kick them until you use !addbots
        """
        input = self._adminPlugin.parseUserCmd(data)
        self.disableBots()
        if not input:
            client.message('^7You ^1kicked ^7all bots in the server')
            client.message('^7Use ^2!addbots ^7to add them')
            return False

        regex = re.compile(r"""^(?P<number>\d+)$""");
        match = regex.match(data)

        time = int(match.group('number'))
        t = threading.Timer((time * 60), self.enableBots)
        t.start()
        client.message('^7You ^1kicked ^7all bots in the server for ^5%s ^7minutes' % time)
        client.message('^7Use ^2!addbots ^7to add them')
        
    def cmd_addbots(self, data, client, cmd=None):
        """\
        Add bots to the server
        """
        mapcycle = self.console.getCvar('g_mapcycle').getString()
        if mapcycle == self._newmapcycle:
            client.message('^7You have to use ^2!remmaps ^7before to add bots.')
            return False
        
        self._botstart = True
        self.addBots()
        client.message('^7Bots ^2added^7.')