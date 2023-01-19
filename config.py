import xml.etree.ElementTree as ET

# fichier xml qui regroupe 
configfile = './routeurs.xml'

# definir les fonctions dont on aura besoin dans le main
def initXML():
    tree = ET.parse(configfile) # transforme le fichier en ElementTree
    return tree.getroot() # selectionne la racine de l'arbre à elements (l'ET)

def getRouterName(router): #A jour
    return router.get('hostname')

def getRouterNumber(router) : #A jour
    return router.get('Rnumber')

def getNeighbors(router) : #A jour
    lNeighbors = []
    for i in router :
        lNeighbors.append(i.find('neighbor').text)
    return lNeighbors

def getInterfaceAddress(interface):
    return interface.find('address')

def getInterfaceNei(interface):
    return interface.find('neighbor').text

def getInterfaceFromNei(router, nei):
    res,n = (0, 0)
    for i in router :
        voisin = getInterfaceNei(i)
        if voisin == nei :
            res = n
        n+=1
    print(res)
    return router[res]

def getASList(root):
    lAS = []
    for AS in root.iter('AS'):
        lAS.append(AS)
    return lAS

def getASPosition(root, ASnumber) : #A jour
    for i in range(len(root)) :
        name = root[i].get('name')
        if ASnumber == int(name) : return i  

def getRoutersInAS(root, ASnumber): # A jour
    lRouters = []
    n = getASPosition(root, ASnumber)
    for router in root[n].iter('router'):
        lRouters.append(str(router.get('hostname')))
    return lRouters

def getASLinksNum(root, ASnumber) : #A jour
    i = getASPosition(root, ASnumber)
    return int((root[i]).get('nblinks'))

def getASProtocol(root, ASnumber): #A jour
    i = getASPosition(root, ASnumber)
    return (root[i]).get('protocol')

def getASAddress(root, ASnumber): #Defectueux
    i = getASPosition(root, ASnumber)
    return (root[i]).get('addressing')

def getASName(root, AS) : #A jour
    return int(AS.get('name'))

def getFileName(router) : #A jour
    number = router.get('Rnumber')
    fileName = 'i'+number+'_startup-config.cfg'
    return fileName

def getFilePath(router) :
    pass

def openConfFile(router) : #A jour
    filePath = getFilePath(router)
    return open(filePath, "a")

def writeAddresses(router, interface, f):

    hostname = router.get('hostname')

    f.write("interface "+interface[0].text+interface.get('number')+"/0\n")
    f.write(" no ip address\n")
    if int(interface.get('number')) == 0 :
        f.write(" duplex full\n")
    else :
        f.write(" negotiation auto\n")
    f.write(" ipv6 address "+interface[1].text+"/64\n")
    f.write(" ipv6 enable\n")
    if hostname in root[1][0] :
        f.write(" ipv6 rip ripng enable\n")
    elif hostname in root[1][1] :
        f.write(" ipv6 ospf 7 area 0\n")
    f.write("!\n")

def defaultInfoHead(f, router):
    f.write("service timestamps debug datetime msec\n")
    f.write("service timestamps log datetime msec\n")
    f.write("hostname "+router.get('hostname')+"\n")
    f.write("boot-start-marker\n")
    f.write("boot-end-marker\n")
    f.write("no aaa new-model\n")
    f.write("no ip icmp rate-limit unreachable\n")
    f.write("ip cef\n")
    f.write("no ip domain lookup\n")
    f.write("ipv6 unicast-routing\n")
    f.write("ipv6 cef\n")
    f.write("multilink bundle-name authenticated\n")
    f.write("ip tcp synwait-time 5\n")
    f.write("!\n")

