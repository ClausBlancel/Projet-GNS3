import os
import xml.etree.ElementTree as ET
import re

# fichier xml qui regroupe 
configfile = './routeurs.xml'

# definir les fonctions dont on aura besoin dans le main
def initXML():
    tree = ET.parse(configfile) # transforme le fichier en ElementTree
    root = tree.getroot() # selectionne la racine de l'arbre à elements (l'ET)
    return tree, root

def getRouterName(router): #A jour
    """_summary_ : Gets the name of a router

    Args:
        router (ET.Element): the router

    Returns:
        string: its name
    """
    return router.get('hostname')

def getRouterNumber(router) : #A jour
    """_summary_ : Gets the number of a router

    Args:
        router (ET.Element): the router

    Returns:
        string: its number
    """
    return router.get('Rnumber')

def getNeighbors(router) : #A jour
    """_summary_ : Gets the neighbors of a router

    Args:
        router (ET.Element): the router

    Returns:
        list: its neighbors
    """
    lNeighbors = []
    for i in router :
        lNeighbors.append(i.find('neighbor').text)
    return lNeighbors

def getInterfaceAddress(interface):
    """_summary_ : Gets the ipv6 address of an interface

    Args:
        interface (ET.Element): the interface

    Returns:
        string: its ipv6 address
    """
    return interface.find('address')

def getInterfaceType (interface) :
    type =interface.find('type').text
    return type

def getInterfaceNumber(interface):
    number = interface.get('number')
    return number

def getInterfaceAddress(interface):
    address = interface.find('address').text
    return address

def getInterfaceNei(interface):
    """_summary_ : Gets the neighbor of an interface

    Args:
        interface (ET.Element): the interface

    Returns:
        string: its neighbor (the router's name)
    """
    return interface.find('neighbor').text

def getInterfaceFromNei(router, nei):
    """_summary_ : Gets the interface of a router's neighbor

    Args:
        router (ET.Element): the router
        nei (ET.Element): the neighbor

    Returns:
        ET.Element: the interface
    """
    res,n = (0, 0)
    for i in router :
        voisin = getInterfaceNei(i)
        if voisin == nei :
            res = n
        n+=1
    #print(res)
    return router[res]

def getASInterfQtty(root, AS) :
    ASnumber = getASName_int(root, AS)
    i = getASPosition(root, ASnumber)

    # Initialize a count variable
    interface_count = 0

    # Iterate over all elements in the XML file
    for element in root[i].iter():
        # Check if the element is an interface
        if element.tag == 'interface' :
            interface_count += 1

    return interface_count

def getASList(root):
    """_summary_ : Gets the list of AS

    Args:
        root (ET.Element): the root of the XML tree

    Returns:
        list: the list of AS
    """
    lAS = []
    for AS in root.iter('AS'):
        name = getASName_int(root, AS)
        lAS.append(name)
    return lAS

def getASPosition(root, ASnumber) : #A jour
    """_summary_ : Gets the position of an AS in the XML tree

    Args:
        root (ET.Element): the root of the XML tree
        ASnumber (int): the number of the AS

    Returns:
        int: the position of the AS in the XML tree
    """
    for i in range(len(root)) :
        name = root[i].get('name')
        if ASnumber == int(name) : return i  

def getRoutersInAS(root, ASnumber): #A jour
    """_summary_ : Gets the routers in an AS

    Args:
        root (ET.Element): the root of the XML tree
        ASnumber (int): the number of the AS

    Returns:
        list: the list of routers in the AS
    """
    lRouters = []
    n = getASPosition(root, ASnumber)

    for router in root[n].iter('router'):
        lRouters.append(str(getRouterName(router)))
    return lRouters

def getASLinksNum(root, ASnumber) : #A jour
    """_summary_ : Gets the number of links of an AS

    Args:
        root (ET.Element): the root of the XML tree
        ASnumber (int): the number of the AS

    Returns:
        int: the number of links of the AS
    """
    i = getASPosition(root, ASnumber)
    return int((root[i]).get('nblinks'))

