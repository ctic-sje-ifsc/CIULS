#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import argparse
import subprocess
import paramiko


class ciuls(object):

    def __init__(self):
        self.login = {"username": "root", "hostname": "dk"}
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(**self.login, disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']})

# Função para pesquisar no DK o argumento passado
# retorna uma lista de usuários e a quantidade
    def consulta(self, args):
        listaUsers = []
        user = []
        stdin, stdout, stderr = self.ssh.exec_command(
            "/usr/bin/smbstatus -b |grep %s" % args)
        saida = stdout.read().decode('UTF-8')
        rep = len(saida.split('\n')) - 1
        if (rep == 1):  # caso encontre apenas um usuário
            num, user_table, ips = programa.organiza(saida)
            choice = int(num[0]) - 1
            user = user_table[choice]
            ips = ips[choice]
        elif (rep >= 2):  # caso encontre vários usuários
            num, user_table, ips = programa.organiza(saida)
            y = 0
            for i in user_table:
                print(num[y] + ")", i, '  \t-\t[' + ips[y] + ']')
                y += 1
            choice = int(input('Qual sua escolha: '))
            choice -= 1
            user = user_table[choice]
            ips = ips[choice]
        else:
            listaUsers = []
            choice = 0
            user = []
            ips = []
        return choice, user, ips

# Função que recebe os dados do comando smbstatus e retorna só usuário e ip
    def organiza(self, tabela):
        tabelaNum = []
        tabelaUser = []
        tabelaIp = []
        y = 1
        for i in tabela.split("\n"):
            if i:
                tabelaNum.append(str(y))
                y += 1
                tabelaUser.append(i.split()[1])
                enumerate(tabelaUser, 1)
                tabelaIp.append(i.split().pop().strip("()"))
        return tabelaNum, tabelaUser, tabelaIp

# Função para organizar o endeço ipv4 e ipv6
    def trataIP(self, ip):
        if (ip[:4] != str(2804)):  # tratando ipv4 ou ipv6
            ip = ip
        return ip

# Função que procura o nome de uma pessoa e retorna seu usuário e o UID
    def nome(self, args):
        stdin, stdout, stderr = self.ssh.exec_command(
            "ldapsearch -x -h ldap.sj.ifsc.edu.br -b ou=SaoJose,ou=usuarios,dc=cefetsc,dc=edu,dc=br displayName=*%s* |grep uid: | wc -l" % (args))
        contNome = stdout.read().rstrip().decode('UTF-8')
        y = int(contNome) + 1
        stdin, stdout, stderr = self.ssh.exec_command(
            'ldapsearch -x -h ldap.sj.ifsc.edu.br -b ou=SaoJose,ou=usuarios,dc=cefetsc,dc=edu,dc=br displayName=*%s* |grep displayName | cut -d ":" -f2 | head -n %s | tail -n %s' % (args, str(y), contNome))
        nomes = []
        temp = stdout.read().splitlines()
        if len(temp):
            for i in temp:  # cria uma lista com todos os usuários encontrados
                nomes.append(i.decode('UTF-8'))
            stdin, stdout, stderr = self.ssh.exec_command(
                'ldapsearch -x -h ldap.sj.ifsc.edu.br -b ou=SaoJose,ou=usuarios,dc=cefetsc,dc=edu,dc=br displayName=*%s* |grep uid: | cut -d ":" -f2 | head -n %s | tail -n %s' % (args, str(y), contNome))
            temp = stdout.read().splitlines()
            usuario = []
            for i in temp:
                usuario.append(i.decode('UTF-8'))
            for i, x in zip(nomes, usuario):  # Mescla o nome do usuário com o uid do usuário.
                print('O usuário' + BRED + i + NC,
                      'tem o UID' + BRED + x + NC + '.')
        else:
            print(
                'Não foi possível encontrar o usuário ' + BRED + args + NC + '.')
        return

# Função que pesquisa os grupos de um usuário específico
    def grupo(self, args):
        stdin, stdout, stderr = self.ssh.exec_command(
            "/usr/bin/smbstatus -b |grep %s |head -n 1 |tail -n 1 |awk '{print $2}'" % (args))
        user = stdout.read().rstrip().decode('UTF-8')
        if len(user):
            stdin, stdout, stderr = self.ssh.exec_command("id %s" % (user))
            grupo = stdout.read().rstrip().decode('UTF-8')
            print("Grupos ao qual o usuário", BRED +
                  str(user) + NC, "pertence:\n", grupo)
        else:
                print(
                    'Não foi possível encontrar o usuário ' + BRED + args + NC + '.')

if __name__ == "__main__":
    try:
        # if sys.argv[1] == '-v' or sys.argv[1] == '-h':
        #     pass
        if len(sys.argv) == 2 and str(sys.argv[1])[0] != '-':  # define opção padrão -i caso o usuário não informe
            sys.argv = ['./ciuls.py', '-i', sys.argv[1]]
        parser = argparse.ArgumentParser(prog='ciuls')
        parser.add_argument(
            '-g', '--grafico', metavar='NOME/USUÁRIO', help='Acesso remoto na máquina em que o usuário está conectado.')
        parser.add_argument(
            '-G', '--grupo', metavar='USUÁRIO', help='Lista os grupos que o usuário tem permissão.')
        parser.add_argument(
            '-i', '--ip', metavar='NOME/USUÁRIO', help='Mostra o ip do usuário especificado.')
        parser.add_argument(
            '-n', '--nome', metavar='NOME', help='Pesquisa o nome da pessoa e retorna o usuário.')
        parser.add_argument(
            '-s', '--ssh', metavar='NOME/USUÁRIO', help='Conecta, através de ssh no computador em que o usuário está conectado.')
        parser.add_argument(
            '-v', '--version', action='version', version='%(prog)s - Versão 3.5')
        argumento = parser.parse_args()
    except:
        # print('Final inesperado do programa.')
        sys.exit(1)
    else:
        BRED = "\033[1;31m"  # Texto Vermelho e Negrito
        NC = "\033[0;0m"  # Texto sem formatação
        programa = ciuls()
        if argumento.grafico:  # Se tiver o argumento -g ou --grafico
            choice, user, ips = programa.consulta(argumento.grafico)
            if len(user):  # caso variavel user não seja nula
                ip = programa.trataIP(ips)
                ip = "[" + ip + \
                    "]::5900"  # preparando o ip para ser passado como parametro para o vinagre
                erros = open(os.devnull, 'w')
                subprocess.Popen(
                    ["vinagre", ip], stderr=erros, stdout=subprocess.PIPE).communicate()[0]
            else:
                print("O usuário", BRED +
                      argumento.grafico + NC, "não possui nenhum endereço IP associado.")
        if argumento.ip:  # Se tiver o argumento -i ou --ip
            choice, user, ips = programa.consulta(argumento.ip)
            if len(user):  # caso variavel user não seja nula
                ip = programa.trataIP(ips)
                print("O IP do usuário", BRED + user + NC, "é", ip)
            else:
                print("O usuário", BRED +
                      argumento.ip + NC, "não possui nenhum endereço IP associado.")
        if argumento.nome:  # Se tiver o argumento -n ou --nome
            programa.nome(argumento.nome)
        if argumento.grupo:  # Se tiver o argumento -G ou --grupo
            programa.grupo(argumento.grupo)
        if argumento.ssh:  # Se tiver o argumento -s ou --ssh
            choice, user, ips = programa.consulta(argumento.ssh)
            if len(user):  # caso variavel user não seja nula
                ip = programa.trataIP(ips)
                subprocess.call("ssh -XC root@" + ip, shell=True)
                sys.exit(0)
            else:
                print("O usuário", BRED +
                      argumento.ssh + NC, "não possui nenhum endereço IP associado.")
