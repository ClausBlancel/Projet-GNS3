import xml.etree.ElementTree as ET

# fichier xml qui regroupe 
configfile = './routeurs.xml'

# definir les fonctions dont on aura besoin dans le main
def initXML():
    tree = ET.parse(configfile) # transforme le fichier en ElementTree
    return tree.getroot() # selectionne la racine de l'arbre à elements (l'ET)

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

def getFileName(router) :
    number = router.get('Rnumber')
    fileName = 'i'+number+'_startup-config.cfg'
    return fileName

def getFilePath(router) :
    pass

def openConfFile(router) :
    filePath = getFilePath(router)
    return open(filePath, "a")

def writeAddresses(router, interface, f):

    hostname = router.get('hostname')

    f.write("interface "+interface[0].text+interface[1].text+"/0\n")
    f.write(" no ip address\n")
    if interface[1] == 0 :
        f.write(" duplex full\n")
    else :
        f.write(" negotiation auto\n")
    f.write(" ipv6 address "+interface[2].text+"/64\n")
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

def deployProtocol(router):
    hostname = router.get('hostname')
    n = router.get('Rnumber')

    ASN = 111

    if hostname in root[1][0] :
        ASN = 111
    elif hostname in root[1][1] :
        ASN = 222

    ASN = str(ASN)
    
    f.write("router bgp "+ ASN+"\n")
    f.write(" bgp router-id "+n+"."+n+"."+n+"."+n+"\n")
    f.write(" bgp log-neighbor-changes\n")
    f.write(" no bgp default ipv4-unicast\n")
    for interface in router :
        f.write(" neighbor "+interface[2].text+" remote-as "+ASN+"\n")
    f.write(" !\n")
    f.write(" address-family ipv4\n")
    f.write(" exit-address-family\n")
    f.write(" !\n")
    f.write(" address-family ipv6\n")
    for interface in router :
        f.write(" neighbor "+interface[2].text+" activate\n")
    f.write(" exit-address-family\n")
    f.write("!\n")


# main
if __name__ == "__main__":
    # ce qui est demandé : il faut ecrire un code utilisant les fonctions définies 
    # qui nous servira à configurer tous les routeurs deja en place

    root = initXML() # crée la racine et la stocke dans la variable root

    for data in root :
        if data.tag == 'routers' : 
            for router in data :
                # on génere la config file et on la remplit d'abord avec ce qui ne dépend pas des interfaces
                f = open(getFileName(router), "a")

                defaultInfoHead(f, router)

                for interface in router :
                    writeAddresses(router, interface,f)

                deployProtocol(router)

                defaultInfoFoot(f, router)

                f.close()

    

    # il reste les cas suivants :
    # eBGP (remote-as)
    # corriger l'emplacer de création des fichiers
    # faire des tests sur GNS3 et comparer les config files, encore aucun test fait à part génerer les files





    



