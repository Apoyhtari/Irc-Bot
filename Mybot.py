# -*- coding: iso-8859-15 -*

import socket
import sqlite3
import time
import urllib2
import random
import time
import datetime
import pyreadline
from bs4 import BeautifulSoup

class DB(object):
   def __init__(self):
        self.db_path = 'lollipopguild.db'
        self.define_table = 'define'

        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()

        sql = 'create table if not exists ' + self.define_table + ' (id integer primary key, key text, value text, epoch_timestamp text)'
        self.c.execute(sql)

        self.c.close()
        self.conn.close()
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()

        
   def get_defines(self, key):
        
        return_list = []
        for row in self.c.execute('SELECT * FROM ' + self.define_table + ' WHERE key=?', (key.decode('iso-8859-15'),)):
            return_list.append({"id":row[0],"key":row[1].encode('iso-8859-15'),"value":row[2].encode('iso-8859-15'), "epoch_timestamp":row[3]})

        return return_list

   def insert_define(self, key, value):
        epoch_timestamp = time.time()
        self.c.execute("INSERT INTO " + self.define_table + " VALUES (NULL,?,?,?)", (key.decode("iso-8859-15"),
            value.decode("iso-8859-15"),epoch_timestamp))
        self.conn.commit()

   
        

class Mybot(object):    

   def __init__(self):
      self.DB = DB()
      network = 'irc.suomi.net'
      port = 6667
      self.irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
      self.irc.connect ( ( network, port ) )
      
      self.irc.send ( 'NICK testibotti\r\n' )
      self.irc.send ( 'USER botty botty botty :Python IRC\r\n' )
      self.irc.send ( 'JOIN #lollipopguild\r\n' )
      
        
   def handle_message(self, connection, event):
        msg = event.arguments()[0]
        if event.target()[0] != "#":
            return
        if msg[0] != "!":
            return
        
        author = event.source().split("!")[0]
        target = event.target()
        command, key, value = Parser.parse(msg)
        output = []

        if command == "define":     
            output = self._handle_define(key, value)

        elif command == "get":
            output = self._handle_get(key)
   def _handle_define(self, key, value):
        if key is "" or value is "":
            return ["Key or value missing."]
        self.DB.insert_define(key,value)
        return ['"' + key.lower() + '" defined.']

   def _handle_get(self, key):
        output = []
        if key is "":
            return ["Key missing."]
        defines = self.DB.get_defines(key)
        count = 1
        for define in defines:
            def_str = key + "[" + str(count) + "]: " + define["value"]
            output.append(def_str)
            count = count + 1
        if count == 1:
            output.append("'" + key + "' not found.")
        return output

   

   def getweather(self):
       
       html =urllib2.urlopen( 'http://weather.willab.fi/weather.html')
       soup=BeautifulSoup(html)
       newdoc = soup.find('p', class_="tempnow")
       self.irc.send('PRIVMSG #lollipopguild :Current weather in Linnanmaa:' +" " +newdoc.text.encode('iso-8859-15')+ '\r\n')
       
   def gettitle(self, url):
        
       
       html = urllib2.urlopen(url)
       soup=BeautifulSoup(html)
       newdoc = soup.find('title')
       print newdoc
       try:
          self.irc.send('PRIVMSG #lollipopguild :title:' +" " +newdoc.text.encode('iso-8859-15')+ '\r\n')
       except:
          print ("luls")
      
   def quote(self):
       try:
          import pyreadline as readline
       except ImportError:
          import readline
         
       from random import randint
       rng = 0
       rng = random.randint(0, 26)
       filename = open("C:\Users\Aleksi\Desktop\irkkibotti\irc-bot1\quotes.txt")
       line = filename.readlines()
      
       self.irc.send('PRIVMSG #lollipopguild :' +" " + str(line [rng])+'\r\n')
       filename.close()
    #This insult function is not done by me. Thanks for this go to Juho "Mutjake" Myllylahti
   def insult(self):
      insults = """artless             base-court          apple-john
   bawdy               bat-fowling         baggage
   beslubbering        beef-witted         barnacle
   bootless            beetle-headed       bladder
   churlish            boil-brained        boar-pig
   cockered            clapper-clawed      bugbear
   clouted             clay-brained        bum-bailey
   craven              common-kissing      canker-blossom
   currish             crook-pated         clack-dish
   dankish             dismal-dreaming     clotpole
   dissembling         dizzy-eyed          coxcomb
   droning             doghearted          codpiece
   errant              dread-bolted        death-token
   fawning             earth-vexing        dewberry
   fobbing             elf-skinned         flap-dragon
   froward             fat-kidneyed        flax-wench
   frothy              fen-sucked          flirt-gill
   gleeking            flap-mouthed        foot-licker
   goatish             fly-bitten          fustilarian
   gorbellied          folly-fallen        giglet
   impertinent         fool-born           gudgeon
   infectious          full-gorged         haggard
   jarring             guts-griping        harpy
   loggerheaded        half-faced          hedge-pig
   lumpish             hasty-witted        horn-beast
   mammering           hedge-born          hugger-mugger
   mangled             hell-hated          joithead
   mewling             idle-headed         lewdster
   paunchy             ill-breeding        lout
   pribbling           ill-nurtured        maggot-pie
   puking              knotty-pated        malt-worm
   puny                milk-livered        mammet
   qualling            motley-minded       measle
   rank                onion-eyed          minnow
   reeky               plume-plucked       miscreant
   roguish             pottle-deep         moldwarp
   ruttish             pox-marked          mumble-news
   saucy               reeling-ripe        nut-hook
   spleeny             rough-hewn          pigeon-egg
   spongy              rude-growing        pignut
   surly               rump-fed            puttock
   tottering           shard-borne         pumpion
   unmuzzled           sheep-biting        ratsbane
   vain                spur-galled         scut
   venomed             swag-bellied        skainsmate
   villainous          tardy-gaited        strumpet
   warped              tickle-brained      varlot
   wayward             toad-spotted        vassal
   weedy               unchin-snouted      whey-face
   yeasty              weather-bitten      wagtail
   cullionly           whoreson            knave
   fusty               malmsey-nosed       blind-worm
   caluminous          rampallian          popinjay
   wimpled             lily-livered        scullian
   burly-boned         scurvy-valiant      jolt-head
   misbegotten         brazen-faced        malcontent
   odiferous           unwash'd            devil-monk
   poisonous           bunch-back'd        toad
   fishified           leaden-footed       rascal
   Wart-necked         muddy-mettled       Basket-Cockle"""
 
 
