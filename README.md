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
 **ucs_certificate_generator.py -f config.yaml -o output.yaml**
~~~
O **"output.yaml"** vai ser salvo no mesmo diretório em que o script for executado.



### YAML