def defaultInfoFoot(f, router):
    hostname = router.get('hostname')
    f.write("ip forward-protocol nd\n")
    f.write("no ip http server\n")
    f.write("no ip http secure-server\n")
    if hostname in root[1][0] :
        f.write("ipv6 router rip ripng\n")
        f.write(" redistribute connected\n")
    elif hostname in root[1][1] :
        n = router.get('Rnumber')
        f.write("ipv6 router ospf 7\n")
        f.write(" router-id "+n+"."+n+"."+n+"."+n+"\n")
    f.write("\n")
    f.write("\n")
    f.write("control-plane\n")
    f.write("line con 0\n")
    f.write(" exec-timeout 0 0\n")
    f.write(" privilege level 15\n")
    f.write(" logging synchronous\n")
    f.write(" stopbits 1\n")
    f.write("line aux 0\n")
    f.write(" exec-timeout 0 0\n")
    f.write(" privilege level 15\n")
    f.write(" logging synchronous\n")
    f.write(" stopbits 1\n")
    f.write("line vty 0 4\n")
    f.write(" login\n")
    f.write("end\n")

def getRoutersArray(root):
    rows = int(root.get('qtty'))
    cols = 1
    for AS in root.iter('AS') :
        if int(AS.get('nbrouters')) > cols :
            cols = int(AS.get('nbrouters'))
        
    print(rows, cols)
    arr = [[0 for i in range(cols)] for j in range(rows)]
    print(arr[0] is arr[1])

    #for router in root.iter('router') :

    for i in range(len(root)) :
        for j in range(len(root[i])) :
            arr[i][j]=root[i][j].get('hostname')
            print(arr[i][j])

    return arr

def getASOfRouter(root, router): #A jour
    lAS = getASList(root)
    for AS in lAS :
        pass
    l1 = getRoutersInAS(root, 111)
    l2 = getRoutersInAS(root, 222)
    hostname = getRouterName(router)

    if hostname in l1 :
        return 111
    if hostname in l2 :
        return 222

def getOtherASes(router):
    pass

def isBorderRouter(root, router) : #A jour
    hostname = getRouterName(router)
    lNeighbors = getNeighbors(router)
    CurrentASRouters = getRoutersInAS(root, getASOfRouter(root, router))

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
    hostname = getRouterName(router)
    n = getRouterNumber(router)
    ASN = getASOfRouter(root, router)
    ASNs = str(ASN)
    border, borderNei, address_ebgp = isBorderRouter(root, router)

    OASN = "222"


    f.write("router bgp "+ ASNs+"\n")
    f.write(" bgp router-id "+n+"."+n+"."+n+"."+n+"\n")
    f.write(" bgp log-neighbor-changes\n")
    f.write(" no bgp default ipv4-unicast\n")

    if border : 
        for interface in router :
            if interface.find('neighbor').text != borderNei :
                f.write(" neighbor "+interface[1].text+" remote-as "+ASNs+"\n")
            else :
                f.write(" neighbor "+interface[1].text+" remote-as "+ OASN+"\n")

    else : 
        for interface in router :
            f.write(" neighbor "+interface[1].text+" remote-as "+ASNs+"\n")
        
    f.write(" !\n")
    f.write(" address-family ipv4\n")
    f.write(" exit-address-family\n")
    f.write(" !\n")
    f.write(" address-family ipv6\n")

    if border :
        address = getASAddress(root, ASN)
        address = address[0:11]
        print(address)

        nblinks = getASLinksNum(root, ASN)
        for i in range(1,nblinks+1) :
            f.write("  network "+address+str(i)+"::/64\n")

        # adresse de la liaison interAS :
        network_ebgp = address_ebgp[:-1]
        f.write("  network "+network_ebgp+"/64\n")


    for interface in router :
        f.write("  neighbor "+interface[1].text+" activate\n")
    f.write(" exit-address-family\n")
    f.write("!\n")


# main
if __name__ == "__main__":
    # ce qui est demandé : il faut ecrire un code utilisant les fonctions définies 
    # qui nous servira à configurer tous les routeurs deja en place

    root = initXML() # crée la racine et la stocke dans la variable root


    for AS in root :
        for router in AS :
            # on génere la config file et on la remplit d'abord avec ce qui ne dépend pas des interfaces
            f = open(getFileName(router), "w")

            defaultInfoHead(f, router)

            for interface in router :
                writeAddresses(router, interface,f)

            deployProtocol(root, router)

            defaultInfoFoot(f, router)

            f.close()

    

    # il reste les cas suivants :
    # eBGP (remote-as)
    # faire des tests sur GNS3 et comparer les config files, encore aucun test fait à part génerer les files
    # GNS3 fy
    # spécifier le nombre d'AS au début




    



