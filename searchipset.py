#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import readline
import re
import json
import ipcalc

class MyCompleter(object):  # Custom completer

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options
                                    if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try:
            return self.matches[state]
        except IndexError:
            return None


def getconfig(configfile):

    with open(configfile, "r") as jsonfile:
        data = json.load(jsonfile)

    return data


def showrules(iptables,ipsetname):

    rules = []
    resp = ['S','s','Sim','SIM','y','Y','YES']

    for rule in iptables:
        if re.search(ipsetname,rule):
            rules.append(rule)

    if len(rules) > 1:
        result = input("IPSET encontrado no 'iptables-save' deseja mostrar todos? [S/n] ")

        if result in resp:
            for rule in rules:
                print(rule)


def main():
    #Coletar dados JSON
    result = getconfig('ipsetip.json')
    searchnet = getconfig('ipsetnet.json')
    iptables = getconfig('iptables.save.json')

    keywords = []
    for key in result:
        keywords.append(key)

    #keywords = ["hello", "hi", "how are you", "goodbye", "great"]
    while True:
        try:
            completer = MyCompleter(keywords)
            readline.set_completer(completer.complete)
            readline.parse_and_bind('tab: complete')
            for kw in keywords:
                readline.add_history(kw)

            #Python2
            #input = raw_input("Search: ")
            #Python3
            #search = input("Search: ")
            search = input("===== Busca: ")

            #print("You entered %s" %search)
            #print("Result: [%s]" %result[search])
            try: 
                #print("==== Resultado: [%s]" %result[search])
                print("==== IPSET:")
                for info in result[search]:
                    for i in result[search][info]:
                        #Printar o nome da chave e o nome do ipset
                        print("\t %s : %s" %(info.upper(),i))
                        showrules(iptables,i)
            except Exception as e: 
                print("Informação não encontrada no 'ipset list' - [%s]" %e)
            
            try:
                if re.search('[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}',search):
                    for netip in searchnet:
                        if search in ipcalc.Network(netip):
                            print("==== Rede encontrada: [%s]" %netip)
                            #print("==== Resultado [network]: [%s]" %result[netip])
                            print("==== IPSET:")
                            for info in result[netip]:
                                for i in result[netip][info]:
                                    print("\t %s : %s" %(info.upper(),i))
            except Exception as e:
                print("Erro: [%s]" %e)
        except Exception as e:
            #print("Error fetching data")
            print("Erro ao coletar dados: [%s]" %e)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt):
        print('')
