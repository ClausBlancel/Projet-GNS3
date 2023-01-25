import gns3fy

# Connect to the GNS3 server
gns3_api = gns3fy.GNS3()

# Get the list of devices in the topology
devices = gns3_api.get_devices()

# Iterate through the devices
for device in devices:
    # Get the device's name
    device_name = device["name"]
    
    # Get the device's config files path
    config_path = device["properties"]["configs_path"]
    
    number = device#........
    fileName = 'i'+number+'_startup-config.cfg'

    # Drag and drop config file to the device folder
    gns3_api.add_file(device_name, config_path, "config.cfg")

