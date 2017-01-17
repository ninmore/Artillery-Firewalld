#!/usr/bin/python
################################################################################
#
#  Artillery - An active honeypotting tool and threat intelligence feed
#
# Written by Dave Kennedy (ReL1K) @HackingDave
#
# A Binary Defense Project (https://www.binarydefense.com) @Binary_Defense
#
################################################################################
import time
import sys
# needed for backwards compatibility of python2 vs 3 - need to convert to threading eventually
try: import thread
except ImportError: import _thread as thread
import os
import subprocess

# check if its installed
if not os.path.isfile("/var/artillery/artillery.py"):
    print("[*] Artillery is not installed, running setup.py..")
    subprocess.Popen("python setup.py", shell=True).wait()
    sys.exit()

from src.core import *
# from src.config import * # yaml breaks config reading - disabling

# create the database directories if they aren't there
if not os.path.isdir("/var/artillery/database/"):
    os.makedirs("/var/artillery/database/")
if not os.path.isfile("/var/artillery/database/temp.database"):
    filewrite = open("/var/artillery/database/temp.database", "w")
    filewrite.write("")
    filewrite.close()

# let the logfile know artillery has started successfully
write_log("[*] %s: Artillery has started successfully." % (grab_time()))
if is_config_enabled("CONSOLE_LOGGING"):
    print("[*] %s: Artillery has started successfully.\n[*] Console logging enabled.\n" % (grab_time()))

# prep everything for artillery first run
check_banlist_path()

try:
    # update artillery
    if is_config_enabled("AUTO_UPDATE"):
        thread.start_new_thread(update, ())
        print("[*] Auto Update Checked!")

    # import base monitoring of fs
    if is_config_enabled("MONITOR"):
        from src.monitor import *
    print("[*] Monitor Enabled!")

    # port ranges to spawn
    port = read_config("PORTS")

    # if we are running posix then lets create a new ipset alias
    if is_posix():
        time.sleep(2)
        create_ipset_subset()
        print("[*] ipset's done!")
        # start anti_dos
        import src.anti_dos
        print("[*] Anti-Dos done!")
        
    # spawn honeypot
    import src.honeypot
    print("[*] Honeypot spawned!")

    # spawn ssh monitor
    if is_config_enabled("SSH_BRUTE_MONITOR"):
        import src.ssh_monitor
        print("[*] SSH Monitor Started!")

    # spawn ftp monitor
    if is_config_enabled("FTP_BRUTE_MONITOR"):
        import src.ftp_monitor
        print("[*] FTP Monitor started!")

    # start monitor engine
    import src.monitor
    print("[*] Monitor Engine Started!")

    # check hardening
    import src.harden
    print("[*] Harden check done!")

    # start the email handler
    import src.email_handler
    print("[*] Email Handler started!")

    # check to see if we are a threat server or not
    if is_config_enabled("THREAT_SERVER"):
        thread.start_new_thread(threat_server, ())
        print("[*] Threat Server enabled!")

    # recycle IP addresses if enabled
    if is_config_enabled("RECYCLE_IPS"):
        thread.start_new_thread(refresh_log, ())

    # pull additional source feeds from external parties other than artillery
    # - pulls every 2 hours or ATIF threat feeds
    thread.start_new_thread(pull_source_feeds, ())
    print("[*] Pulled extra source feeds!")
    
    print("[*] Artillery started!")

    # let the program to continue to run
    while 1:
        try:
            time.sleep(100000)
        except KeyboardInterrupt:
            print("\n[!] Exiting Artillery... hack the gibson.\n")
            write_log("[!] %s: Artillery has been stopped." % (grab_time()))
            cleanup_artillery()
            sys.exit()

#except sys.excepthook as e:
#    print("Excepthook exception: " + format(e))
#    pass

except KeyboardInterrupt:
    cleanup_artillery()
    sys.exit()

except Exception as e:
    print("General exception: " + format(e))
    cleanup_artillery()
    sys.exit()
