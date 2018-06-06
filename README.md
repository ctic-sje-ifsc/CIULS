# Scripts

Para o Script de consulta LDAP funcionar deve-se ter a sua chave pública no usuário root do monitoramento em /root/.ssh/authorized_keys.
Para facilitar o uso do script recomendo colocar em /usr/local/bin (ou qualquer outro que não seja o diretório raiz), editar o arquivo /home/${USUARIO}/.bashrc e adicionar um alias. Exemplo: alias usuario='bash /usr/bin/consultaSAMBA.sh'
