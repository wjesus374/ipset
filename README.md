# Search ipset

Documentação básica

Pré requisitos:
* Todos os scripts em Python no mesmo diretório

Contribuição:
* https://doughellmann.com/blog/2008/11/30/pymotw-readline/
* https://pypi.org/project/ipcalc/

Gerar um ipset list:
* sudo ipset list -output plain -file ipset.plain

Ou

* sudo ipset list -output plain > ipset.plain

Configurar no script *parser.py* o nome dos input e output:

<pre>
    readfile('ipset.plain')
    writestatistic('ipsetip.json',ipsetipinfo)
    writestatistic('ipsetnet.json',ipsetnetinfo)
</pre>

Se mudar o path padrão, definir um path absoluto em ambos scripts

# Exemplo:

De:

<pre>
    result = getconfig('ipsetip.json')
    searchnet = getconfig('ipsetnet.json')
</pre>

Para:

<pre>
    result = getconfig('/tmp/ipsetip.json')
    searchnet = getconfig('/tmp/ipsetnet.json')
</pre>


# Para o iptables

iptables-save > iptables.save
