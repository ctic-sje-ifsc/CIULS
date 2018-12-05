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
        self.ssh.connect(**self.login)

# Função para pesquisar no DK o argumento passado
# retorna uma lista de usuários e a quantidade
    def consulta(self, args):
        listaUsers = []
        user = []
        stdin, stdout, stderr = self.ssh.exec_command(
            "/usr/bin/smbstatus -b |grep %s |wc -l" % args)
        rep = int(stdout.read().decode('UTF-8'))
        if (rep == 1): #caso encontre apenas um usuário
            stdin, stdout, stderr = self.ssh.exec_command(
                "/usr/bin/smbstatus -b |grep %s |awk '{print $2}'" % args)
            user = stdout.read().splitlines()[0].decode('UTF-8')
            choice = 0
        elif (rep >= 2):  #caso encontre vários usuários
            stdin, stdout, stderr = self.ssh.exec_command(
                "/usr/bin/smbstatus -b |grep %s |awk '{print $2}'" % args)
            listaUsers = stdout.read().splitlines()
            for i, line in enumerate(listaUsers, 1): #Enumerando todos os usuário encontrados
                print(str(i) + ')', line.decode('UTF-8'))
            choice = int(input('Qual sua escolha: '))
            choice -= 1
            user = listaUsers[choice].decode('UTF-8')
        else:
            listaUsers = []
            choice = 0
            user = []
        return choice, user

# Função para mostrar e tratar o ip do usuário
# retorna o ipv4 ou ipv6 do usuário
    def pesquisa(self, choice, args):
        choice = choice + 1
        stdin, stdout, stderr = self.ssh.exec_command(
            "/usr/bin/smbstatus -b |grep %s |head -n %s |tail -n 1 |cut -d '(' -f2 | cut -d ')' -f1" % (args, str(choice)))
        ip = stdout.read().rstrip().decode('UTF-8')
        if (ip[:4] != str(2804)): #tratando ipv4 ou ipv6
            ip = ip[7:]
        return ip

# Função que procura o nome de uma pessoa e retorna seu usuário e o UID
    def nome(self, args):
        stdin, stdout, stderr = self.ssh.exec_command(
            "ldapsearch -x -h vm-bd1 -b ou=SaoJose,ou=usuarios,dc=cefetsc,dc=edu,dc=br displayName=*%s* |grep uid: | wc -l" % (args))
        contNome = stdout.read().rstrip().decode('UTF-8')
        y = int(contNome) + 1
        stdin, stdout, stderr = self.ssh.exec_command(
            'ldapsearch -x -h vm-bd1 -b ou=SaoJose,ou=usuarios,dc=cefetsc,dc=edu,dc=br displayName=*%s* |grep displayName | cut -d ":" -f2 | head -n %s | tail -n %s' % (args, str(y), contNome))
        nomes = []
        temp = stdout.read().splitlines()
        if len(temp):
            for i in temp: #cria uma lista com todos os usuários encontrados
                nomes.append(i.decode('UTF-8'))
            stdin, stdout, stderr = self.ssh.exec_command(
                'ldapsearch -x -h vm-bd1 -b ou=SaoJose,ou=usuarios,dc=cefetsc,dc=edu,dc=br displayName=*%s* |grep uid: | cut -d ":" -f2 | head -n %s | tail -n %s' % (args, str(y), contNome))
            temp = stdout.read().splitlines()
            usuario = []
            for i in temp:
                usuario.append(i.decode('UTF-8'))
            for i, x in zip(nomes, usuario): #Mescla o nome do usuário com o uid do usuário.
                print('O usuário' + BRED + i + NC,
                    'tem o UID' + BRED + x + NC + '.')
        else:
            print('Não foi possível encontrar o usuário ' + BRED + args + NC + '.')
        return

# Função que pesquisa a permissão de um usuário específico
    def permissao(self, args):
        stdin, stdout, stderr = self.ssh.exec_command(
            "/usr/bin/smbstatus -b |grep %s |head -n 1 |tail -n 1 |awk '{print $2}'" % (args))
        user = stdout.read().rstrip().decode('UTF-8')
        if len(user):
            stdin, stdout, stderr = self.ssh.exec_command("id %s" % (args))
            grupo = stdout.read().rstrip().decode('UTF-8')
            print("Grupos ao qual o usuário", BRED +
                str(user) + NC, "pertence:\n", grupo)
        else:
                print('Não foi possível encontrar o usuário ' + BRED + args + NC + '.')

if __name__ == "__main__":
    try:
        # if sys.argv[1] == '-v' or sys.argv[1] == '-h':
        #     pass
        if len(sys.argv) == 2 and str(sys.argv[1])[0] != '-': # define opção padrão -i caso o usuário não informe
            sys.argv = ['./ciuls.py', '-i', sys.argv[1]]
        parser = argparse.ArgumentParser(prog='ciuls')
        parser.add_argument(
            '-g', '--grafico', metavar='NOME/USUÁRIO', help='Acesso remoto na máquina em que o usuário está conectado.')
        parser.add_argument(
            '-i', '--ip', metavar='NOME/USUÁRIO', help='Mostra o ip do usuário especificado.')
        parser.add_argument(
            '-n', '--nome', metavar='NOME', help='Pesquisa o nome da pessoa e retorna o usuário.')
        parser.add_argument(
            '-p', '--permissao', metavar='USUÁRIO', help='Lista as permissões que o usuário tem.')
        parser.add_argument(
            '-s', '--ssh', metavar='NOME/USUÁRIO', help='Conecta, através de ssh no computador em que o usuário está conectado.')
        parser.add_argument(
            '-v', '--version', action='version', version='%(prog)s - Versão 3.0 Beta')
        argumento = parser.parse_args()
    except:
        print('Final inesperado do programa.')
        sys.exit(1)
    else:
        BRED = "\033[1;31m" #Texto Vermelho e Negrito
        NC = "\033[0;0m" #Texto sem formatação
        programa = ciuls()
        if argumento.grafico: #Se tiver o argumento -g ou --grafico
            choice, user = programa.consulta(argumento.grafico)
            if len(user): #caso variavel user não seja nula
                ip = programa.pesquisa(choice, argumento.grafico)
                ip = "[" + ip + "]::5900" #preparando o ip para ser passado como parametro para o vinagre
                erros = open(os.devnull, 'w')
                subprocess.Popen(
                    ["vinagre", ip], stderr=erros, stdout=subprocess.PIPE).communicate()[0]
            else:
                print("O usuário", BRED +
                    argumento.grafico + NC, "não possui nenhum endereço IP associado.")
        if argumento.ip: #Se tiver o argumento -i ou --ip
            choice, user = programa.consulta(argumento.ip)
            if len(user): #caso variavel user não seja nula
                ip = programa.pesquisa(choice, argumento.ip)
                print("O IP do usuário", BRED + user + NC, "é", ip)
            else:
                print("O usuário", BRED +
                    argumento.ip + NC, "não possui nenhum endereço IP associado.")
        if argumento.nome: #Se tiver o argumento -n ou --nome
            programa.nome(argumento.nome)
        if argumento.permissao: #Se tiver o argumento -p ou --permissao
            programa.permissao(argumento.permissao)
        if argumento.ssh: #Se tiver o argumento -s ou --ssh
            choice, user = programa.consulta(argumento.ssh)
            if len(user): #caso variavel user não seja nula
                ip = programa.pesquisa(choice, argumento.ssh)
                subprocess.call("ssh -XC ctic@" + ip, shell=True)
            else:
                print("O usuário", BRED +
                    argumento.ssh + NC, "não possui nenhum endereço IP associado.")
