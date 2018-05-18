#!/bin/bash
## Script para pegar do dk o ip que o usuario especificado esta conectado

#### Para arrumar ####
## problema no help, se colocar comando -h dá msg de erro por causa do if [ $# -gt 2 ].
## problema se não colocar variavel -?, definir uma configuração padrão.


erroMSG() {
echo "Sintaxe errada, diferencie maiusculas das minusculas. Exemplo:"
echo "Uso: $0 [[OPÇÃO...] [USUARIO]])"
}

helpMSG() {
echo "-g, --grafico     Abre o Vinagre para ter acesso remoto."
echo "-h, --help        Exibe esta ajuda."
echo "-i, --ip          Exibe apenas o ip do usuário."
echo "-s, --ssh         Abre uma conexão remota via ssh entre
                o usuário logado e o usuário remoto."
echo "-v, --version     Exibe a versão do software."
}

if [ $# -gt 2 ] ;
    then
	erroMSG
        exit
fi

ip=$(ssh -q root@dk /usr/bin/smbstatus | grep ${2} |head -n 1 |tail -n 1 | cut -d "(" -f2 | cut -d ")" -f1)

test=$(echo "${ip}" |cut -d ":" -f1)
ipv6=$(echo "2804")
if [ "${test}" == "${ipv6}" ];
    then
        true
    else
        ip=$(echo "${ip}" |cut -d ":" -f4)
fi

case ${1} in
	"-h" | "--help")
		helpMSG
	;;
	"-g" | "--grafico")
		vinagre [${ip}]::5900
	;;
	"-i" | "--ip")
		echo "O ip do usuario ${1} eh --> ${ip} <--."
	;;
	"-s" | "--ssh")
		user=$(/usr/bin/whoami)
		ssh -XC ${user}@${ip}
	;;
	"-v" | "--version" | "")
		echo "${0} 2.2"
	;;
	*)
		erroMSG
		helpMSG
	;;
esac
