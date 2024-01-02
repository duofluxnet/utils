import os

"""
ls -x /sys/module/*/parameters
...

/sys/module/virtio_pci/parameters:
force_legacy

/sys/module/vt/parameters:
color      cur_default  default_blu  default_grn  default_red  default_utf8  global_cursor_default  italic
underline

/sys/module/watchdog/parameters:
handle_boot_enabled  open_timeout  stop_on_reboot

/sys/module/wmi/parameters:
debug_dump_wdg  debug_event

...
"""
result = os.popen("/usr/bin/ls -x /sys/module/*/parameters/").read()
for l in result.split("\n"):
    if len(l.strip()) > 0:        
        if l.endswith(":"):
            mod_n = l.replace(":", " ")            
        else:
            for w in l.replace("\t", " ").split(" "):
                if len(w.strip()) > 0:
                    print(mod_n, w.strip(), end="\n")
