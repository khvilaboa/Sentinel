# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import urllib2
import sys, csv, pyproj
reload(sys)
sys.setdefaultencoding('utf8')

cr = csv.reader(open("intens_points.csv", "rb"), delimiter=";")
coords = {row[0]:(row[4], row[5]) for row in cr}

e = ET.ElementTree(file=urllib2.urlopen('http://informo.munimadrid.es/informo/tmadrid/pm.xml'))
#e = xml.etree.ElementTree.parse('pm.xml').getroot()
pms = [l for l in e.findall("pm")]

cont = 0
res = {}


kl = ["codigo", "descripcion", "intensidad", "ocupacion", "carga", "accesoAsociado", "nivelServicio", "subarea", "intensidadSat"]
#f = open("out", "wb")

elipsoide1 = "intl"

for pm in pms:
    pmc = pm.getchildren()
    tags = map(lambda x: x.tag, pmc)
    texts = map(lambda x: x.text, pmc)
    
    if any([t not in tags for t in kl]):
        continue
        
    for ind, t in enumerate(texts):
        if t is None:
            if ind == 1:
                texts[ind] = ""
            else:
                texts[ind] = -1
                
    if texts[1] == "":
        continue
        
    if cont == 3:
        break
        
    cont += 1
    #print texts
    code = texts[tags.index("codigo")]

    utm_x, utm_y = map(lambda x: float(x.replace(",", ".")), list(coords[code]))
    huso = 30
    srcProj = pyproj.Proj(proj="utm", zone=huso, ellps=elipsoide1, units="m")
    dstProj = pyproj.Proj(proj='longlat', ellps='WGS84', datum='WGS84')
    long,lat = pyproj.transform(srcProj, dstProj, utm_x, utm_y)
    res[code] = [texts[tags.index(ke)] if ind == 1 else int(texts[tags.index(ke)]) for ind,ke in enumerate(kl)] + [long, lat]
    #print(url % texts[tags.index("descripcion")].replace(" ", "%20"))
#f.close()
print cont
#print res