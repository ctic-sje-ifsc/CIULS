#!/bin/bash
## Script para pegar do dk o ip que o usuario especificado esta conectado

erroMSG() {
echo "Sintaxe errada, diferencie maiusculas das minusculas. Exemplo:"
echo "Uso: $0 [[OPÇÃO...] [USUARIO]])"
}

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

arg1=${1}
arg2=${2}

if [ $# -gt 2 ] ;
    then
	erroMSG
        exit
elif [ ${arg1} = "-h" ] || [ ${arg1} = "--help" ] ;
    then
	helpMSG
	exit
elif [ -z ${arg2} ] ;
    then
	arg2=${arg1}
	arg1=$(echo "-i")
fi

ip=$(ssh -q root@dk /usr/bin/smbstatus | grep ${arg2} |head -n 1 |tail -n 1 | cut -d "(" -f2 | cut -d ")" -f1 2> /dev/null)

test=$(echo "${ip}" |cut -d ":" -f1)
ipv6=$(echo "2804")
if [ -z ${test} ];
    then
	echo "O usuário ${arg2} não possui nenhum IP relacionado."
	exit
elif [ "${test}" == "${ipv6}" ];
    then
        true
    else
        ip=$(echo "${ip}" |cut -d ":" -f4)
fi

case ${arg1} in
	-g | --grafico )
		vinagre [${ip}]::5900
	;;
	-i | --ip )
		echo "O ip do usuario ${arg2} eh --> ${ip} <--."
	;;
	-s | --ssh )
		user=$(/usr/bin/whoami)
		ssh -XC ${user}@${ip}
	;;
	-v | --version )
		echo "${0} 2.3"
	;;
	-*)
		erroMSG
	;;

	*)
		erroMSG
		helpMSG
	;;
esac
