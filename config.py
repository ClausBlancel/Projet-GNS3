import xml.etree.ElementTree as ET

configfile = 'routeurs.xml'

def initXML():
    tree = ET.parse(configfile)
    return tree.getroot()

def getRouterName(root, nb):
    return root[0][nb].get('name')

def getInterfaceAddress(root, router):
    return root[0][router]

if __name__ == "__main__":
    root = initXML()
    print(getRouterName(root, 1))
    print(getInterfaceAddress(root, 1))