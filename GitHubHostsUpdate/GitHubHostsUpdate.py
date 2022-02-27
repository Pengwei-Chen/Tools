import os
import re
from urllib.request import urlopen

def get_IP_Address(url):
    html = urlopen(url).read().decode('utf-8')
    pattern = r'<tr><th>IP Address</th><td><ul class="comma-separated"><li>(\d+\.\d+\.\d+\.\d+)</li></ul></td></tr>'
    return(re.findall(pattern, html)[0])

def generate_text():
    path = "C:/Windows/System32/drivers/etc/hosts"
    hosts = open(path, 'r')
    text = hosts.read()
    hosts.close()
    pattern = r'#github\n\d+\.\d+\.\d+\.\d+ github.com\n\d+\.\d+\.\d+\.\d+ github.global.ssl.fastly.net'
    updated_pattern = '#github\n' + get_IP_Address("http://github.com.ipaddress.com/") + " github.com\n" + get_IP_Address("http://github.global.ssl.fastly.net.ipaddress.com/") + " github.global.ssl.fastly.net"
    if(re.findall(pattern, text) != []):
        text = re.sub(pattern, updated_pattern, text)
    else:
        text = text + "\n" + updated_pattern;
    return(text)

def update_Hosts(name, text):
    path = "C:/Windows/System32/drivers/etc/" + name
    hosts = open(path, 'w')
    hosts.write(text)
    hosts.close()

text = generate_text()
update_Hosts("hosts", text)


