

import os
import configparser


configParser = configparser.RawConfigParser()
configFilePath = os.path.join(os.path.dirname(__file__), 'Configure.cfg')
configParser.read(configFilePath)
scWidth  = int(configParser.get("info","Screen width"))
scHeight = int(configParser.get("info","Screen height"))
rHeight=int(configParser.get("info","Racket height"))
rWidth=int(configParser.get("info","Racket width"))
ballsize=int(configParser.get("info","Ball size"))
diff=int(configParser.get("info","Difficulty"))
comp=int(configParser.get("info","Computer"))
ballspeed=int(configParser.get("info","Ball speed"))
print(scHeight)

#odczytanie konfiguracji z pliku cfg
