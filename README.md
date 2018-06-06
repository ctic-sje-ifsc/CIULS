# CIULS

O CIULS é um script que acessa via SSH com chave compartilhada um servidor SAMBA e consulta, com o comando smbstatus, o IP de um determinado usuário passado como parâmetro. Com ele é possível consultar o IP, fazer acesso ssh ou gráfico(VNC/Vinagre) na máquina que o usuário está logado.

## Observação:
Para o CIULS funcionar deve-se ter a sua chave pública no usuário root do servidor SAMBA em /root/.ssh/authorized_keys.

## Instalação:

```bash 
$ wget https://raw.githubusercontent.com/ctic-sje-ifsc/CIULS/master/ciuls
```

```bash 
$ chmod +x ./ciuls
```

```bash
$ sudo mv ./ciuls /usr/local/bin/ciuls
```

## Como usar:

```bash
ciuls [opções] [usuário]

Opções
-g, --grafico     Abre o Vinagre para ter acesso remoto.
-h, --help        Exibe esta ajuda.
-i, --ip          Exibe apenas o ip do usuário. [Opção padrão caso o usuário
                  não digitar nada.
-s, --ssh         Abre uma conexão remota via ssh entre
                  o usuário logado e o usuário remoto.
-v, --version     Exibe a versão do software.
```
