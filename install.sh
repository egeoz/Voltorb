#/bin/bash

mkdir -vp /etc/Voltorb
cp -v main.py /etc/Voltorb/
cp -v MainWindow.ui /etc/Voltorb/
cp -v icon.png /etc/Voltorb/
cp -v voltorb_service.py /etc/Voltorb/
cp -v config /etc/Voltorb/
cp -v gen_values /etc/Voltorb/
cp -v battery_values /etc/Voltorb/
cp -v perf_values /etc/Voltorb/


cp -v voltorb /usr/local/bin/
chmod +x /usr/local/bin/voltorb
cp -v Voltorb.desktop /usr/share/applications/
chmod 755 /usr/share/applications/Voltorb.desktop

cp -v voltorb.service /etc/systemd/system/

pip3 install undervolt

