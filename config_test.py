import unittest
import config

class TestConfig(unittest.TestCase):

    def test_initXML(self):
        self.assertEqual(config.initXML().tag, 'data')
        
    def test_getRouterName(self):
        self.assertEqual(config.getRouterName(config.initXML(), 1), 'R2')
        
    def test_getInterfaceAddress(self):
        self.assertEqual(config.getInterfaceAddress(config.initXML(), 1, 0), '2001:100:1:7::1')
        
    def test_getRoutersInAS(self):
        self.assertListEqual(config.getRoutersInAS(config.initXML(), 0), ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7'])
    
    def test_getASProtocol(self):
        self.assertEqual(config.getASProtocol(config.initXML(), "222"), 'OSPFv3')
        
    def test_getFileName(self):
        self.assertEqual(config.getFileName(config.initXML()[0][0]), 'i1_startup-config.cfg')
    
if __name__ == '__main__':
    unittest.main()