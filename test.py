import xml.etree.ElementTree as ET

tree = ET.parse('routeurs.xml')

root = tree.getroot()

# Get all routers names
for router in root[0].findall('router'):

    name = router.get('name')

    print(name)