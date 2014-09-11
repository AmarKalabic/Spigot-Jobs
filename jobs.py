__plugin_name__ = "Jobs"
__plugin_version__ = "1.0"
__plugin_mainclass__ = "brix"

import os,math,re
from java.io import FileInputStream,File
from java.lang import String
from org.bukkit.util import Vector
from org.bukkit.configuration.file import YamlConfiguration
import org.bukkit as bukkit
from java.util.logging import Level
import java.util.ArrayList as ArrayList
import java.util.HashMap
import org.bukkit.block.Block
import org.bukkit.enchantments.Enchantment
import org.bukkit.Material
import org.bukkit.entity.Player
import org.bukkit.event.EventHandler
import org.bukkit.event.EventPriority
import org.bukkit.event.Listener
import org.bukkit.event.block.BlockBreakEvent
import org.bukkit.inventory.ItemStack as ItemStack
import org.bukkit.inventory.meta
import org.bukkit.event.entity.CreatureSpawnEvent
import org.bukkit.command.Command
import org.bukkit.command.CommandSender
import org.bukkit.entity.Player as player
import org.bukkit.event
import org.bukkit.event.player.PlayerInteractEvent
import org.bukkit.inventory.meta.ItemMeta
import org.bukkit.plugin.java.JavaPlugin
Material = bukkit.Material
import org.bukkit.block
import org.bukkit.entity
import org.bukkit.entity.EntityType
log = server.getLogger()
import org.bukkit.event.entity.EntityTargetEvent
from java.util import Random
import org.bukkit.event.entity.EntityDeathEvent
from random import randrange
from random import randint
import random
import java.awt.event.KeyEvent 
import warnings
import org.bukkit.event.entity.EntityDamageByEntityEvent
import org.bukkit.inventory.ShapedRecipe as ShapedRecipe
import org.bukkit.material.MaterialData as MaterialData
import org.bukkit.Bukkit
import org.bukkit.potion.PotionEffect as PotionEffect
import org.bukkit.potion.PotionEffectType as PotionEffectType
import org.bukkit.event.player.PlayerItemHeldEvent
import unicodedata

try:                                                          #
    from MySQLdb import *                                     # CIJELI MODUL NE RADI
except:                                                       # BEZ LINUX SETUP VERZIJE (CEKA SE DA PRORADI MASINA KAKO BIH ISTI GENERISAO)
	print "UPOZORENJE: Nije instaliran MySQLdb Python Modul!"   # DATUM: 11.9.2014
	raise                                                       # 

server = bukkit.Bukkit.getServer()

log = server.getLogger()
CHAT_PREFIX = "[Poslovi] "
def info(*text):
    log.log(Level.INFO,CHAT_PREFIX+" ".join(map(unicode,text)))
def severe(*text):
    log.log(Level.SEVERE,CHAT_PREFIX+" ".join(map(unicode,text)))
def msg(player,*text):
    player.sendMessage(CHAT_PREFIX+" ".join(map(unicode,text)))

CONSOLE = server.getConsoleSender()

db = MySQLdb.connect("ip_adresa","username","password","ime_baze")
cursor = db.cursor()


