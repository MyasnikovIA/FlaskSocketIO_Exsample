from bs4 import BeautifulSoup as BS

class subObjPars:
    ind = 0
    max = 0
    formLines = []
    proxy = {}


def DFM(txt, printRes=False):
    info = subObjPars()
    info.formLines = txt.split('\n')
    info.max = len(info.formLines) - 1
    info.ind += 1
    line = info.formLines[info.ind]
    obj = {}
    obj['objectName'] = line[line.rfind('object ') + len('object '):line.rfind(':')]
    obj['objectClass'] = line[line.rfind(': ') + 2:].lower()
    obj['property'] = {}
    obj['child'] = []
    DFMsubObj(obj, None, info, 0)
    html = parseJsonToHtml(obj)
    soup = BS(html, "html.parser")
    if printRes == True:
        print(soup.prettify())
        return
    else:
        return soup.prettify()

def parseJsonToHtml(objhtml):
    prop = []
    prop.append('<%s  name="%s" ' % (objhtml['objectClass'], objhtml['objectName']))
    for propName in objhtml['property']:
        prop.append(' %s="%s" ' % (propName, objhtml['property'][propName]) )
    prop.append('>')
    for subObj in objhtml['child']:
        prop.append(parseJsonToHtml(subObj))
    prop.append('</%s>' % objhtml['objectClass'])
    return "".join(prop)

def DFMsubObj(obj, parent, info, lavelobject):
    while True:
        info.ind += 1
        if info.max == info.ind:
            break
        line = info.formLines[info.ind]
        lineArr = line.split()
        nextline = info.formLines[info.ind + 1]
        operName = lineArr[0];
        lavel = line.find(operName)
        lavelnext = nextline.find(nextline.split()[0])
        if operName == "object":
            subobj = {}
            subobj['objectName'] = line[line.rfind('object ') + len('object '):line.rfind(':')]
            subobj['objectClass'] = line[line.rfind(': ') + 2:].lower()
            subobj['property'] = {}
            subobj['child'] = []
            obj['child'].append(subobj)
            DFMsubObj(subobj, obj, info, lavel)
        if lineArr[0] == 'end':
            break
        if ((' = ' in line) & (lineArr[1] == '=')):
            propName = line.split()[0];
            propVal = line[line.find(' = ') + 3:]
            if ((propVal[0] == "'") & (propVal[-1] == "'")):
                propVal = propVal[1:-1]
            obj['property'][propName] = propVal.replace('"', '""')
