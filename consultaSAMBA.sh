#!/bin/bash
## Script para pegar do dk o ip que o usuario especificado esta conectado


### melhorias a fazer
### 1 -> arrumar help para não pedir nome de usuario
### 2 -> arrumar conexão via vinagre,  ipv4 ou [ipv6]
###   -> 7053      diego.sarda   Domain Users  sj-manut-744529 (2804:1454:1004:200:cd22:ab23:e27f:2a18)
###   -> 6683      rmartins      Domain Users               (2804:1454:1004:120:feaa:14ff:fefc:b655)
### 3 -> possibilidade de mudar a ordem das opções???



erroMSG() {
echo "Sintaxe errada, diferencie maiusculas das minusculas. Exemplo:"
echo "Uso: $0 [[OPÇÃO...] [USUARIO]])"
}

if [ $# -gt 2 ] ;
    then
	erroMSG
        exit
fi

ip=$(ssh -q root@dk /usr/bin/smbstatus | grep ${2} |awk '{print $5}' |head -n 1 |tail -n     1 |awk '{print substr($0,2,length()-2);}')
case ${1} in
	"-h" | "--help")
		echo "-g, --grafico	Abre o Vinagre para ter acesso remoto."
		echo "-h, --help	Exibe esta ajuda."
		echo "-i, --ip		Exibe apenas o ip do usuário."
		echo "-s, --ssh		Abre uma conexão remota via ssh entre 
			o usuário logado e o usuário remoto."
		echo "-v, --version	Exibe a versão do software."
	;;
	"-g" | "--grafico")
		vinagre [${ip}]::5900
	;;
	"-i" | "--ip" | "")
		echo "O ip do usuario ${1} eh --> ${ip} <--."
	;;
	"-s" | "--ssh")
		user=$(/usr/bin/whoami)
		ssh -XC ${user}@${ip}
	;;
	"-v" | "--version" | "")
		echo "${0} 2.00"
	;;
	*)
		erroMSG
	;;
esac
