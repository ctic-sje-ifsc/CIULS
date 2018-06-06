#!/bin/bash
## Script para pegar do dk o ip que o usuario especificado esta conectado

arg1=${1}
arg2=${2}
BRED='\033[1;31m'
NC='\033[0m' # No Color

### Funcao numero da versao ###
version() {
echo "${0} - Versão 2.6alpha"
}

### Funcao mensagem de erro ###
erroMSG() {
echo "Sintaxe errada. Exemplo:"
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
-v, --version     Exibe a versão do software."
}

############## Inicio do programa #########################
if [ $# -gt 2 ] ;
    then
	erroMSG
        exit 1 
elif [ $# -eq 0 ] ;
    then
	erroMSG
        exit 1 
elif [ ${arg1} = "-h" ] || [ ${arg1} = "--help" ] ;
    then
	helpMSG
	exit 1 
elif [ ${arg1} = "-v" ] || [ ${arg1} = "--version" ] ;
    then
	version
	exit 1 
elif [ -z ${arg2} ] ;
    then
	arg2=${arg1}
	arg1=$(echo "-i")
fi

rep=$(ssh -q root@dk /usr/bin/smbstatus | grep ${arg2} |wc -l)
rep=$(echo "${rep} / 2" |bc)

if [ ${rep} -eq 1 ] ;
	then
		choice=1
elif [ ${rep} -ge 2  ] ;
	then
		echo "Foram encontrado ${rep} usuários!"
                lista
                echo -n "Qual sua escolha: "
                read choice
elif [ ${rep} -lt 1 ];
	then
                erroMSG
                helpMSG
                exit 1
fi

ip=$(ssh -q root@dk /usr/bin/smbstatus | grep ${arg2} |head -n ${choice} |tail -n 1 | cut -d "(" -f2 | cut -d ")" -f1 )

test=$(echo "${ip}" |cut -d ":" -f1)
ipv6=$(echo "2804")
if [ -z ${test} ];
    then
        ip=$(echo "${ip}" |cut -d ":" -f4)
	if [ -z ${ip} ];
	    then
		echo -e "O usuário ${BRED}${arg2}${NC} não possui nenhum IP relacionado."
		exit 1
	fi
fi

case ${arg1} in
	-g | --grafico )
		vinagre [${ip}]::5900
	;;
	-i | --ip )
		user=$(ssh -q root@dk /usr/bin/smbstatus | grep ${arg2} |head -n ${choice} |tail -n 1 |awk '{print $2}' )
		echo -e "O ip do usuario ${BRED}${user}${NC} é ${BRED}${ip}${NC}."
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