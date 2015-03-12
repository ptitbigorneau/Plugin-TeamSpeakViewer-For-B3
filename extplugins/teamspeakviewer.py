# Teamspeakviewer Plugin

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.4'

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
    
    _ts3adresse = "localhost"
    _ts3hostname = "teamspeak.example.com"
    _ts3admin = "serveradmin"
    _ts3pwd = "password"
    _ts3portquery = 10011
    _ts3virtualserverid = 1
    _interval = 10
    _ts3level = 1
    _ts3mess1 = "Currently Online"
    _ts3mess2 = "Currently there is no people online"
    _ts3activedlevel = 100
    _ts3actived = "on"
    _ts3kick = 20
    _ts3ban = 40
    _ts3poke = 20
    _ts3msg = 20
    _ts3channelmsg = 20	

    def onStartup(self):
        
        self._adminPlugin = self.console.getPlugin('admin')
        
        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False

        self._adminPlugin.registerCommand(self, 'ts3',self._ts3level, self.cmd_ts3)
        self._adminPlugin.registerCommand(self, 'ts3actived',self._ts3activedlevel, self.cmd_ts3actived)
        
        self._adminPlugin.registerCommand(self, 'ts3kick',self._ts3kick, self.cmd_ts3kick, 'ts3k')
        self._adminPlugin.registerCommand(self, 'ts3ban',self._ts3ban, self.cmd_ts3ban, 'ts3b')
        self._adminPlugin.registerCommand(self, 'ts3poke',self._ts3poke, self.cmd_ts3poke, 'ts3p')
        self._adminPlugin.registerCommand(self, 'ts3msg',self._ts3msg, self.cmd_ts3msg, 'ts3m')
        self._adminPlugin.registerCommand(self, 'ts3channelmsg',self._ts3channelmsg, self.cmd_ts3channelmsg, 'ts3cm')

        if self._cronTab:
            
            self.console.cron - self._cronTab

        self._cronTab = b3.cron.PluginCronTab(self, self.ts3update, minute='*/%s'%(self._interval))
        self.console.cron + self._cronTab
    
    def onLoadConfig(self):

        try:
            self._ts3level = self.config.getint('settings', 'ts3level')
        except Exception, err:
            self.warning("Using default value %s for ts3level. %s" % (self._ts3level, err))
        self.debug('ts3level : %s' % self._ts3level)

        try:
            self._ts3adresse = self.config.get('settings', 'ts3adresse')
        except Exception, err:
            self.warning("Using default value %s for ts3adresse. %s" % (self._ts3adresse, err))
        self.debug('ts3adresse : %s' % self._ts3adresse)

        try:
            self._ts3hostname = self.config.get('settings', 'ts3hostname')
        except Exception, err:
            self.warning("Using default value %s for ts3hostname. %s" % (self._ts3hostname, err))
        self.debug('ts3hostname : %s' % self._ts3hostname)

        try:
            self._ts3portquery = self.config.get('settings', 'ts3portquery')
        except Exception, err:
            self.warning("Using default value %s for ts3portquery. %s" % (self._ts3portquery, err))
        self.debug('ts3portquery : %s' % self._ts3portquery)

        try:
            self._ts3virtualserverid = self.config.getint('settings', 'ts3virtualserverid')
        except Exception, err:
            self.warning("Using default value %s for ts3virtualserverid. %s" % (self._ts3virtualserverid, err))
        self.debug('ts3virtualserverid : %s' % self._ts3virtualserverid)

        try:
            self._ts3admin = self.config.get('settings', 'ts3admin')
        except Exception, err:
            self.warning("Using default value %s for ts3admin. %s" % (self._ts3admin, err))
        self.debug('ts3admin : %s' % self._ts3admin)
        
        try:
            self._ts3pwd = self.config.get('settings', 'ts3pwd')
        except Exception, err:
            self.warning("Using default value %s for ts3pwd. %s" % (self._ts3pwd, err))
        self.debug('ts3pwd : *******')

        try:
            self._interval = self.config.getint('settings', 'interval')
        except Exception, err:
            self.warning("Using default value %s for interval. %s" % (self._interval, err))
        self.debug('interval : %s' % self._interval)

        try:
            self._ts3mess1 = self.config.get('settings', 'ts3mess1')
        except Exception, err:
            self.warning("Using default value %s for ts3mess1. %s" % (self._ts3mess1, err))
        self.debug('ts3mess1 : %s' % self._ts3mess1)

        try:
            self._ts3mess2 = self.config.get('settings', 'ts3mess2')
        except Exception, err:
            self.warning("Using default value %s for ts3mess2. %s" % (self._ts3mess2, err))
        self.debug('ts3mess2 : %s' % self._ts3mess2)

        try:
            self._ts3actived = self.config.get('settings', 'ts3actived')
        except Exception, err:
            self.warning("Using default value %s for ts3actived. %s" % (self._ts3actived, err))
        self.debug('ts3actived : %s' % self._ts3actived)

        try:
            self._ts3activedlevel = self.config.getint('settings', 'ts3activedlevel')
        except Exception, err:
            self.warning("Using default value %s for ts3activedlevel. %s" % (self._ts3activedlevel, err))
        self.debug('ts3activedlevel : %s' % self._ts3activedlevel)

        try:
            self._ts3kick = self.config.getint('settings', 'ts3kick')
        except Exception, err:
            self.warning("Using default value %s for ts3kick. %s" % (self._ts3kick, err))
        self.debug('ts3kick : %s' % self._ts3kick)

        try:
            self._ts3ban = self.config.getint('settings', 'ts3ban')
        except Exception, err:
            self.warning("Using default value %s for ts3ban. %s" % (self._ts3ban, err))
        self.debug('ts3ban : %s' % self._ts3ban)

        try:
            self._ts3poke = self.config.getint('settings', 'ts3poke')
        except Exception, err:
            self.warning("Using default value %s for ts3poke. %s" % (self._ts3poke, err))
        self.debug('ts3poke : %s' % self._ts3poke)

        try:
            self._ts3msg = self.config.getint('settings', 'ts3msg')
        except Exception, err:
            self.warning("Using default value %s for ts3kick. %s" % (self._ts3msg, err))
        self.debug('ts3msg : %s' % self._ts3msg)

        try:
            self._ts3channelmsg = self.config.getint('settings', 'ts3channelmsg')
        except Exception, err:
            self.warning("Using default value %s for ts3channelmsg. %s" % (self._ts3channelmsg, err))
        self.debug('ts3channelmsg : %s' % self._ts3channelmsg)

    def ts3update(self):

        if self._ts3actived == 'off':
           
           self.debug('TeamSpeakViewer %s'%(self._ts3actived))
           return False

        if self._ts3actived == 'on':
            
            self.debug('TeamSpeakViewer %s'%(self._ts3actived))

            if ts3test(self._ts3adresse, self._ts3portquery, self._ts3admin, self._ts3pwd, self._ts3virtualserverid) == True:

                list = self.tslistclients()
                listclients = None
            
                for tsclient in list:
        
                    if listclients == None:

                        listclients = tsclient
                        
                    else:

                        listclients = listclients + ', ' + tsclient

                if listclients != None:
                    
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

            list = self.tslistclients()
            listclients = None
            
            for tsclient in list:
        
                if listclients == None:

                    listclients = tsclient
                        
                else:

                    listclients = listclients + ', ' + tsclient

            if listclients != None:
                    
                client.message('^3TeamSpeak3 Server: ^5%s'%self._ts3hostname)					
                client.message('^3%s: '%(self._ts3mess1))
                client.message('^5%s^7'%(listclients))       
					
            else:

                client.message('^3TeamSpeak3 Server: ^5%s'%(self._ts3hostname)) 
                client.message('^3%s^7'%(self._ts3mess2))
        else:

            client.message('^1ERROR TS3 SERVER')

    def cmd_ts3kick(self, data, client, cmd=None):
        
        """\
        ts3 kick
        """

        adminb3=client.name.replace("|", "*")
        adminb3=client.name.replace("/", "*")
        adminb3=client.name.replace("\\", "*")

        clid = None        

        if data:
            
            input = data.split(" ")
        
        else:

            client.message('!ts3kick <teamspeak user> <reason>')
            return
	
        listclients = None

        tslistclients = self.tslistclients()
		
        if len(input) < 2:
            reason = "You have been kicked by %s"%client.name

        else:
            reason = None
            datareason = input[1:]
            for d in datareason:
                if reason == None:
                    reason = d
                else:
                    reason = reason + " " + d

        if input[0].isdigit():
            userts = self.searchtsclid(input[0])
            self.kicktsclient(input[0], reason, adminb3)
            client.message('^3TeamSpeak Server ^2You kicked: ^5%s'%(userts))
            client.message('for ^5%s^7'%(reason))

        else:

            tsuser=input[0].lower()
            
            if len(tsuser) < 3:
                client.message('^1Need a minimum of 3 characters for the TeamSpeak user name^7')            
                return
               
            n = 0
            lusers = None
            
            for cl in tslistclients:
                  
                if tsuser in cl.lower():

                    n = n + 1
                    clid = self.tsclid(cl)
                    
                    if lusers == None:
                        clts = cl
                        lusers = "%s:%s"%(clid, cl)
                    else:
                        lusers = lusers + ", %s:%s"%(clid, cl)

            if n == 0:

                client.message('^1No Teamspeak User found^7')

            if n > 1:
                         
                client.message('^3User TeamSpeak found: ^2%s^7'%(lusers))
                    
            if n == 1:
                
                clid = self.tsclid(clts)
                self.kicktsclient(clid, reason, adminb3)
                client.message('^3TeamSpeak ^2Server You kicked: ^5%s'%(clts))
                client.message('^2for ^5%s^7'%(reason))

    def cmd_ts3poke(self, data, client, cmd=None):
        
        """\
        ts3 poke
        """

        adminb3=client.name.replace("|", "*")
        adminb3=client.name.replace("/", "*")
        adminb3=client.name.replace("\\", "*")

        clid = None        

        if data:

            input = data.split(" ")
        
        else:

            client.message('!ts3poke <teamspeak user> <message>')
            return

        listclients = None

        tslistclients = self.tslistclients()

        if len(input) < 2:
            message = "Hello !!!"

        else:
            message = None
            datamessage = input[1:]
            for d in datamessage:
                if message == None:
                    message = d
                else:
                    message = message + " " + d

        if input[0].isdigit():
            userts = self.searchtsclid(input[0])
            self.poketsclient(input[0], message, adminb3)
            client.message('^3TeamSpeak Server ^2You poke: ^5%s'%(userts))
            client.message('^2message: ^5%s^7'%(message))

        else:

            tsuser=input[0].lower()
            
            if len(tsuser) < 3:
                client.message('^1Need a minimum of 3 characters for the TeamSpeak user name^7')            
                return
                
            n = 0
            lusers = None
            
            for cl in tslistclients:
                   
                if tsuser in cl.lower():

                    n = n + 1
                    clid = self.tsclid(cl)
                    if lusers == None:
                        clts = cl
                        lusers = "%s:%s"%(clid, cl)
                    else:
                        lusers = lusers + ", %s:%s"%(clid, cl)

            if n == 0:

                client.message('^1No Teamspeak User found^7')
            if n > 1:
                         
                client.message('^3User TeamSpeak found: ^2%s^7'%(lusers))
                    
            if n == 1:
                
                clid = self.tsclid(clts)
                self.poketsclient(clid, message, adminb3)
                client.message('^3TeamSpeak Server ^2You poke: ^5%s'%(clts))
                client.message('^2message: ^5%s^7'%(message))

    def cmd_ts3msg(self, data, client, cmd=None):
        
        """\
        ts3 message
        """

        adminb3=client.name.replace("|", "*")
        adminb3=client.name.replace("/", "*")
        adminb3=client.name.replace("\\", "*")

        clid = None        

        if data:
            
            input = data.split(" ")
        
        else:

            client.message('!ts3msg <teamspeak user> <message>')
            return

        listclients = None

        tslistclients = self.tslistclients()

        if len(input) < 2:
            message = "Hello !"

        else:
            message = None
            datamessage = input[1:]
            for d in datamessage:
                if message == None:
                    message = d
                else:
                    message = message + " " + d

        if input[0].isdigit():
            
            userts = self.searchtsclid(input[0])
            self.tsclientmsg(input[0], message, adminb3)
            client.message('^3TeamSpeak Server ^2Your message to ^5%s ^2:'%(userts))
            client.message('^5%s^7'%(message))

        else:

            tsuser=input[0].lower()
            
            if len(tsuser) < 3:
                client.message('^1Need a minimum of 3 characters for the TeamSpeak user name^7')            
                return
                
            n = 0
            lusers = None
            
            for cl in tslistclients:
                   
                if tsuser in cl.lower():

                    n = n + 1
                        
                    clid = self.tsclid(cl)
                    
                    if lusers == None:
                        clts = cl
                        lusers = "%s:%s"%(clid, cl)
                    else:
                        lusers = lusers + ", %s:%s"%(clid, cl)

            if n == 0:

                client.message('^1No Teamspeak User found^7')

            if n > 1:
                         
                client.message('^3User TeamSpeak found: ^2%s^7'%(lusers))
                    
            if n == 1:
                
                clid = self.tsclid(clts)
                self.tsclientmsg(clid, message, adminb3)
                client.message('^3TeamSpeak Server ^2Your message to ^5%s^2:'%(clts))
                client.message('^5%s^7'%(message))

    def cmd_ts3channelmsg(self, data, client, cmd=None):
        
        """\
        ts3 channel message
        """

        adminb3=client.name.replace("|", "*")
        adminb3=client.name.replace("/", "*")
        adminb3=client.name.replace("\\", "*")
        
        if data:
            
            input = data
        
        else:

            client.message('!ts3channelmsg <message>')
            return

        listclients = None

        tslistclients = self.tslistclients()

        message = input


        self.tschanmsg(message, adminb3)

        client.message('^3TeamSpeak Server ^2Your message to default Channel:')
        client.message('^5%s^7'%(message))

    def cmd_ts3ban(self, data, client, cmd=None):
        
        """\
        ts3 ban
        """

        adminb3=client.name.replace("|", "*")
        adminb3=client.name.replace("/", "*")
        adminb3=client.name.replace("\\", "*")

        clid = None        

        if data:
            
            input = data.split(" ")
        
        else:

            client.message('!ts3ban <teamspeak user> <reason> <duration>')
            client.message('duration: <#mxx><#hxx><#dxx><#wxx><#p>')
            client.message('ex: #m15 for 15 minutes, #h2 for 2 hours, #d3 for 3 days, #w5 for 5 weeks, #p for permanent')

            return
	
        listclients = None

        tslistclients = self.tslistclients()

        if len(input) < 2:
            
            reason = "You have been banned by %s"%client.name
            duree = "#p"

        elif len(input) < 3:

            datax = input[1]

            if datax[:2] in "#m, #h, #d, #w, #p":
                duree = datax
                reason = "You have been banned by %s"%client.name
            
            else:
                reason = None
                datareason = input[1:]
                duree = "#p"
				
                for d in datareason:
                    if reason == None:
                        reason = d
                    else:
                        reason = reason + " " + d

        elif len(input) >= 3:

            reason = None
            datax = input[-1:]
            datay = datax[0]

            if datay[:2] in "#m, #h, #d, #w, #p":
                duree = datay
                datareason = input[1:-1]
            else:
                duree = "#p"
                datareason = input[1:]

            for d in datareason:
                if reason == None:
                    reason = d
                else:
                    reason = reason + " " + d

        if duree == "#p":
            
            time = "permanent"
            xtime = " Permanent"
        
        else:

            if duree[:2] == "#m":
                time = int(duree[2:]) * 60
                xtime = " %s minute(s)"%duree[2:]
            if duree[:2] == "#h":
                time = int(duree[2:]) * 3600
                xtime = " %s hour(s)"%duree[2:]
            if duree[:2] == "#d":
                time = int(duree[2:]) * 86400
                xtime = " %s day(s)"%duree[2:]
            if duree[:2] == "#w":
                time = int(duree[2:]) * 604800
                xtime = " %s week(s)"%duree[2:]
    
        if input[0].isdigit():
 
            userts = self.searchtsclid(input[0])
            self.bantsclient(input[0], time, reason, adminb3)
            client.message('^3TeamSpeak Server ^2You banned: ^5%s ^1%s'%(userts, xtime))
            client.message('^2for ^5%s^7'%(reason))

        else:

            tsuser=input[0].lower()
            
            if len(tsuser) < 3:
                client.message('^1Need a minimum of 3 characters for the TeamSpeak user name^7')            
                return
                
            n = 0
            lusers = None
            
            for cl in tslistclients:
                   
                if tsuser in cl.lower():

                    n = n + 1
                    clid = self.tsclid(cl)
            
                    if lusers == None:
                        clts = cl
                        lusers = "%s:%s"%(clid, cl)
                    else:
                        lusers = lusers + ", %s:%s"%(clid, cl)

            if n == 0:

                client.message('^1No Teamspeak User found^7')

            if n > 1:
                         
                client.message('^3User TeamSpeak found: ^2%s^7'%(lusers))
                    
            if n == 1:
                
                clid = self.tsclid(clts)
                self.bantsclient(clid, time, reason, adminb3)
                client.message('^3TeamSpeak Server ^2You banned: ^5%s ^1%s'%(clts, xtime))
                client.message('^2for ^5%s^7'%(reason))

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

    def tslistclients(self):
	
        serverts3 = TS3Server(self._ts3adresse, self._ts3portquery, self._ts3virtualserverid)
        serverts3.login(self._ts3admin, self._ts3pwd)
        
        clientslist = serverts3.clientlist()
        listclients = []
        ip = None    
        for clientts in clientslist.values():
            dataclient = serverts3.send_command("clientinfo clid=%s"%clientts['clid'])
            for a in dataclient.data:
                ip = a['connection_client_ip']
            if ip != None:
                
                client = clientts['client_nickname']            
                client = client.replace('\xc3\xa9','e')
                client = client.replace('\xc3\xa8','e')
                client = client.decode('utf-8')

                listclients.append(client)
            
        return listclients

    def searchtsclid(self, clid):

        serverts3 = TS3Server(self._ts3adresse, self._ts3portquery, self._ts3virtualserverid)
        serverts3.login(self._ts3admin, self._ts3pwd)
        
        clientslist = serverts3.clientlist()
         
        for user in clientslist.values():
            cliduser = user['clid']
            if clid == cliduser:
                username = user['client_nickname']
            
        return username
        
    def kicktsclient(self, clid, reason, client):

        serverts3 = TS3Server(self._ts3adresse, self._ts3portquery, self._ts3virtualserverid)
        serverts3.login(self._ts3admin, self._ts3pwd)
        serverts3.send_command('clientupdate client_nickname=%s(B3)'%client)
        
        serverts3.send_command('clientkick', keys={'clid': clid, 'reasonid': 5, 'reasonmsg': reason})

    def bantsclient(self, clid, time, reason, client):
        
        serverts3 = TS3Server(self._ts3adresse, self._ts3portquery, self._ts3virtualserverid)
        serverts3.login(self._ts3admin, self._ts3pwd)
        serverts3.send_command('clientupdate client_nickname=%s(B3)'%client)
        if time == "permanent":
            serverts3.send_command('banclient', keys={'clid': clid, 'banreason': reason})
        else:

            serverts3.send_command('banclient', keys={'clid': clid, 'time': time, 'banreason': reason})

    def poketsclient(self, clid, message, client):

        serverts3 = TS3Server(self._ts3adresse, self._ts3portquery, self._ts3virtualserverid)
        serverts3.login(self._ts3admin, self._ts3pwd)
        serverts3.send_command('clientupdate client_nickname=%s(B3)'%client)

        serverts3.send_command('clientpoke', keys={'clid': clid, 'msg': message})

    def tschanmsg(self, message, client):

        serverts3 = TS3Server(self._ts3adresse, self._ts3portquery, self._ts3virtualserverid)
        serverts3.login(self._ts3admin, self._ts3pwd)
        serverts3.send_command('clientupdate client_nickname=%s(B3)'%client)

        serverts3.send_command('sendtextmessage', keys={'targetmode': 2,'msg': message})

    def tsclientmsg(self, clid, message, client):

        serverts3 = TS3Server(self._ts3adresse, self._ts3portquery, self._ts3virtualserverid)
        serverts3.login(self._ts3admin, self._ts3pwd)
        serverts3.send_command('clientupdate client_nickname=%s(B3)'%client)

        serverts3.send_command('sendtextmessage', keys={'targetmode': 1, 'target': clid, 'msg': message})
    
    def tsclid(self, tsuser):

        serverts3 = TS3Server(self._ts3adresse, self._ts3portquery, self._ts3virtualserverid)
        serverts3.login(self._ts3admin, self._ts3pwd)
        clientslist = serverts3.clientlist()

        for clientts in clientslist.values():

            if tsuser == clientts['client_nickname']:
                
                return clientts['clid']
				
   