# -> ["artless             base-court          apple-john",
#     "bawdy               bat-fowling         baggage" ...]
      insults = insults.split("\n")
 
      insults = map(lambda x: x.split(" "), insults)
# -> [["artless", "", "", ..., "basecourt", "", ...], ...]
 
      insults = map(lambda x: filter(lambda y: len(y) > 0, x), insults)
# -> [["artless, "basecourt", "apple-john"], ...]
 
      first_adj_list = map(lambda x: x[0], insults)
      second_adj_list = map(lambda x: x[1], insults)
      noun_list = map(lambda x: x[2], insults)
 
# first_adj_list = ["artless", "bawdy", ...]
# second_adj_list = ["base-court", "bat-fowling", ...]
# noun_list = ["apple-john", "baggage", ...]
 
   
      print_str = "Thou "
      print_str += random.choice(first_adj_list)
      print_str += " "
      print_str += random.choice(second_adj_list)
      print_str += " "
      print_str += random.choice(noun_list)
      print_str += "!"
 
      print print_str
      self.irc.send('PRIVMSG #lollipopguild :'+ print_str + '\r\n')

       
   def date(self):
       now = datetime.datetime.now()
       self.irc.send('PRIVMSG #lollipopguild :Current date is:'+" "+ str(now) [:10]+ '\r\n')
                    
   def randomnumber(self):
       from random import randint

       rgn = 0
       rgn = random.randint(0, 1000)
       self.irc.send('PRIVMSG #lollipopguild :Here is your randomly generated number:'+ " " + str(rgn)+ '\r\n')
      
   
       
   
   @classmethod
   def _output_lines_to_irc(cls, rows, connection, target):
        for row in rows:
            connection.privmsg(target, row)

   def processForever(self):
     while True:
       data = self.irc.recv (1024)
       #crude as hell but it works
       if data.find ( 'PING' ) != -1:
          self.irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
       if data.find ( '!testibotti quit') != -1:
          self.irc.send ( 'PRIVMSG #lollipopguild :Fine, if you do not want me\r\n' )
          self.irc.send ( 'QUIT\r\n' )
       if data.find('!randomnumber')!=-1:
          self.randomnumber()
       if data.find('<3') !=-1:
          self.irc.send('PRIVMSG #lollipopguild :L�LLYYYYYYYYYY!!!\r\n')
       if data.find('!date')!=-1:
          self.date()
       if data.find('!quote')!=-1:
          self.quote()
       if data.find('!insult') !=-1:
          self.insult();
       if data.find('Kaira-' + 'DRM' + 'steam') !=-1:
          self.irc.send('Shut yer trap, ye stinking hippie!!!') 
       if data.find ( 'hi testibotti' ) != -1:
          self.irc.send ( 'PRIVMSG #lollipopguild ' + data.split('!') [0] + ': I already said hi...\r\n'  )
       if data.find ( 'Hello testibotti' ) != -1:
          self.irc.send ( 'PRIVMSG #lollipopguild ' + data.split('!') [0] +': I already said hi...\r\n' )
       if data.find ( 'KICK' ) != -1:
          self.irc.send ( 'JOIN #lollipopguild\r\n' )
       if data.find ( 'Cheese' ) != -1:
          self.irc.send ( 'PRIVMSG #lollipopguild ' + data.split('!') [0] + ': WHERE!!!!!!\r\n' )
       if data.find ( 'slaps testibotti' ) != -1:
          self.irc.send ( 'PRIVMSG #lollipopguild ' + data.split('!') [0] + ': Why did you do that? :(\r\n' )
       if data.find('ohayoo') != -1:
          self.irc.send (' PRIVMSG #lollipopguild ' + data.split('!') [0] + ': Ohayoo gozaimasu!\r\n')
       if data.find ('Tu tu ru') != -1:
          self.irc.send (' PRIVMSG #lollipopguild ' + data.split('!') [0] +  ': Tu tu ru~\r\n')
       if data.find('!party')!= -1:
          self.irc.send('PRIVMSG #lollipopguild : OOOOOOOH YEEEEEEEEEAH *RaivoRaimo puts on some good music*\r\n ')
       if data.find ('!gangnam')!=-1:
          self.irc.send('PRIVMSG #lollipopguild : OPPA GANGNAM STYLE! http://www.youtube.com/watch?v=9bZkp7q19f0\r\n')
       if data.find ('!halp') != -1:
          self.irc.send ('PRIVMSG #lollipopguild :every command starts with "!"\r\n  ')
          self.irc.send ('PRIVMSG #lollipopguild :define lets you place definitions in to the database.\r\n')
          self.irc.send ('PRIVMSG #lollipopguild :get lets you pull information out of the database.\r\n')
          self.irc.send ('PRIVMSG #lollipopguild :party command will cause Raimo to go nuts.\r\n')
          self.irc.send ('PRIVMSG #lollipopguild :weather command gives you the current weather in linnnanmaa.\r\n')
          self.irc.send ('PRIVMSG #lollipopguild :date gives you the current date\r\n')
          self.irc.send ('PRIVMSG #lollipopguild :quote will give you a random famous people quote.\r\n')
          self.irc.send ('PRIVMSG #lollipopguild :intro will introduce testibotti\r\n')
       if data.find('http://www.youtube.com') !=-1:
          print ("yay got here")
          elements = data.split(' ')
          print elements
          for element in elements:
        #find URLs
             if element.startswith(':http://www.youtube.com'):
               url = self.gettitle(element[1:])
       if data.find('https://www.youtube.com') !=-1:
          print ("yay got here")
          elements = data.split(' ')
          print elements
          for element in elements:
        #find URLs
             if element.startswith(':https://www.youtube.com'):
               url = self.gettitle(element[1:])
       if data.find('!weather') !=-1:
          self.getweather()
       if data.find('!fibonacci') !=-1:
          self.fibo()
       if data.find ('!intro') !=-1:
          self.irc.send( ' PRIVMSG #lollipopguild :I am testibotti, bot extraordinaire and a gentleman! I can do tricks when my lazy ass creator implements them. I also use a define-database for your convenience.\r\nYou can also type !halp for more information.')
       if data.find ('!define') != -1:
         
          #insert into db data
          command, key, value = Parser.parse(data.split (" ", 2) [2][:-2])
          self.DB.insert_define(key, value)
          
          self.irc.send ('PRIVMSG #lollipopguild :' + " " +key.encode('iso-8859-15')+ ' defined \r\n')

          
       if data.find('!get') != -1:
          command, key, value = Parser.parse(data.split (" ", 2) [2] [:-2])
          #get data from db
          output = self._handle_get(key)
     
          for define in output:
             
             out_str = ('PRIVMSG #lollipopguild :' + " " +define+ '\r\n')
             self.irc.send (out_str)
             time.sleep(1)
             
             
       print data
       
        
#parsing the data for database
class Parser(object):
    @classmethod
    def parse(cls, row):

        
        split_list = row.split(" ", 3)
        command = split_list[1][:] # skip the first character
        command = command.lower()
        key = ""
        if len(split_list) > 2:
            key = split_list[2] [:]
            key = key.lower()
        value = ""
        if len(split_list) > 3:
            value = split_list[3]
        return command, key, value

#program starts actually from here
ib = Mybot()
ib.processForever()