class brix(PythonPlugin):
    def __init__(self):
        PythonPlugin.__init__(self)
        self.api = None
        self.cfg = None
        self.folder = ""
        self.nameChecker = re.compile("^[a-zA-Z0-9\._]+$")
        
    def onEnable(self):
        pluginlokacija1 = os.path.realpath("%s/plugins"%os.getcwd())
        if os.path.isfile("%s/Jobs/config.yml"%pluginlokacija1):
           self.findFolder()
           self.cfg = YamlConfiguration.loadConfiguration(File(os.path.join(self.folder,"config.yml")))
        else:
            os.mkdir("%s/Jobs/"%pluginlokacija1)
            self.findFolder()
            self.cfg = YamlConfiguration.loadConfiguration(File(os.path.join(self.folder,"config.yml")))
            
    @hook.command("autoconfig", usage="/<command>", desc="Stvara novi config.")        
    def createConfig(sender, command, args):
        if sender.hasPermission("jobs.autocfg"):
           pluginlokacija2 = os.path.realpath("%s/plugins"%os.getcwd())
           fo = open("%s/Jobs/config.yml"%pluginlokacija2, "wb")
           fo.write("players:")
           fo.close
           sender.sendMessage("%sNovi config je generisan."%bukkit.ChatColor.DARK_AQUA)
 
    def findFolder(self):
          pluginfolder = os.path.split(self.dataFolder.toString())[0]
          for name in os.listdir(pluginfolder):
              if self.dataFolder.toString().lower() == os.path.join(pluginfolder,name).lower():
                 self.folder = os.path.join(pluginfolder,name)
                 
    def getCfg(self):
        getcfg = self.cfg
        return getcfg
                 
    @hook.event("player.PlayerInteractEvent", "HIGHEST")
    def onPlayerInteractEvent(event):
        clickedblock = event.getClickedBlock()
        clickedblock1 = event.getClickedBlock().getType()
        section = pyplugin.getCfg().getConfigurationSection("main")
        UUIDigraca = org.bukkit.Bukkit.getServer().getPlayerExact(event.getPlayer().getName()).getUniqueId()
        imeigraca = event.getPlayer().getName()
        if event.getClickedBlock().getType() == Material.SIGN or event.getClickedBlock().getType() == Material.SIGN_POST or event.getClickedBlock().getType() == Material.WALL_SIGN:
           if event.getPlayer().hasPermission("jobs.takejob"):
              sign = clickedblock.getState()
              name = bukkit.ChatColor.stripColor(sign.getLine(0))
              name1 = bukkit.ChatColor.stripColor(sign.getLine(2))
              if name == "[POSAO]" or name == "[Posao]":
                 if name1 == "Farmer": #dodati dodavanje igraca u MySQL bazu
                    #ostatak flat file storagea -> section.add("%s"%event.getPlayer().getName())
                    #ostatak flat file storagea -> section.getSection("main.%s"%event.getPlayer().getName()).add("FARMER")
                    sql = """INSERT INTO Igraci(UUID,
                             ime, job, level)
                             VALUES (%s, %s, 'Farmer', 1)"""%(UUIDigraca, imeigraca)
                    try:
                       cursor.execute(sql)
                       db.commit() # Comitta promjene u bazu
                    except:
                       db.rollback() #Rollbacka u slucaju errora
                    event.getPlayer().sendMessage("%sUzeo/la si posao %s%sFarmera %s%s. Jednom kada uzmes posao, ne mozes ga mijenjati!"%(bukkit.ChatColor.DARK_PURPLE, bukkit.ChatColor.BOLD, bukkit.ChatColor.LIGHT_PURPLE, bukkit.ChatColor.RESET, bukkit.ChatColor.DARK_PURPLE))
                 elif name1 == "Trgovac": #dodati dodavanje igraca u MySQL bazu
                      sql = """INSERT INTO Igraci(UUID,
                               ime, job, level)
                               VALUES (%s, %s, 'Trgovac', 1)"""%(UUIDigraca, imeigraca)
                      try:
                         cursor.execute(sql)
                         db.commit() # Comitta promjene u bazu
                      except:
                         db.rollback() #Rollbacka u slucaju errora
                      event.getPlayer().sendMessage("%sUzeo/la si posao %s%sTrgovca %s%s. Jednom kada uzmes posao, ne mozes ga mijenjati!"%(bukkit.ChatColor.DARK_PURPLE, bukkit.ChatColor.BOLD, bukkit.ChatColor.LIGHT_PURPLE, bukkit.ChatColor.RESET, bukkit.ChatColor.DARK_PURPLE))
                 elif name1 == "Rudar": #dodati dodavanje igraca u MySQL bazu
                      sql = """INSERT INTO Igraci(UUID,
                               ime, job, level)
                               VALUES (%s, %s, 'Rudar', 1)"""%(UUIDigraca, imeigraca)
                      try:
                         cursor.execute(sql)
                         db.commit() # Comitta promjene u bazu
                      except:
                         db.rollback() #Rollbacka u slucaju errora
                      event.getPlayer().sendMessage("%sUzeo/la si posao %s%sRudara %s%s. Jednom kada uzmes posao, ne mozes ga mijenjati!"%(bukkit.ChatColor.DARK_PURPLE, bukkit.ChatColor.BOLD, bukkit.ChatColor.LIGHT_PURPLE, bukkit.ChatColor.RESET, bukkit.ChatColor.DARK_PURPLE))
                 else:
                 	print "Postoji problem sa znakom na lokaciji: %s"%event.getPlayer().getLocation()
                 	server.dispatchCommand(org.bukkit.Bukkit.getServer().getConsoleSender(), "helpop [POSLOVI] Postoji problem sa znakom na lokaciji: %s"%(event.getPlayer().getLocation()))
                 	event.getPlayer().sendMessage("%sDoslo je do problema."%bukkit.ChatColor.RED)
                 	event.getPlayer().sendMessage("%sAdministrator je obavjesten o istom, ali ga mozes i ti podsjetiti"%bukkit.ChatColor.RED)
              else:
                  pass
           else:
                event.getPlayer().sendMessage("%sNemas prava da uzmes taj posao!"%bukkit.ChatColor.RED)
                event.getPlayer().sendMessage("%sAko mislis da je ovo greska, obrati se administratoru!"%bukkit.ChatColor.RED)
        else:
             pass