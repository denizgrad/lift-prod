#!/usr/bin/env bash

sudo mkdir -p /opt/registry/{data,ssl,config}
sudo mkdir -p /etc/systemd/system/docker.service.d/

cat /home/core/liftnec/install/registry/opt/registry/config/template_server_openssl.cnf>/home/core/liftnec/install/registry/opt/registry/config/server_openssl.cnf
sudo $(ip a | grep inet | grep -v inet6 | awk '{print $2}' |awk -F"/" '{printf("IP.%d = %s \n",NR, $1)}' >>/home/core/liftnec/install/registry/opt/registry/config/server_openssl.cnf)

# CREATE SSL
sudo openssl genrsa -out /opt/registry/ssl/ca-key.pem 2048
sudo openssl req -x509 -new -nodes -key /opt/registry/ssl/ca-key.pem -days 10000 -out /opt/registry/ssl/ca.pem -subj '/CN=docker-CA'

# create and sign a certificate for the client
sudo openssl genrsa -out /opt/registry/ssl/client_key.pem 2048
sudo openssl req -new -key /opt/registry/ssl/client_key.pem -out /opt/registry/ssl/client_cert.csr -subj '/CN=docker-client' -config /opt/registry/config/client_openssl.cnf
sudo openssl x509 -req -in /opt/registry/ssl/client_cert.csr -CA /opt/registry/ssl/ca.pem -CAkey /opt/registry/ssl/ca-key.pem -CAcreateserial -out /opt/registry/ssl/cert.pem -days 365 -extensions v3_req -extfile opt/registry/config/client_openssl.cnf

# create and sign a certificate for the server
sudo openssl genrsa -out /opt/registry/ssl/server_key.pem 2048
sudo openssl req -new -key /opt/registry/ssl/server_key.pem -out /opt/registry/ssl/server_cert.csr -subj '/CN=docker-server' -config /opt/registry/config/server_openssl.cnf
sudo openssl x509 -req -in /opt/registry/ssl/server_cert.csr -CA /opt/registry/ssl/ca.pem -CAkey /opt/registry/ssl/ca-key.pem -CAcreateserial -out /opt/registry/ssl/server_cert.pem -days 365 -extensions v3_req -extfile /opt/registry/config/server_openssl.cnf

sudo cp -r /home/core/liftnec/install/registry/etc /
sudo systemctl daemon-reload
sudo systemctl restart docker
