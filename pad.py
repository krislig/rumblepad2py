import usb.core
import usb.util
from time import sleep

dev = usb.core.find(idVendor=0x046d, idProduct=0xc218)

if dev is None:
	raise ValueError('Device not found')

interface = 0

endpoint = dev[0][(0,0)][0]

if dev.is_kernel_driver_active(interface) is True:
	dev.detach_kernel_driver(interface)
	usb.util.claim_interface(dev, interface)
	print 'claimed'

collected = 0
attemps = 100

print endpoint.bEndpointAddress

try:
    # strong vibration - left side - vibration level from  0x00 to 0xff
	dev.write(1, [0x51, 0, 0, 0, 0xff, 0, 0, 0], interface)
	sleep(1)
    # stop vibration
	dev.write(1, [0xf3, 0, 0, 0, 0, 0, 0, 0], interface)
	sleep(1)
    # weak vibration - right side - vibration level from  0x00 to 0xff
	dev.write(1, [0x51, 0, 0xff, 0, 0, 0, 0, 0], interface)
	sleep(1)
	dev.write(1, [0xf3, 0, 0, 0, 0, 0, 0, 0], interface)
except:
	print 'exception occured'

while collected < attemps:
	try:
		data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
		collected += 1
		print data 
	except usb.core.USBError as e:
		data = None
		if e.args == ('Operation timed out',):
			print 'time out'

print 'releasing interface'
usb.util.release_interface(dev, interface)
dev.attach_kernel_driver(interface)
print 'done'
