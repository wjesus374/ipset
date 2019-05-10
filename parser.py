#!/usr/bin/python
# -*- encoding: utf-8 -*-

import re
import json

import pprint
pp = pprint.PrettyPrinter(indent=2)

#pip install ipcalc
import ipcalc

#Variavel de membros
member = None
#Informações sobre o ipset
ipsetdata = {}
#Informações sobre os IP's do ipset
ipsetipinfo = {}
#Informações sobre as Redes do ipset
ipsetnetinfo = []

#Exclude da expansão de rede
#netexclude = ['192.168.209.0/24']
netexclude = []

#Permite da expansão de rede
#netpermit = ['10.12.222.56/29','192.168.240.0/24']
netpermit = []

def addname(data,name):
    try:
        if name not in ipsetipinfo[data]['name']:
            ipsetipinfo[data]['name'].append(name)
    except:
        ipsetipinfo[data] = {}
        ipsetipinfo[data]['name'] = [name]

def addproto(data,proto):
    try:
        if proto not in ipsetipinfo[data]['proto']:
            ipsetipinfo[data]['proto'].append(proto)
    except:
        ipsetipinfo[data]['proto'] = [proto]

def net2ip(data):
    result = []

    for ip in ipcalc.Network(data):
        result.append(str(ip))

    return result


#def addnet(data,name):
#    try:
#        if name not in ipsetnetinfo[data]['name']:
#            ipsetnetinfo[data]['name'].append(name)
#    except:
#        ipsetnetinfo[data] = {}
#        ipsetnetinfo[data]['name'] = [name]
#        if data in netpermit and data not in netexclude:
#            result = net2ip(data)
#            ipsetnetinfo[data]['iplist'] = result
#
#        #if data == '192.168.60.0/27':
#        #    result = net2ip(data)
#        #    ipsetnetinfo[data]['iplist'] = result

def addnet(data):

    if data not in ipsetnetinfo:
        ipsetnetinfo.append(data)


def readfile(ipsetfile):
    stat = {}
    with open(ipsetfile, 'r') as thefile:
        for line in thefile:
            #line = thefile.readline()
            line = re.sub('[\n]','', line)
        
            if re.search('^[A-Za-z]',line):
                if line == 'Members:':
                    member = True
                    ipsetdata[name].append(stat)
                    #Zerar o dict
                    stat = {}
                else:
                    member = False

                    #Quando não for um Member, dividir a linha em 2 partes
                    #Name: Teste
                    info = line.split(':',1)
                    key = info[0].strip()
                    value = info[1].strip()

                    #Gravar valor em um dict
                    stat[key] = value
                    if key == 'Name':
                        #Gravar o name em uma variável diferente para utilizar no append 'Members'
                        name = value
                        ipsetdata[value] = []

            if member is True and re.search('^[0-9]',line):
                #mem['name'] = name
                for value in line.split(','):
                    #Se encontrar algum texto, significa que é uma porta
                    #tcp:22
                    if re.search('^[a-z]',value):
                        proto,port = value.split(':')
                        addname(port,name)
                        addproto(port,proto)
                        #print("Proto: [%s]:[%s]" %(proto,port))

                    #Se encontrar a /, significa que é uma rede
                    if re.search('/',value):
                        print("Network: [%s]" %value)
                        addname(value,name)
                        addnet(value)

                    #Se encontrar um formato de IP (sem a barra)
                    if re.search('^[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}$',value):
                        #print("IP: [%s]" %value)
                        addname(value,name)


def writestatistic(configfile,data):
    with open(configfile,"w") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4, sort_keys=True)


if __name__ == "__main__":
    readfile('ipset.plain')
    writestatistic('ipsetip.json',ipsetipinfo)
    #print(ipsetdata)
    #print(ipsetipinfo)
    #pp.pprint(ipsetipinfo)
    #pp.pprint(ipsetnetinfo)
    writestatistic('ipsetnet.json',ipsetnetinfo)
    #for info in ipsetipinfo:
    #    print("=== IP/Port: [%s]" %info)
    #    for name in ipsetipinfo[info]['name']:
    #        print("Name: [%s]" %name)
    #        #print("ipset: [%s]" %ipsetdata[name])
    #        print("Type: [%s]" %ipsetdata[name][0]['Type'])
