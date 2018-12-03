#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import getopt
import subprocess
import paramiko


class ciuls(object):

    def __init__(self, comando, args):
        self.comando = comando
        if len(args) > 0:
            self.args = args[0]
        else:
            self.args = ''
        self.login = {"username": "root", "hostname": "dk"}
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(**self.login)

    def main(self, options):
        pass

    def version(self):
        return self.comando + ' - Versão 3.0 Alpha'

    def erroMSG(self):
        return 'Sintaxe errada. Exemplo:\nUso: ' + self.comando + ' ( [OPÇÂO...] [USUÁRIO] )'

    def helpMSG(self):
        return '''
Nome
CIULS - (C)onsulta (I)P (U)suário (L)ogado (S)amba

Synopse
python3 ''' + self.comando + ''' [opção] [usuário]

Programas
Programas necessários para a execução correta deste script:
As root: apt-get install ssh, vinagre, python3, pip3
As user: pip install paramiko

Descrição
Este manual foi desenvolvido para facilitar o acesso remoto aos servidores do IFSC,
para funcionar corretamente é necessário que seu usuário esteja no LDAP do ifsc, no
caso de acesso SSH, e é fundamental que a chave pública do SSH do seu usuário esteja
no servidor de arquivos. Para abrir o modo gráfico do acesso remoto é necessário ter
instalado no computador o visualizador de área remota chamado vinagre.

Opções
-g, --grafico     Abre o Vinagre para ter acesso remoto.
-h, --help        Exibe esta ajuda.
-i, --ip          Exibe apenas o ip do usuario. [Opcao padrao
                  caso o usuario nao digitar nada.]
-n, --nome        Pesquisa o UID de um usuario atraves
                  de seu nome.
-p, --permissao   Lista todos os grupos que o usuario
                  especificado tem permissao de acesso.
-s, --ssh         Abre uma conexao remota via ssh entre
                  o usuario logado e o usuario remoto.
-v, --version     Exibe a versao do software.
'''

# Função para pesquisar no DK o argumento passado
# retorna uma lista de usuários e a quantidade
    def consulta(self):
        listaUsers = []
        stdin, stdout, stderr = self.ssh.exec_command(
            "/usr/bin/smbstatus -b |grep %s |wc -l" % self.args)
        rep = int(stdout.read().decode('UTF-8'))
        if (rep == 1):
            stdin, stdout, stderr = self.ssh.exec_command(
                "/usr/bin/smbstatus -b |grep %s |awk '{print $2}'" % self.args)
            user = stdout.read().splitlines()[0].decode('UTF-8')
            choice = 0
        elif (rep >= 2):
            user = []
            stdin, stdout, stderr = self.ssh.exec_command(
                "/usr/bin/smbstatus -b |grep %s |awk '{print $2}'" % self.args)
            listaUsers = stdout.read().splitlines()
            for i, line in enumerate(listaUsers, 1):
                print(str(i) + ')', line.decode('UTF-8'))
            choice = int(input('Qual sua escolha: '))
            choice -= 1
            user = listaUsers[choice].decode('UTF-8')
        else:
            listaUsers = []
            choice = 0
        return choice, user

# Função para mostrar e tratar o ip do usuário
# retorna o ipv4 ou ipv6 do usuário
    def pesquisa(self, choice):
        choice = choice + 1
        stdin, stdout, stderr = self.ssh.exec_command(
            "/usr/bin/smbstatus -b |grep %s |head -n %s |tail -n 1 |cut -d '(' -f2 | cut -d ')' -f1" % (self.args, str(choice)))
        ip = stdout.read().rstrip().decode('UTF-8')
        if (ip[:4] != str(2804)):
            ip = ip[7:]
        return ip