def getASProtocol(root, ASnumber): #A jour
    """_summary_ : Gets the protocol of an AS

    Args:
        root (ET.Element): the root of the XML tree
        ASnumber (int): the number of the AS

    Returns:
        string: the protocol of the AS
    """
    i = getASPosition(root, ASnumber)
    return (root[i]).get('protocol')

def getASAddress(root, ASnumber): #Defectueux
    """_summary_ : Gets the addressing of an AS

    Args:
        root (ET.Element): the root of the XML tree
        ASnumber (int): the number of the AS

    Returns:
        string: the addressing of the AS
    """
    i = getASPosition(root, ASnumber)
    return (root[i]).get('addressing')

def getASPrefix(root, ASnumber):
    """_summary_ : Gets the prefix of an AS

    Args:
        root (ET.Element): the root of the XML tree
        ASnumber (int): the number of the AS

    Returns:
        string: the prefix of the AS
    """
    i = getASPosition(root, ASnumber)
    return (root[i]).get('prefix')

def getASName_str(root, AS) : #A jour
    """_summary_ : Gets the name of an AS

    Args:
        root (ET.Element): the root of the XML tree
        ASnumber (int): the number of the AS

    Returns:
        int: the name of the AS
    """
    return str(AS.get('name'))

def getASName_int(root, AS) : #A jour
    """_summary_ : Gets the name of an AS

    Args:
        root (ET.Element): the root of the XML tree
        ASnumber (int): the number of the AS

    Returns:
        int: the name of the AS
    """
    return int(AS.get('name'))

def getASQtty (root) :
    return int(root.get('qtty'))

def getFileName(router) : #A jour
    """_summary_ : Gets the name of the file of a router
    
    Args:
        router (ET.Element): the router
        
    Returns:
        string: the name of the file
    """
    number = router.get('Rnumber')
    fileName = 'i'+number+'_startup-config.cfg'
    return fileName

def getFilePath(router) :
    pass

def openConfFile(router) : #A jour
    """_summary_ : Opens the configuration file of a router

    Args:
        router (ET.Element): the router

    Returns:
        io.TextIOWrapper: the configuration file
    """
    filePath = getFilePath(router)
    return open(filePath, "a")

def setAddresses(root, AS):
    ASnumber_int = getASName_int(root, AS)
    ASInterfacesQtty = getASInterfQtty(root, AS)
    prefix = getASPrefix(root, ASnumber_int)

    i = 1



    for router in AS:
        for interface in router :
            address = prefix + str(i)

            # Find the element to add/modify
            elem_to_modify = interface.find("address")

            # If the element already exists
            if elem_to_modify is not None :
                # Modify the element's attribute
                elem_to_modify.text = address
            else :
                new_line_element = ET.Element("address")
                new_line_element.text = address
                interface.append(new_line_element)
            i+=1

    tree.write(configfile, xml_declaration=True, encoding='utf-8', method="xml")

def writeAddresses(AS, router, interface, f, tree):
    """_summary_ : Writes the addresses of an interface in the configuration file

    Args:
        router (ET.Element): the router
        interface (ET.Element): the interface
        f (io.TextIOWrapper): the configuration file
    """
    hostname = getRouterName(router)   


    f.write("interface "+getInterfaceType(interface)+getInterfaceNumber(interface)+"/0\n")
    f.write(" no ip address\n")

    if int(interface.get('number')) == 0 :
        f.write(" duplex full\n")
    else :
        f.write(" negotiation auto\n")

    f.write(" ipv6 address "+getInterfaceAddress(interface)+"/64\n")
    f.write(" ipv6 enable\n")
    enableProtocolInterface(root, router, f)

    f.write("!\n")

def enableProtocolInterface(root, router, f) :
    ASN = getASNOfRouter(root, router)
    protocol = getASProtocol(root, ASN)

    if protocol == "RIPNG" :
        f.write(" ipv6 rip ripng enable\n")
    elif protocol == "OSPFv3" :
        f.write(" ipv6 ospf 7 area 0\n")


