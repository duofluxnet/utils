from os import walk
from os.path import join

linux_folder = "/linux"
k_config_count = 0
k_curr_map = {}
k_current_f = open(join(linux_folder, ".config"), "r", encoding="UTF-8", newline="\n")
for l in k_current_f:
    if l.strip().startswith("CONFIG_"):
        k_config_count += 1
        l_k = l.strip().split("=")
        k_curr_map[l_k[0].removeprefix("CONFIG_")] = "=".join(l_k[1:])
k_config_loaded_count = len(k_curr_map)
assert k_config_count == k_config_loaded_count

k_count = 0
k_map = {}
for root, dirs, files in walk(linux_folder):
    for f in files:
        if f == "Kconfig":
            k_count += 1
            k_path = join(root, f)
            k_file = open(k_path, "r", encoding="UTF-8", newline="\n")
            k_map[
                k_path.removeprefix(linux_folder).removesuffix(f)
            ] = k_file.readlines()
            k_file.close()
k_loaded_count = len(k_map.keys())
assert k_count == k_loaded_count

k_map_1 = {}
for k, v in k_map.items():
    k_map_1[k] = []
    for l in v:
        k_map_1[k].append(l.replace("\n", ""))

k_map_2 = {}
for k, v in k_map_1.items():
    k_map_2[k] = []
    for l in v:
        if not l.strip().startswith("#"):
            if len(l.strip()) > 0:
                k_map_2[k].append(l)

k_symbol_count = 0
k_symbol_loaded_count = 0
ks_map = {}
max_k_name_size = 0
for k, v in k_map_2.items():
    ks_map[k] = {}
    max_k_name_size = max(max_k_name_size, len(k))
    current_ksymbol = None
    for l in v:
        if l.startswith("\tconfig") or l.startswith("config") or l.startswith("menuconfig"):
            current_ksymbol = l.split()[1].replace("\t", "")
            ks_map[k][current_ksymbol] = []
            k_symbol_count += 1
        if current_ksymbol:
            ks_map[k][current_ksymbol].append(l)

for k in ks_map.keys():
    k_symbol_loaded_count += len(ks_map[k].keys())
# assert k_symbol_count == k_symbol_loaded_count

k_symbol_final_count = 0
ks_final = {}
k_symbol_in_file = 0
k_symbol_notin_file = 0
for k, v in ks_map.items():
    ks_final[k] = {}
    for sk, sv in v.items():
        ks_final[k][sk] = {}
        ks_final[k][sk]["desc_help"] = ""
        if sk in k_curr_map:
            ks_final[k][sk]["curr"] = k_curr_map[sk]
            k_symbol_in_file += 1
        else:
            # ks_final[k][sk]["curr"] = "n"
            k_symbol_notin_file += 1
        isHelp = False
        ks_final[k][sk]["help"] = []
        for l in sv:
            if l == "\thelp" and not isHelp:
                isHelp = True
                continue
            if isHelp and l.startswith("\t"):
                ks_final[k][sk]["help"].append(l.replace("\t", "").strip())
            else:
                isHelp = False
            if l.startswith("\tbool") or l.startswith("\ttristate"):
                try:
                    ks_final[k][sk]["desc"] = " ".join(l.split()[1:]).replace('"', "")
                except IndexError:
                    ks_final[k][sk]["desc"] = l.replace("\t", "")
        if "desc" not in ks_final[k][sk]:
            ks_final[k][sk]["desc"] = ""
        ks_final[k][sk]["help"] = " ".join(ks_final[k][sk]["help"])

        if len(ks_final[k][sk]["desc"].strip()) > 0:
            ks_final[k][sk]["desc_help"] = ks_final[k][sk]["desc"] + "."
            if len(ks_final[k][sk]["help"].strip()) > 0:
                ks_final[k][sk]["desc_help"] = (
                    ks_final[k][sk]["desc_help"] + " |    " + ks_final[k][sk]["help"]
                )
        else:
            ks_final[k][sk]["desc_help"] = ks_final[k][sk]["help"]

        k_symbol_final_count += 1
(
    k_symbol_loaded_count
    == k_symbol_final_count
    == k_symbol_in_file + k_symbol_notin_file
)
"""
  ks_final = {
    'TTY': {
        'help': 'Allows you to...', 
        'desc': 'Enable TTY if EXPERT'
        'curr': 'y'
      }, 
      ...
  }
"""
f_out = open("/tmp/kconfig_inliner.csv", "w", encoding="UTF-8")
print(
    "{}\t{}\t{}\t{}\t{}".format(
        "K_GROUP", "K_SYMBOL", "K_CURR", "K_DESC", "K_HELP", "K_DESC_HELP"
    ),
    file=f_out,
    end="\n",
)
for kgroup, ksymbol in ks_final.items():
    for k, v in ksymbol.items():
        print(
            # "{}\t{}\t{}\t{}".format(kgroup.ljust(max_k_name_size), k, v["curr"].upper(), v["desc_help"]),
            "{}\t{}\t{}\t{}\t{}".format(
                kgroup,
                k,
                v["curr"] if "curr" in v else "",
                v["desc_help"],
                ("CONFIG_" + k + "=" + v["curr"]) if "curr" in v else "",
            ),
            file=f_out,
            end="\n",
        )
    f_out.flush()
f_out.close()

print(
    "KConfig Files:\t{:,}.\nKConfig Files Loaded:\t{:,}. \
      \n\nConfig File Symbols:\t{:,}.\nConfig File Symbols Loaded:\t{:,}. \
      \n\nKConfig Symbols:\t{:,}.\nKConfig Symbols Loaded:\t{:,}.\nKConfig Symbols Final:\t{:,}. \
      \n\n(a) Symbols Found in Config File:\t{:,}.\n(b) Symbols NOT Found in Config File:\t{:,} (a + b = {:,}).".format(
        k_count,
        k_loaded_count,
        k_config_count,
        k_config_loaded_count,
        k_symbol_count,
        k_symbol_loaded_count,
        k_symbol_final_count,
        k_symbol_in_file,
        k_symbol_notin_file,
        k_symbol_in_file + k_symbol_notin_file,
    )
)
exit(0)