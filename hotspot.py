import subprocess
import uuid

ssid = input("Enter the name of the hotspot: ")
while True:
    password = input("Enter the password for the hotspot: ")
    if len(password) > 7:
        break
    print("The password is less than 8 characters!!")


auth = input("Select the authentication method (WEP, WPA1, WPA2): ").upper()
if auth == "WEP":
    auth_type = "open"
    enc_type = "WEP"
elif auth == "WPA1":
    auth_type = "WPA"
    enc_type = "TKIP"
elif auth == "WPA2":
    auth_type = "WPA2PSK"
    enc_type = "AES"
else:
    print("Invalid authentication method!")
    exit()

use_mac_address = input("Use MAC address? (y/n): ").lower() == "y"
if use_mac_address is True:
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 48, 8)][::-1])
    subprocess.run('netsh wlan set hostednetwork mode=allow ssid={} key={}'.format(ssid, password), shell=True, check=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="runas")
    subprocess.call("netsh wlan set hostednetwork authentication={} encryption={}".format(auth_type, enc_type), shell=True, check=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="runas")
    subprocess.run('netsh wlan set hostednetwork filterlist="{}"'.format(mac_address), shell=True, check=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="runas")
else:
    subprocess.run('netsh wlan set hostednetwork mode=allow ssid={} key={}'.format(ssid, password), shell=True, check=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="runas")
    subprocess.call("netsh wlan set hostednetwork authentication={} encryption={}".format(auth_type, enc_type), shell=True, check=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="runas")

hidden = input("Make the access point hidden? (y/n): ").lower() == "y"
if hidden:
    subprocess.run('netsh wlan set hostednetwork mode=disallow', shell=True, check=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="runas")
    subprocess.run('netsh wlan set hostednetwork mode=allow mode=hidden ssid={} key={}'.format(ssid, password), shell=True, check=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="runas")

subprocess.run('netsh wlan start hostednetwork', shell=True, check=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="runas")
