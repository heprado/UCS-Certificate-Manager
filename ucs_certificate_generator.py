import requests
import xml.etree.ElementTree as ET
import time
import yaml
import os
import argparse

def main():
    
    cimc_check_certificate(cimc_get_cookies())

def menu():

    menu = argparse.ArgumentParser(description="This script generates a new self-signed certificate for the CIMC",
                                    epilog="This program was made by Henrique Prado, if you have any problem with the script open a issue on https://github.com/Tidebinder ")

    menu.add_argument("-f","--file",
                      action='store',
                      metavar="file",      
                      type=str,
                      help="The full path or the name of the configuration YAML file, just use the name if the configuration file is in the same directory as the script"
                     )

    args = menu.parse_args()

    return args
    

def yaml_read_config():
    file = menu().file

    if "/" not in file:

        try:
            with open("./{}".format(file), 'r') as f:
                    print(file)
                    yaml_file = yaml.safe_load(f)
                    
        except:
            print("The file wasn't found")
    
    if "/" in file:

        try:
            with open("{}".format(file), 'r') as f:
                    print(file)
                    yaml_file = yaml.safe_load(f)
                    
        except:
            print("The file wasn't found")

    return yaml_file
    

def cimc_get_cookies():

    try:
        credentials = yaml_read_config()["config"].get("credentials")
    except:
        print("You didn't put any credentials in the yaml file.")

    body_credentials = '''<aaaLogin
        inName='{username}'
        inPassword='{password}'>
        </aaaLogin>'''.format(username = credentials["username"],password = credentials["password"])

    hosts = yaml_read_config()["config"].get("hosts")

    cookies_dict = {}
    for cimcs in hosts:
        print("Getting the CIMC cookie for {}".format(cimcs))
        
        login_request = requests.post(url="https://"+cimcs+"/nuova",data=body_credentials, verify= False)

        if login_request.status_code == 200:
            
            try:
                xml = ET.fromstring(login_request.text)
                cookie = xml.attrib["outCookie"]
                cookies_dict[cimcs] = cookie
                print("Done!")
            except KeyError:
                print("Could not get Cookie for CIMC {}".format(cimcs))

        else :
            print("The API of the CIMC {} is not available".format(cimcs))
        
    
    return cookies_dict

   

def cimc_check_certificate(cookies_dict):

    
    for cimc,cookie in cookies_dict.items():

        body_check_certificate = '''<configResolveClass 
                                    cookie="{}" 
                                    classId="currentCertificate" 
                                    inHierarchical="false">
                                    </configResolveClass>'''.format(cookie)

        check_certificate_request = requests.post(url="https://"+cimc+"/nuova",data=body_check_certificate, verify= False)

        
        xml_date = ET.ElementTree(ET.fromstring(check_certificate_request.text))
        
        ##Atualizar a CIMC da UCS 10.97.39.44 porque se nao não consigo pegar o status do certificado

        for element in xml_date.iter('currentCertificate'):
            date = element.attrib["validTo"]
            print(date)

    
    

def cimc_generate_certificate():

     cookie = cimc_get_cookies()

     body_generate_certificate = '''<configConfMo cookie='{}' 
                                                    dn="sys/cert-mgmt/gen-csr-req" inHierarchical="false">
	                                    <inConfig>
	                                        <generateCertificateSigningRequest commonName="Banco do Brasil" organization="Banco do Brasil" 
                                            organizationalUnit="Banco do Brasil" locality="Brazil" state="Brasilia" countryCode="Brazil" 
                                            selfSigned="yes"  dn="sys/cert-mgmt/gen-csr-req"/>
	                                    </inConfig>
                                    </configConfMo>'''.format(cookie)
    
     certificate_request = requests.post(url="https://10.97.39.42/nuova",data=body_generate_certificate, verify= False)
     
     
     
     if certificate_request.status_code == 200:
        
        xml_cert_status = ET.ElementTree(ET.fromstring(certificate_request.text))
     
        for child in xml_cert_status.iterfind('./outConfig/'):
            status = child.attrib["csrStatus"]
            
            
        if status == "Completed CSR":
            
            check_cimc_up = requests.get(url = "https://10.97.39.42/login.html",verify= False)
            

            while check_cimc_up.status_code == 502:
                print("Waiting for CIMC to generate Self-Signed Certificate...")
                time.sleep(10)
                check_cimc_up = requests.get(url = "https://10.97.39.42/login.html",verify= False)
            
            
            if check_cimc_up.status_code == 200:
                time.sleep(10)
                date = cimc_check_certificate()
                print("Done")
            
            return date
                

        


if __name__ == "__main__":

    main()



 