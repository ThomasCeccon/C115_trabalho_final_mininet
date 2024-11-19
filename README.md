# Projeto Mininet final

- Este projeto utiliza o Mininet para criar uma topologia linear com oito hosts

## 1. A) Criando Topologia linaer com 8 hosts
```sh
  sudo mn --topo linear,8 --mac --link tc,bw=30
```

## B) Inspecione informações das interfaces, endereços MAC, IP

- Listar todos os nós (hosts e switches):
```sh
    nodes
```

- Verficar os enlaces
```sh
    net
```

- Verificar endereços lógicos
```sh
    dump
```

- Mostrar dados dos dispositivos h1 a h8
```sh
    h1 ifconfig
    h2 ifconfig
    ...
    h8 ifconfig
```

## C) Desenho ilustrativo da topologia

- Ping entre todos os hosts
```sh
    pingall
```

## D) Executar testes de ping e tcpdump entre os diferentes nós

- Ping específico entre os hosts h1 e h8
```sh
    h1 ping -c 6 h8
```

- Comando iperf
```sh
      xterm h1 h8
```

- Capturar pacotes com o tcpdump
```sh
      h1 tcpdump -n -i h1-eth0
```

- Node h8
```sh
      ping 10.0.0.1
```

- Node h1
```sh
     tcpdump -n -i h1-eth0
```

## E) Testes com iperf entre servidor e cliente (h1 servidor e h2 cliente)

- Definir o servidor TCP:
```sh
      h1 iperf -s -p 5555 -i 1
```
- Definir o cliente:
```sh
     h2 iperf -c 10.0.0.1 -p 5555 -i 1 -t 15
```
- Isso executa um teste de 15 segundos com relatórios por segundo.

- Variando a largura de banda para cada largura de banda solicitada (1, 5, 10, 15, 20, 25 Mbps)
  
  -Ajuste para a largura de banda desejada
  ```sh
    sudo mn --topo linear,8 --mac --link tc,bw=1,10,15,20,25
    h1 iperf -s -p 5555 -i 1
    h2 iperf -c 10.0.0.1 -p 5555 -i 1 -t 15
  ```

## 2. A) Topologia Personalizada (Código Python)
- `topologia.py`
- Desenho topologia customizada


