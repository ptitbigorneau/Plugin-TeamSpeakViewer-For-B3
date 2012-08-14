# Teamspeakviewer Plugin

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.2.1'

import b3
import b3.plugin
import b3.cron
from b3 import clients
from ts3 import TS3Server
from xml.etree.ElementTree import *

def ts3test(adresse, ts3portquery, admin, pwd, id):

    try:
    
        serverts3 = TS3Server(adresse, ts3portquery, id)
        serverts3.login(admin, pwd)

        return True
   
    except:
  
        return False 

class TeamspeakviewerPlugin(b3.plugin.Plugin):

    _adminPlugin = None
    _cronTab = None
    
    def onStartup(self):
        
        self._adminPlugin = self.console.getPlugin('admin')
        
        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False
	
        self._adminPlugin.registerCommand(self, 'ts3',self._ts3level, self.cmd_ts3)
        self._adminPlugin.registerCommand(self, 'ts3actived',self._ts3activedlevel, self.cmd_ts3actived)
		
        if self._cronTab:
            
            self.console.cron - self._cronTab

        self._cronTab = b3.cron.PluginCronTab(self, self.ts3update, minute='*/%s'%(self._interval))
        self.console.cron + self._cronTab
    
    def onLoadConfig(self):
	
        self._ts3level = self.config.getint('settings', 'ts3level')
        self._ts3adresse = self.config.get('settings', 'ts3adresse')
        self._ts3hostname = self.config.get('settings', 'ts3hostname')
        self._ts3portquery = self.config.get('settings', 'ts3portquery')
        self._ts3virtualserverid = self.config.getint('settings', 'ts3virtualserverid')
        self._ts3admin = self.config.get('settings', 'ts3admin')
        self._ts3pwd = self.config.get('settings', 'ts3pwd')
        self._interval = self.config.getint('settings', 'interval')
        self._ts3mess1 = self.config.get('settings', 'ts3mess1')
        self._ts3mess2 = self.config.get('settings', 'ts3mess2')
        self._ts3actived = self.config.get('settings', 'ts3actived')
        self._ts3activedlevel = self.config.getint('settings', 'ts3activedlevel')
    
    def ts3update(self):

        if self._ts3actived == 'off':
           
           self.debug('TeamSpeakViewer %s'%(self._ts3actived))
           return False

        if self._ts3actived == 'on':
            
            self.debug('TeamSpeakViewer %s'%(self._ts3actived))

            if ts3test(self._ts3adresse, self._ts3portquery, self._ts3admin, self._ts3pwd, self._ts3virtualserverid) == True:

                serverts3 = TS3Server(self._ts3adresse, self._ts3portquery, self._ts3virtualserverid)
                serverts3.login(self._ts3admin, self._ts3pwd)
                clientslist = serverts3.clientlist()
                listclients = None
            
                for clientts in clientslist.values():

                    if self._ts3admin not in clientts['client_nickname']:
                    
                        if "Unknown" in clientts['client_nickname'] or "from" in clientts['client_nickname'] and len(clientts['client_nickname']) > 1:
                    
                            listclients = listclients    
                       
                        else:

                            if listclients == None:

                                listclients = clientts['client_nickname']
                        
                            else:

                                listclients = listclients + ', ' + clientts['client_nickname']        

                if listclients != None:
                
                    listclients = listclients.replace('\xc3\xa9','e')
                    listclients = listclients.replace('\xc3\xa8','e')
                    listclients = listclients.decode('utf-8')
                    self.console.say('^3TeamSpeak3 Server: ^5%s'%(self._ts3hostname))
                    self.console.say('^3%s: '%(self._ts3mess1))
                    self.console.say('^5%s'%(listclients))
                    
                else:

                    self.console.say('^3TeamSpeak3 Server: ^5%s'%(self._ts3hostname))              

    def cmd_ts3(self, data, client, cmd=None):
        
        """\
        list of people on ts3
        """

        if ts3test(self._ts3adresse, self._ts3portquery, self._ts3admin, self._ts3pwd, self._ts3virtualserverid) == True:

            serverts3 = TS3Server(self._ts3adresse, self._ts3portquery, self._ts3virtualserverid)
            serverts3.login(self._ts3admin, self._ts3pwd)
            clientslist = serverts3.clientlist()
            listclients = None
            
            for clientts in clientslist.values():

                if self._ts3admin not in clientts['client_nickname']:

                    if "Unknown" in clientts['client_nickname'] or "from" in clientts['client_nickname'] and len(clientts['client_nickname']) > 1:
                    
                        listclients = listclients

                    else:                    

                        if listclients == None:

                            listclients = clientts['client_nickname']

                        else:

                            listclients = listclients + ', ' + clientts['client_nickname']        

            if listclients != None:
                
                listclients = listclients.replace('\xc3\xa9','e')
                listclients = listclients.replace('\xc3\xa8','e')
                listclients = listclients.decode('utf-8')
                client.message('^3TeamSpeak3 Server: ^5%s'%(self._ts3hostname))
                client.message('^3%s: '%(self._ts3mess1))
                client.message('^5%s'%(listclients))

            else:
                client.message('^3TeamSpeak3 Server: ^5%s'%(self._ts3hostname))
                client.message('^3%s'%(self._ts3mess2))
        else:

            client.message('^1ERROR TS3 SERVER')

    def cmd_ts3actived(self, data, client, cmd=None):
        
        """\
        activate / deactivate teamspeakviewer messages 
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
        
            if self._ts3actived == 'on':

                client.message('teamspeakviewer messages ^2activated')

            if self._ts3actived == 'off':

                client.message('teamspeakviewer messages ^1deactivated')

            client.message('!ts3actived <on / off>')
            return
      
		
        if input[0] == 'on':

            if self._ts3actived != 'on':

                self._ts3actived = 'on'
                message = '^2activated'

            else:

                client.message('teamspeakviewer messages is already ^2activated') 

                return False

        if input[0] == 'off':

            if self._ts3actived != 'off':

                self._ts3actived = 'off'
                message = '^1deactivated'

            else:
                
                client.message('teamspeakviewer messages is already ^1disabled')                

                return False

        client.message('teamspeakviewer messages %s'%(message))

        fichier = self.config.fileName
        tree = parse(fichier)
        root = tree.getroot()

        variables = root.find('settings')

        for a in variables:
           
            if a.get('name') == 'ts3actived':
      
                a.text = input[0]
        
        tree.write(fichier)