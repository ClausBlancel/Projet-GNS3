import xml.etree.ElementTree as ET

configfile = 'routeurs.xml'

def initXML():
    tree = ET.parse(configfile)
    return tree.getroot()

def getRouterName(root, nb):
    return root[0][nb].get('hostname')

def getInterfaceAddress(root, router, nbInterface):
    return root[0][router][nbInterface][2].text

def getRoutersInAS(root, ASnumber):
    lRouters = []
    for router in root[1][ASnumber].iter('contains'):
        lRouters.append(router.text)
    return lRouters

def getASProtocol(root, ASnumber):
    return root.find('./AutonomousSystems/AS[@name="' + ASnumber + '"]/protocol').text

if __name__ == "__main__":
    root = initXML()