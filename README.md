# UCS Certificate Manager

UCS Certificate Manager isé um script em python feito para gerar outro certificado auto-assinado de uma ou diversas CIMCs simultaneamente.

## Instalação

1. Faça download ou clone o repositório.

2. Use o pip para istalar as bibliotecas necessárias.

  **pip istall -r requirements.txt**

## Como usar


### Script

Para usar o UCS Certificate Manager basta chamarmos o script e passarmos o arquivo de configuração YAML, no arquivo [config.yaml](../main/config.yaml) que está na raiz do reposítorio possuimos um exemplo de como preencher ele.

Precisamos especificar o arquivo de saida também, segue abaixo exemplo:
~~~
 ucs_certificate_generator.py -f config.yaml -o output.yaml
~~~
O **"output.yaml"** vai ser salvo no mesmo diretório em que o script for executado.

Também podemos utilizar o -h para obtermos ajuda:

#### Executando ajuda

~~~
 ucs_certificate_generator.py -h
~~~

#### Output 

~~~
usage: ucs_certificate_generator.py [-h] [-f file] [-o output]

This script generates a new self-signed certificate for the CIMC

optional arguments:
  -h, --help            show this help message and exit
  -f file, --file file  The full path or the name of the configuration YAML file, just use the name if the configuration file is in the same directory as the script      
  -o output, --output output
                        This will be the name of the output file with all the old certificates expiracy dates and new certificates expiracy dates

If you have any problem with the script open a issue on https://github.com/Tidebinder, or make your own pull request
~~~


### YAML