def defaultInfoHead(f, router):
    """_summary_ : Writes the default information header of the configuration file

    Args:
        f (io.TextIOWrapper): the configuration file
        router (ET.Element): the router
    """
    f.write("service timestamps debug datetime msec\nservice timestamps log datetime msec\n!\nhostname "+getRouterName(router)+"\n!\nboot-start-marker\nboot-end-marker\n!\n!\n!\nno aaa new-model\nno ip icmp rate-limit unreachable\nip cef\n!\n!\n!\nno ip domain lookup\nipv6 unicast-routing\nipv6 cef\n!\n!\n!\nmultilink bundle-name authenticated\n!\n!\n!\nip tcp synwait-time 5\n!\n!\n!\n")

def defaultInfoFoot(f, router):
    """_summary_ : Writes the default information footer of the configuration file

    Args:
        f (io.TextIOWrapper): the configuration file
        router (ET.Element): the router
    """
    hostname = getRouterName(router)
    f.write("ip forward-protocol nd\nno ip http server\nno ip http secure-server\n")
    found = False
    for routersAS in root[0].iter('router'):
        if routersAS.get('hostname') == hostname :
            f.write("!\nipv6 router rip ripng\n redistribute connected\n")
            found = True
    if not found :
        for routersAS in root[1].iter('router'):
            if routersAS.get('hostname') == hostname :
                n = router.get('Rnumber')
                f.write("!\nipv6 router ospf 7\n router-id "+n+"."+n+"."+n+"."+n+"\n")
    f.write("!\n!\ncontrol-plane\n!\n!\nline con 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\nline aux 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\nline vty 0 4\n login\n!\n!\nend\n")

def getRoutersArray(root): #Non utilisé pour l'instant : pas de description
    rows = getASQtty(root)
    cols = 1
    for AS in root.iter('AS') :
        if int(AS.get('nbrouters')) > cols :
            cols = int(AS.get('nbrouters'))
        
    # print(rows, cols)
    arr = [[0 for i in range(cols)] for j in range(rows)]
    # print(arr[0] is arr[1])

    #for router in root.iter('router') :

    for i in range(len(root)) :
        for j in range(len(root[i])) :
            arr[i][j]=root[i][j].get('hostname')
            # print(arr[i][j])

    return arr

def getAllRouters(root):
    lAS = getASList(root)
    lR = []

    for i in range(getASQtty(root)) :
        lR.append(getRoutersInAS(root,lAS[i]))
    
    return lR

def getASNOfRouter(root, router): #A jour
    """_summary_ : Gets the AS of a router

    Args:
        root (ET.Element): the root of the XML tree
        router (ET.Element): the router

    Returns:
        int: the AS of the router
    """

    l = getAllRouters(root)

    
    hostname = getRouterName(router)


    for i in range(len(l)) :
        if hostname in l[i] :
            return i+1
            break

            

def getAdjacentAS(root, router):
    l = getAllRouters(root)
    border, borderNei, address_ebgp = isBorderRouter(root, router)
    if border :
        for i in range(len(l)) :
            if borderNei in l[i] :
                return i+1
                break


def getOtherASes(router): 
    pass

def isBorderRouter(root, router) : #A jour
    """_summary_ : Checks if a router is a border router

    Args:
        root (ET.Element): the root of the XML tree
        router (ET.Element): the router

    Returns:
        (bool, ET.Element, string): boolean indicating if the router is a border router, the neighbor router that is not in the same AS and the address of the ebgp session
    """
    hostname = getRouterName(router)
    lNeighbors = getNeighbors(router)
    CurrentAS = getASNOfRouter(root, router)
    # print(CurrentAS)
    CurrentASRouters = getRoutersInAS(root, CurrentAS)
    border = False
    Router = 'None'
    address_ebgp = 'None'
    i = 0

    for rtr in lNeighbors :
        if rtr not in CurrentASRouters :
            border = True
            Router = lNeighbors[i]
        i+=1

    address_ebgp = str(getInterfaceFromNei(router, Router).find('address').text)
    return (border,Router,address_ebgp)
    
