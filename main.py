import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import time
import yaml
import os
import getopt,sys.argv

def main():
    #Lembrar de adicionar um comando no args pra selecionar um yaml file
    cimc_generate_certificate()

def yaml():


    with open({}).format()
def cimc_get_cookies():

    credentials = {"Username":str(input("Username:")),
                "Password":str(input("Password:"))}

    ip = "10.97.39.42"

    body_credentials = '''<aaaLogin
        inName='{username}'
        inPassword='{password}'>
        </aaaLogin>'''.format(username = credentials["Username"],password = credentials["Password"])


    login_request = requests.post(url="https://"+ip+"/nuova",data=body_credentials, verify= False)
    
    xml = ET.fromstring(login_request.text)

    return xml.attrib["outCookie"]

def cimc_check_certificate():

    cookie = cimc_get_cookies()

    body_check_certificate = '''<configResolveClass 
                                cookie="{}" 
                                classId="currentCertificate" 
                                inHierarchical="false">
                                </configResolveClass>'''.format(cookie)

    check_certificate_request = requests.post(url="https://10.97.39.42/nuova",data=body_check_certificate, verify= False)

    
    xml_date = ET.ElementTree(ET.fromstring(check_certificate_request.text))
    
    

    for element in xml_date.iter('currentCertificate'):
        date = element.attrib["validTo"]

    return date

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



 