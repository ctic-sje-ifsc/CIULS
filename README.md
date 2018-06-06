# Scripts

Para o Script CIULS funcionar deve-se ter a sua chave pública no usuário root do servidor SAMBA em /root/.ssh/authorized_keys.
Para facilitar o uso do script recomendo colocar em /usr/local/bin (ou qualquer outro que não seja o diretório raiz), editar o arquivo /home/${USUARIO}/.bashrc e adicionar um alias. Exemplo: alias ciuls='bash /usr/local/bin/consultaSAMBA.sh'

Como usar:
```bash
ciuls [opções] [usuário]

Opções
-g, --grafico     Abre o Vinagre para ter acesso remoto.
-h, --help        Exibe esta ajuda.
-i, --ip          Exibe apenas o ip do usuário. [Opção padrão caso o usuário
                  não digitar nada.
-s, --ssh         Abre uma conexão remota via ssh entre
                  o usuário logado e o usuário remoto.
-v, --version     Exibe a versão do software.
```