def deployProtocol(root, router):
    """_summary_ : Writes the protocol configuration of the router

    Args:
        root (ET.Element): the root of the XML tree
        router (ET.Element): the router
    """
    hostname = getRouterName(router)
    n = getRouterNumber(router)
    ASN = getASNOfRouter(root, router)
    ASNs = str(ASN)
    border, borderNei, address_ebgp = isBorderRouter(root, router)

    OASN = getAdjacentAS(root, router)
    OASNs = str(OASN)


    f.write("router bgp "+ ASNs+"\n")
    f.write(" bgp router-id "+n+"."+n+"."+n+"."+n+"\n")
    f.write(" bgp log-neighbor-changes\n")
    f.write(" no bgp default ipv4-unicast\n")

    if border : 
        for interface in router :
            if interface.find('neighbor').text != borderNei :
                f.write(" neighbor "+getInterfaceAddress(interface)+" remote-as "+ASNs+"\n")
            else :
                f.write(" neighbor "+getInterfaceAddress(interface)+" remote-as "+ OASNs+"\n")

    else : 
        for interface in router :
            f.write(" neighbor "+getInterfaceAddress(interface)+" remote-as "+ASNs+"\n")
        
    f.write(" !\n")
    f.write(" address-family ipv4\n")
    f.write(" exit-address-family\n")
    f.write(" !\n")
    f.write(" address-family ipv6\n")

    if border :
        address = getASAddress(root, ASN)
        address = address[0:11]
        # print(address)

        nblinks = getASLinksNum(root, ASN)
        for i in range(1,nblinks+1) :
            f.write("  network "+address+str(i)+"::/64\n")

        # adresse de la liaison interAS :
        network_ebgp = address_ebgp[:-1]
        f.write("  network "+network_ebgp+"/64\n")


    for interface in router :
        f.write("  neighbor "+getInterfaceAddress(interface)+" activate\n")
    f.write(" exit-address-family\n")
    f.write("!\n")


def getConfigFilesPaths(directory, confFiles):
    """_summary_ : Returns a list of paths to all config files from a directory

    Args:
        directory (string): path to starting directory
    """
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    dirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    if files != []:
        for f in files:
            if re.match(r'i[0-9]*_startup-config.cfg', f):
                confFiles.append(os.path.join(directory, f))
    if dirs != []:
        for d in dirs:
            getConfigFilesPaths(os.path.join(directory, d), confFiles)
    return confFiles
            
def findConfFilePath(confFiles, routerNumber):
    for f in confFiles:
        if f.endswith('i'+str(routerNumber)+'_startup-config.cfg'):
            return f


# main
if __name__ == "__main__":
    # ce qui est demandé : il faut ecrire un code utilisant les fonctions définies 
    # qui nous servira à configurer tous les routeurs deja en place

    tree, root = initXML() # crée la racine et la stocke dans la variable root

    confFiles = []
    confFiles = getConfigFilesPaths('C:\\Users\\lucas\\GNS3\\projects\\testP\\project-files\\dynamips', confFiles)

    for AS in root :
        setAddresses(root, AS)
        for router in AS :
            # on génere la config file et on la remplit d'abord avec ce qui ne dépend pas des interfaces
            
            '''try :
                f = open("./conf-files/" + getFileName(router), "w")

                defaultInfoHead(f, router)

                for interface in router :
                    writeAddresses(AS, router, interface,f, tree)

                deployProtocol(root, router)

                defaultInfoFoot(f, router)

                f.close()
            except :
                print("Error while writing the file")'''

            try :
                f = open(findConfFilePath(confFiles, getRouterNumber(router)), "w")
            except :
                print("File not found")

            try :
                defaultInfoHead(f, router)

                for interface in router :
                    writeAddresses(AS, router, interface,f,tree)

                deployProtocol(root, router)

                defaultInfoFoot(f, router)

                f.close()
                print("File written successfully")
            except :
                print("Error while writing the file")
                

    # il reste à faire :

    # " ipv6 rip ripng enable" sur chaque interface
    # "ipv6 router rip ripng
    #   redistribute connected"

    # eBGP (remote-as)
    # faire des tests sur GNS3 et comparer les config files, encore aucun test fait à part génerer les files
    # GNS3 fy




    
    '''
    Nouveaux changements :
        ajout de la fonction enableProtocolInterface
        

    '''


