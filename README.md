# Cyberpunk inspired authentication
====================================

Inspirado no terminal de hacking de Cyberpunk 2077, usando
uma matriz com valores hexadecimais, combinando e gerando uma senha aleatória
para acessar o terminal 

Conta com um menu pos-autenticaçao para sair e acessar o terminal , 
opçoes para modificar e iniciar serviços e afins, podendo ser customizado
e alterado.

Projeto pessoal para usar no meu proprio terminal, como um script
de inicializaçao no boot

## Uso

E necessario instalar certos pacotes, caso nao estejam instalados

> pip install -r requirements.txt

> python3 init.py


Por ser um projeto pessoal, o audio e algumas opções estão em japonês, pois foi inspirado no jogo Cyberpunk 2077 e feito como um aspiração à um terminal da Arasaka Corp. Sinta-se livre para modificar.


Para deixar mais interessante, voce pode colocar o arquivo init.py
para se iniciar juntamente com seu bash no seu arquivo .zshrc/.bashrc
e criar um terminal com autenticação estilo Fallout.

```shell
 git clone https://github.com/ARCANGEL0/CyberpunkTerminal 

 cd CyberpunkTerminal

 echo "python3 $(pwd)/init.py" >> $HOME/.bashrc
```

Desta forma, toda vez que o terminal do linux for chamado, irá abrir o arquivo
python e o terminal só poderá ser acessado se a senha for corretamente decifrada, o script conta com exceptions para lidar com comandos CTRL para saida ou background do processo e evitar acesso não autorizado.

Após 4 tentativas, o terminal é bloqueado.


## Menu de opções

O menu de opções consta com alguns serviços do meu terminal próprio ( como apache, mysql, snapd )
que podem ser inicializados pelo próprio script, como uma shell interativa
Sinta-se a vontade para adicionar seus próprios selects e modificar ao seu gosto


## Geraçao da senha

A senha do terminal e gerada a partir de um arquivo de texto (pass) , que busca os valores hex e gera uma delas
aleatoriamente como senha do sistema
Para visualizar qual a senha escolhida, basta digitar
> [/ADMIN.F PASS] 

no terminal do login para visualizar a senha atual.



## Terminal

Para aderir mais ao estilo retro de Terminal,
recomendo o cool-retro-term de Swordfish90

Deixarei um arquivo .json de personalização para dar um ar "mais cyberpunk".
(https://github.com/Swordfish90/cool-retro-term)
