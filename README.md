# CIULS

O CIULS é um script que acessa via SSH com chave compartilhada um servidor SAMBA e consulta, com o comando `smbstatus`, o IP de um determinado usuário passado como parâmetro. Com ele é possível consultar o usuário pelo nome, consultar o IP, fazer acesso ssh ou gráfico (VNC/Vinagre) na máquina que o usuário está logado e visualizar permissões de usuário no compartilhamento de arquivos.

## Observação
Para o CIULS funcionar deve-se ter a sua chave pública no usuário root do servidor SAMBA em `/root/.ssh/authorized_keys`.

## Programas necessários para a execução correta deste script

```bash
sudo apt-get install ssh vinagre python3 python3-pip python3-setuptools
pip3 install paramiko
```

Para resolver um problema da biblioteca crypto deve-se atualizar o cryptography, o problema é algo do tipo `CryptographyDeprecationWarning`:

```bash
pip3 install cryptography==2.4.2
```

## Instalação

```bash
wget https://raw.githubusercontent.com/ctic-sje-ifsc/CIULS/master/ciuls.py
chmod +x ./ciuls.py
sudo mv ./ciuls.py /usr/local/bin/ciuls
```

## Como usar

```bash
ciuls [opções] [usuário]

Opções
-g, --grafico     Abre o Vinagre para ter acesso remoto.
-G, --grupo   Lista todos os grupos que o usuário
                  especificado tem permissão de acesso. (em teste)
-h, --help        Exibe esta ajuda.
-i, --ip          Exibe apenas o ip do usuário. [Opção padrão
                  caso o usuário não digitar nada.]
-n, --nome        Pesquisa o UID de um usuário através
                  de seu nome.
-s, --ssh         Abre uma conexão remota via ssh entre
                  o usuário logado e o usuário remoto.
-v, --version     Exibe a versão do software."
```
