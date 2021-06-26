import requests
import xml.etree.ElementTree as ET
import time
import yaml
import os
import argparse
import sys


def main():

    try:
        credentials = yaml_read_config()["config"].get("credentials")
    except:
        print("You didn't put any credentials in the yaml file.")
        sys.exit()

    try:
        certificate_config = yaml_read_config()["config"].get("certificate")
    except:
        print("You didn't put any certificate configuration in the yaml file.")


    cookies = cimc_get_cookies(credentials)

    old_expiracy_date = cimc_check_certificate(cookies)

    new_expiracy_date = cimc_generate_certificate(cookies,certificate_config,credentials)

    yaml_write_config(old_expiracy_date,new_expiracy_date)
    
    

    
   


def menu():

    menu = argparse.ArgumentParser(description="This script generates a new self-signed certificate for the CIMC",
                                   epilog="This program was made by Henrique Prado, if you have any problem with the script open a issue on https://github.com/Tidebinder ")

    menu.add_argument("-f", "--file",
                      action='store',
                      metavar="file",
                      type=str,
                      help="The full path or the name of the configuration YAML file, just use the name if the configuration file is in the same directory as the script"
                      )

    menu.add_argument("-o", "--output",
                      action='store',
                      metavar="output",
                      type=str,
                      help="This will be the name of the output file with all the old certificates expiracy dates and new certificates expiracy dates"
                      )

    args = menu.parse_args()

    return args


def yaml_read_config():
    file = menu().file

    if "/" not in file:

        try:
            with open("./{}".format(file), 'r') as f:
                yaml_file = yaml.safe_load(f)

        except:
            print("The file wasn't found")

    if "/" in file:

        try:
            with open("{}".format(file), 'r') as f:
                yaml_file = yaml.safe_load(f)

        except:
            print("The file wasn't found")

    return yaml_file

def yaml_write_config(old_expiracy_date,new_expiracy_date):
    
    full = {}
    file_name = menu().output
    full["out_config"] = {**old_expiracy_date,**new_expiracy_date}

    try:
        with open("./{}".format(file_name), 'w') as f:
            yaml_convert = yaml.dump(full,f,default_flow_style=False)
    except:
        print("ahnn")


def cimc_get_cookies(credentials):

    body_credentials = '''<aaaLogin
        inName='{username}'
        inPassword='{password}'>
        </aaaLogin>'''.format(username=credentials["username"], password=credentials["password"])

    hosts = yaml_read_config()["config"].get("hosts")

    cookies_dict = {}
    for cimcs in hosts:
        print("Getting the CIMC cookie for {}".format(cimcs))

        login_request = requests.post(
            url="https://"+cimcs+"/nuova", data=body_credentials, verify=False)

        if login_request.status_code == 200:

            try:
                xml = ET.fromstring(login_request.text)
                cookie = xml.attrib["outCookie"]
                cookies_dict[cimcs] = cookie
                print("Done!")
            except KeyError:
                print("Could not get Cookie for CIMC {}".format(cimcs))

        else:
            print("The API of the CIMC {} is not available".format(cimcs))

    return cookies_dict


def cimc_check_certificate(cookies_dict):
    date = {"old_expiracy_date" : {}}
    for cimc, cookie in cookies_dict.items():

        body_check_certificate = '''<configResolveClass 
                                    cookie="{}" 
                                    classId="currentCertificate" 
                                    inHierarchical="false">
                                    </configResolveClass>'''.format(cookie)

        check_certificate_request = requests.post(
            url="https://"+cimc+"/nuova", data=body_check_certificate, verify=False)

        xml_date = ET.ElementTree(
            ET.fromstring(check_certificate_request.text))

        

        for element in xml_date.iter('currentCertificate'):
            date["old_expiracy_date"].update({"{}".format(cimc):element.attrib["validTo"]})
                

    return date


def cimc_generate_certificate(cookies_dict,certificate_config,credentials):

    date = {"new_expiracy_date": {}}

    for cimc, cookie in cookies_dict.items():

        body_generate_certificate = '''<configConfMo cookie='{cookie}' 
                                                        dn="sys/cert-mgmt/gen-csr-req" inHierarchical="false">
                                            <inConfig>
                                                <generateCertificateSigningRequest commonName="{commonName}" organization="{organization}" 
                                                organizationalUnit="{organizationalUnit}" locality="{locality}" state="{state}" countryCode="{countryCode}" 
                                                selfSigned="yes"  dn="sys/cert-mgmt/gen-csr-req"/>
                                            </inConfig>
                                        </configConfMo>'''.format(cookie=cookie,
                                                                  commonName=certificate_config["commonName"],
                                                                  organization=certificate_config["organization"],
                                                                  organizationalUnit=certificate_config["organizationalUnit"],
                                                                  locality=certificate_config["locality"],
                                                                  state=certificate_config["state"],
                                                                  countryCode=certificate_config["countryCode"])

        certificate_request = requests.post(
            url="https://"+cimc+"/nuova", data=body_generate_certificate, verify=False)

        

        if certificate_request.status_code == 200:

            xml_cert_status = ET.ElementTree(
                ET.fromstring(certificate_request.text))

            for child in xml_cert_status.iterfind('./outConfig/'):
                status = child.attrib["csrStatus"]

            if status == "Completed CSR":

                check_cimc_up = requests.get(
                    url="https://"+cimc+"/login.html", verify=False)

                while check_cimc_up.status_code == 502:
                    print("Waiting for CIMC to generate Self-Signed Certificate...")
                    time.sleep(10)
                    check_cimc_up = requests.get(
                        url="https://"+cimc+"/login.html", verify=False)

                if check_cimc_up.status_code == 200:
                    time.sleep(10)
                    for cimc, cookie in cimc_get_cookies(credentials).items():
                        
                        
                        body_check_certificate = '''<configResolveClass 
                                        cookie="{}" 
                                        classId="currentCertificate" 
                                        inHierarchical="false">
                                        </configResolveClass>'''.format(cookie)

                            
                        check_certificate_request = requests.post(
                            url="https://"+cimc+"/nuova", data=body_check_certificate, verify=False)
                        
                        xml_date = ET.ElementTree(
                            ET.fromstring(check_certificate_request.text))

                        

                        for element in xml_date.iter('currentCertificate'):
                            
                            date["new_expiracy_date"].update({"{}".format(cimc): element.attrib["validTo"]})
    return date



    
if __name__ == "__main__":

    main()
