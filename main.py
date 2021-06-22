import requests
import xml.etree.ElementTree as ET


def main():
    cimc_check_certificate()

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
                                cookie="{cookie}" 
                                classId="currentCertificate" 
                                inHierarchical="false">
                                </configResolveClass>'''.format(cookie=cookie)

    check_certificate_request = requests.post(url="https://10.97.39.42/nuova",data=body_check_certificate, verify= False)

    
    xml_cert = ET.fromstring(check_certificate_request.text)
    
    print(xml_cert.tag)

    ##Conseguir pegar a data de validade do certificado e checar se ele ainda está valido. Fazer uma forma de deslogar da CIMC dps de fazer essas coisas pq a CIMC é uma merda.

if __name__ == "__main__":

    main()

    