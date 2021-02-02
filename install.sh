#!/bin/sh -ex
PORT=3618
UPDATE_SERVER=http://192.168.4.203:8018
ROOT=/home/tt_signer
mkdir -p ${ROOT}
wget -c -O${ROOT}/tt_signer ${UPDATE_SERVER}/tt-signer
wget -c -O${ROOT}/node_modules.tgz ${UPDATE_SERVER}/node_modules.tgz
(cd ${ROOT} && chmod +x tt_signer && tar -zxvf node_modules.tgz)
cat<<EOT>${ROOT}/config.json
{
    "port": "${PORT}"
}
EOT
# cp tt-signer ${ROOT}/
cat<<EOT>/etc/systemd/system/tt_signer.service
[Unit]
Description=TT_Signer
After=network.target
Wants=network.target

[Service]
Type=simple
ExecStart=${ROOT}/tt_signer
Restart=always
RestartSec=20s
User=nobody
LimitNOFILE=infinity

[Install]
WantedBy=multi-user.target
EOT
systemctl enable tt_signer
systemctl restart tt_signer
systemctl status tt_signer

curl http://localhost:${PORT}/api/v1/version