# Função que procura o nome de uma pessoa e retorna seu usuário e o UID
    def nome(self):
        stdin, stdout, stderr = self.ssh.exec_command(
            "ldapsearch -x -h vm-bd1 -b ou=SaoJose,ou=usuarios,dc=cefetsc,dc=edu,dc=br displayName=*%s* |grep uid: | wc -l" % (self.args))
        contNome = stdout.read().rstrip().decode('UTF-8')
        y = int(contNome) + 1
        stdin, stdout, stderr = self.ssh.exec_command(
            'ldapsearch -x -h vm-bd1 -b ou=SaoJose,ou=usuarios,dc=cefetsc,dc=edu,dc=br displayName=*%s* |grep displayName | cut -d ":" -f2 | head -n %s | tail -n %s' % (self.args, str(y), contNome))
        nomes = []
        temp = stdout.read().splitlines()
        for i in temp:
            nomes.append(i.decode('UTF-8'))
        stdin, stdout, stderr = self.ssh.exec_command(
            'ldapsearch -x -h vm-bd1 -b ou=SaoJose,ou=usuarios,dc=cefetsc,dc=edu,dc=br displayName=*%s* |grep uid: | cut -d ":" -f2 | head -n %s | tail -n %s' % (self.args, str(y), contNome))
        temp = stdout.read().splitlines()
        usuario = []
        for i in temp:
            usuario.append(i.decode('UTF-8'))
        for i, x in zip(nomes, usuario):
            print('O usuário' + BRED + i + NC,
                  'tem o UID' + BRED + x + NC + '.')
        return

# Função que pesquisa a permissão de um usuário específico
    def permissao(self):
        stdin, stdout, stderr = self.ssh.exec_command(
            "/usr/bin/smbstatus -b |grep %s |head -n 1 |tail -n 1 |awk '{print $2}'" % (self.args))
        user = stdout.read().rstrip().decode('UTF-8')
        stdin, stdout, stderr = self.ssh.exec_command("id %s" % (self.args))
        grupo = stdout.read().rstrip().decode('UTF-8')
        print("Grupos ao qual o usuário", BRED +
              str(user) + NC, "pertence:\n", grupo)

if __name__ == "__main__":
    try:
        options, args = getopt.getopt(sys.argv[1:], 'ghinpsv', [
                                      'grafico', 'help', 'ip', 'nome', 'permissao', 'ssh', 'version'])
    except getopt.GetoptError as err:
        print('FATAL ERROR:', err)
        sys.exit(1)
    else:
        BRED = "\033[1;31m"
        NC = "\033[0;0m"
        comando = sys.argv[0]
        programa = ciuls(comando, args)
        # print('teste', args.pop(1)) ## tentativa de tratar mais de uma opção
        # ao mesmo tempo
        if len(args) == 1:
            for opt, arg in options:
                if opt in ('-h', '--help'):
                    print(programa.helpMSG())
                elif opt in ('-v', '--version'):
                    print(programa.version())
                elif opt in ('-g', '--grafico'):
                    choice, user = programa.consulta()
                    ip = programa.pesquisa(choice)
                    ip = "[" + ip + "]::5900"
                    erros = open(os.devnull, 'w')
                    subprocess.Popen(
                        ["vinagre", ip], stderr=erros, stdout=subprocess.PIPE).communicate()[0]
                elif opt in ('-i', '--ip'):
                    choice, user = programa.consulta()
                    ip = programa.pesquisa(choice)
                    print("O IP do usuário", BRED + user + NC, "é", ip)
                elif opt in ('-n', '--nome'):
                    programa.nome()
                elif opt in ('-p', '--permissao'):
                    programa.permissao()
                elif opt in ('-s', '--ssh'):
                    choice, user = programa.consulta()
                    ip = programa.pesquisa(choice)
                    print('ssh')
                    # subprocess.Popen(
                    #     ["konsole", "--hold", "-e", "ssh -XC", "ctic@" + ip], stdout=subprocess.PIPE).communicate()[0]
                    # subprocess.Popen(["konsole", "--hold", "-e", "ssh -XC", "ctic@" + ip],
                    # env=dict(os.environ, DISPLAY=":0.0",
                    # XAUTHORITY="/home/rmartins/.Xauthority",
                    # stdout=subprocess.PIPE).communicate()[0]
        else:
           print(programa.erroMSG())
           print(programa.helpMSG())
