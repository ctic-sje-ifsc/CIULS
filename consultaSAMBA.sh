#!/bin/bash
## Script para pegar do dk o ip que o usuario especificado esta conectado

arg1=${1}
arg2=${2}

### Funcao numero da versao ###
version() {
echo "${0} - Versão 2.5alpha"
}

### Funcao mensagem de erro ###
erroMSG() {
echo "Sintaxe errada, diferencie maiusculas das minusculas. Exemplo:"
echo "Uso: $0 [[OPÇÃO...] [USUARIO]])"
}

### Funcao retorna quantidade usuarios encontrados ###
lista() {
for opt in $(seq 1 ${rep})
  do
  user=$(ssh -q root@dk /usr/bin/smbstatus | grep ${arg2} |head -n ${opt} |tail -n 1 |awk '{print $2}' )
  echo "(${opt}) ${user}"
done
}

### Funcao ajuda ###
helpMSG() {

echo "Nome
usuario.sh - consulta um usuario no samba do DK

Synopse
bash /usr/bin/usuario.sh [opções] [usuário]

Descrição
Este manual foi desenvolvido para facilitar o acesso remoto aos servidores do IFSC,
para funcionar corretamente é necessário que seu usuário esteja no LDAP do ifsc, no 
caso de acesso SSH, e é fundamental que a chave publica do SSH do seu usuário esteja
no servidor de arquivos. Para abrir o modo gráfico do acesso remoto é necessário ter
instalado no computador o visualizador de área remota chamado vinagre.

Opções
-g, --grafico     Abre o Vinagre para ter acesso remoto.
-h, --help        Exibe esta ajuda.
-i, --ip          Exibe apenas o ip do usuário. [Opção padrão caso o usuário
                  não digitar nada.
-s, --ssh         Abre uma conexão remota via ssh entre
                  o usuário logado e o usuário remoto.
-v, --version     Exibe a versão do software.

Arquivos
/usr/bin/usuario.sh"
}

############## Inicio do programa #########################

if [ $# -gt 2 ] ;
    then
	erroMSG
        exit
elif [ ${arg1} = "-h" ] || [ ${arg1} = "--help" ] ;
    then
	helpMSG
	exit
elif [ ${arg1} = "-v" ] || [ ${arg1} = "--version" ] ;
    then
	version
	exit
elif [ -z ${arg2} ] ;
    then
	arg2=${arg1}
	arg1=$(echo "-i")
fi

rep=$(ssh -q root@dk /usr/bin/smbstatus | grep ${arg2} |wc -l)
rep=$(echo "${rep} / 2" |bc)

case ${rep} in
        1 )
                choice=1
        ;;
        2 )
                echo "Foi encontrado mais de um usuário!"
                lista
                echo -n "Qual sua escolha: "
                read choice
        ;;
        * )
                erroMSG
                helpMSG
        ;;
esac

ip=$(ssh -q root@dk /usr/bin/smbstatus | grep ${arg2} |head -n ${choice} |tail -n 1 | cut -d "(" -f2 | cut -d ")" -f1 )

test=$(echo "${ip}" |cut -d ":" -f1)
ipv6=$(echo "2804")
if [ -z ${test} ];
    then
        ip=$(echo "${ip}" |cut -d ":" -f4)
	if [ -z ${ip} ];
	    then
		echo "O usuário ${arg2} não possui nenhum IP relacionado."
		exit
	fi
fi

case ${arg1} in
	-g | --grafico )
		vinagre [${ip}]::5900
	;;
	-i | --ip )
		user=$(ssh -q root@dk /usr/bin/smbstatus | grep ${arg2} |head -n ${choice} |tail -n 1 |awk '{print $2}' )
		echo "O ip do usuario ${user} é --> ${ip} <--."
	;;
	-s | --ssh )
		ssh -XC ctic@${ip}
	;;
	-*)
		erroMSG
	;;
	*)
		erroMSG
		helpMSG
	;;
esac
