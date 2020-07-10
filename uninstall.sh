#/bin/bash

systemctl disable voltorb.service --now

rm -vrf /etc/Voltorb

rm -v /usr/local/bin/voltorb
rm -v /usr/share/applications/Voltorb.desktop

rm -v /etc/systemd/system/voltorb.service
