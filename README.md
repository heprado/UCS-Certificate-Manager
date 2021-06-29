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

#### Exemplo config.yaml

~~~
config:
  credentials:
    username: "admin" #Usuário que será utilizado para autenticar com a CIMC
    password: "1234Qwer" #Senha que será utilizada para autenticar com a CIMC
  hosts:
    - "10.97.39.42" #IP ou FQDN das CIMCs, não coloque "https:// or http://"
    # Podemos adicionar mais IPs ou FQDNs nessa lista, exemplos:
    # -"10.97.39.40"
    # -"paranoid-void-cimc.cisco.com

    



  certificate:
    commonName: "Cisco"  #Commom name que será usado para gerar o certificado auto-assinado, qualquer string
    organization: "Cisco" #organization que será usada para gerar o certificado auto-assinado, qualquer string
    organizationalUnit: "TI" #organizationalUnit que será usado para gerar o certificado auto-assinado, qualquer string
    locality: "Brazil" #locality que será usado para gerar o certificado auto-assinado, qualquer string
    state: "Sao Paulo" #State que será usado para gerar o certificado auto-assinado, qualquer string
    countryCode: "Brazil" ##countryCode que será usado para gerar o certificado auto-assinado, utilize o nome do país em Inglês 
~~~

#### Exemplo "output.yaml"

~~~
out_config:
  new_expiracy_date:
    10.97.39.42: Jun 28 17:48:30 2026 GMT
  old_expiracy_date:
    10.97.39.42: Jun 28 17:47:03 2026 GMT
~~~
