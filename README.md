### Important!
This version of Artillery is using Firewalld and Ipset so please make sure that you install them otherwise it will not work. This is also going to be custom version that will be sligtly modified in different ways for my liking.

You will also need to have GeoIP installed please make sure to install it otherwise it will not work. ```pip install GeoIP```

### What has been changed

1. Uses firewalld and ipset instead of iptables for the dropping and automatic port opening and filtering.

2. You can mute alerts that would be sent via email for certain alerts such as on port connect or monitor alerts. It will still be logged but you will not get an email for that alert type.

3. GeoIP is used so when you are alerted in the email it will also give the location, just a nice little feature.

4. ThreatServer banlist.txt updates dynamically.

More planned in the future.

### Introduction to Artillery

Artillery is a combination of a honeypot, monitoring tool, and alerting system. Eventually this will evolve into a hardening monitoring platform as well to detect insecure configurations from nix systems. It's relatively simple, run ```./setup.py``` and hit yes, this will install Artillery in ```/var/artillery``` and edit your ```/etc/init.d/rc.local``` to start artillery on boot up.

### Features

1. It sets up multiple common ports that are attacked. If someone connects to these ports, it blacklists them forever (to remove blacklisted ip's, remove them from ```/var/artillery/banlist.txt```)

2. It monitors what folders you specify, by default it checks ```/var/www``` and ```/etc``` for modifications.

3. It monitors the SSH logs and looks for brute force attempts.

4. It will email you when attacks occur and let you know what the attack was.

Be sure to edit the ```/var/artillery/config``` to turn on mail delivery, brute force attempt customizations, and what folders to monitor.

### Bugs and enhancements

For bug reports or enhancements, please open an issue here https://github.com/trustedsec/artillery/issues

### Project structure

For those technical folks you can find all of the code in the following structure:

- ```src/core.py``` - main central code reuse for things shared between each module
- ```src/monitor.py``` - main monitoring module for changes to the filesystem
- ```src/ssh_monitor.py``` - main monitoring module for SSH brute forcing
- ```src/honeypot.py``` - main module for honeypot detection
- ```src/harden.py``` - check for basic hardening to the OS
- ```database/integrity.data``` - main database for maintaining sha512 hashes of filesystem
- ```setup.py``` - copies files to ```/var/artillery/``` then edits ```/etc/init.d/artillery``` to ensure artillery starts per each reboot

### Supported platforms

- Linux
- Windows


Project Artillery - A project by Binary Defense Systems (https://www.binarydefense.com).

Binary Defense Systems (BDS) is a sister company of TrustedSec, LLC
