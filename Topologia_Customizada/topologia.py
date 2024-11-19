from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

class MyTopo(Topo):
    """
    Topologia personalizada com 7 hosts e 7 switches
    """

    def __init__(self):
        Topo.__init__(self)

        # Adicionar hosts com MAC e IP configurados
        h1 = self.addHost('h1', mac="00:00:00:00:00:01", ip="10.0.0.1/24")
        h2 = self.addHost('h2', mac="00:00:00:00:00:02", ip="10.0.0.2/24")
        h3 = self.addHost('h3', mac="00:00:00:00:00:03", ip="10.0.0.3/24")
        h4 = self.addHost('h4', mac="00:00:00:00:00:04", ip="10.0.0.4/24")
        h5 = self.addHost('h5', mac="00:00:00:00:00:05", ip="10.0.0.5/24")
        h6 = self.addHost('h6', mac="00:00:00:00:00:06", ip="10.0.0.6/24")
        h7 = self.addHost('h7', mac="00:00:00:00:00:07", ip="10.0.0.7/24")

        # Adicionar switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')

        # Adicionar links entre switches e hosts
        self.addLink(s3, h6)
        self.addLink(s3, s7)
        self.addLink(s7, h7)
        self.addLink(s3, s4)
        self.addLink(s4, h5)
        self.addLink(s4, s2)
        self.addLink(s2, h1)
        self.addLink(s2, s1)
        self.addLink(s4, s5)
        self.addLink(s5, h4)
        self.addLink(s5, s6)
        self.addLink(s6, h2)
        self.addLink(s6, h3)

def test_topology():
    """
    Configura a topologia, realiza testes de conectividade e aplicar regras para endereços mac e apagar as regras anteriores.
    """
    net = Mininet(topo=MyTopo(), controller=RemoteController, switch=OVSSwitch)
    

    print("\n*** Iniciando a rede")
    net.start()

    print("\n*** Testando conectividade entre os hosts")
    net.pingAll()  # Teste de conectividade inicial

    print("\n*** Inspecionando interfaces de h1")
    h1 = net.get('h1')
    print(h1.cmd('ifconfig'))

    print("\n*** Inspecionando tabela de portas do s1")
    s1 = net.get('s1')
    print(s1.cmd('ovs-vsctl show'))

    print("\n*** Configurando regras de fluxo baseadas em MAC")
    # Limpar regras existentes
    for switch in ['s1', 's2', 's3', 's4', 's5', 's6', 's7']:
        sw = net.get(switch)
        print(f"Limpando regras de {switch}")
        sw.cmd('ovs-ofctl del-flows ' + switch)

    # Regras para permitir comunicação entre h1 e h2
    s2 = net.get('s2')
    s2.cmd('ovs-ofctl add-flow s2 priority=1,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:02,actions=output:2')
    s2.cmd('ovs-ofctl add-flow s2 priority=1,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:01,actions=output:1')

    print("\n*** Testando conectividade após aplicar regras de fluxo")
    # Teste positivo
    print("Testando h1 -> h2 (permitido):")
    print(h1.cmd('ping -c 3 10.0.0.2'))

    # Teste negativo
    print("Testando h1 -> h3 (bloqueado):")
    print(h1.cmd('ping -c 3 10.0.0.3'))

    print("\n*** Rede configurada. CLI disponível para mais testes.")
    CLI(net)  # Permite interação manual para inspecionar mais detalhes

    print("\n*** Parando a rede")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    test_topology()


'''
Descrição do Código

Item a: A topologia personalizada é criada com 7 hosts e 7 switches, com endereços MAC e IP definidos.
Item b: Inspeciona informações das interfaces e portas dos switches, exibindo os detalhes no terminal.

Item d: Realiza testes de ping entre hosts.
Item e: Remove regras existentes e aplica novas regras de fluxo baseadas em endereços MAC.
Item f: Testa conectividade após as regras, garantindo que apenas os hosts permitidos podem se comunicar.

'''