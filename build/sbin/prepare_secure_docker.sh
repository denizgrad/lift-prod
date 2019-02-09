#!/usr/bin/env bash
sudo cp -r /home/core/liftnec/install/registry/opt /
docker run -d --name registry -v /opt/registry:/opt/registry -p 443:5000 --restart always --env-file /opt/registry/config/registry.env registry:2
echo "Alttaki komutları diger nodelarda çalıştır."
echo "sudo mkdir -p /etc/docker/certs.d/<corehub_ip>"
echo "sudo scp core@<corehub_ip>:/opt/docker/registry/ca.pem /etc/docker/certs.d/<corehub_ip>/ca.crt"