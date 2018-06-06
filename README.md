# Scripts

Para o Script CIULS funcionar deve-se ter a sua chave pública no usuário root do servidor SAMBA em /root/.ssh/authorized_keys.
Para facilitar o uso do script recomendo colocar em /usr/local/bin (ou qualquer outro que não seja o diretório raiz), editar o arquivo /home/${USUARIO}/.bashrc e adicionar um alias. Exemplo: alias ciuls='bash /usr/local/bin/consultaSAMBA.sh'
