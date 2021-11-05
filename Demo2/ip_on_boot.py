import comms
import netifaces as ni

system = comms.comm()
ni.ifaddresses('wlan0')

ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

system.update_lcd(str(ip))

exit(0)