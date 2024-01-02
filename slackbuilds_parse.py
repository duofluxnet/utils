#------------------------------------------------------------------------------
# slackbuilds_parse.py (Python 3.9.18 / x86_64)
#
# THIS PROGRAM PIPELINES SlackBuild.org PACKAGES INFORMATION FILES ONTO A 
# MySQL (MariaDB) DATABASE MODEL TO ENABLE SQL ANLAYSIS AND UTILITIES BUILD.
#
# maintainer: duoflux (duofluxnet@gmail.com);
# ------------------------------------------------------------------------------
# TODO: 4) Wrap 'SlackBuild_INSTALLER.sql' onto a fairly fucking good CLI util;
# TODO: 5) Wrap 'SlackBuild_SEARCH.sql'    onto a fairly fucking good CLI util;
# ------------------------------------------------------------------------------

import time

p_path = "/opt/slackbuilds/15.0/"
f_name = "SLACKBUILDS.TXT"
t_file = "TAGS.txt"
r_file = "README"
s_file = "slack-desc"
i_file_ext = ".info"

db_name = "slackbuilds"

f = open(p_path + f_name, "r", newline="\n")
# little fucking trick to put all text blocks in one liner (a.k.a.: the "disguised double-feeder")
print("{}: Reading PACKAGES file '{}' onto memory...".format(time.time(), f_name))
data = (
    "".join(f.readlines()).replace("\n\n", "||").replace("\n", "\t").replace("||", "\n")
)

pack_elements = [
    "SLACKBUILD LOCATION",
    "SLACKBUILD VERSION",
    "SLACKBUILD REQUIRES",
    "SLACKBUILD SHORT DESCRIPTION",
    "SLACKBUILD DOWNLOAD",
    "SLACKBUILD DOWNLOAD_x86_64",
]
print("{}: Parsing PACKAGES data...".format(time.time()))
pack_dict = {}
for line in data.split("\n"):
    pack = line.split("\t")
    for pack_element in pack:
        pack_kv = pack_element.split(":")
        pack_k = pack_kv[0].strip()
        pack_v = ":".join(pack_kv[1:]).strip() if len(pack_kv) > 1 else ""
        if pack_k.startswith("SLACKBUILD NAME"):
            key = pack_v
            pack_dict[key] = {}
        if pack_k in pack_elements:
            vkey = pack_k.removeprefix("SLACKBUILD ")
            if vkey in ["REQUIRES", "DOWNLOAD", "DOWNLOAD_x86_64"]:
                pack_dict[key][vkey] = pack_v.split()
            elif vkey == "LOCATION":
                pack_dict[key]["DIRECTORY"] = pack_v
                pack_dict[key][vkey] = pack_v.split("/")[1]
            else:
                pack_dict[key][vkey] = pack_v

f.close()

print("{}: Reading TAGS file '{}' onto memory...".format(time.time(), t_file))
tag_dict = {}
f = open(p_path + t_file, "r")
for line in f.readlines():
    tag_element = line.split(":")
    tag_k = tag_element[0].strip()
    tag_v = "".join(tag_element[1:]).replace("\n", "").strip().split(",")
    if (len(tag_v) > 0) and (not tag_v[0].startswith("No tags found for ")):
        if len(tag_v) == 1:
            tag_v = tag_v[0].split(" ")
        tag_dict[tag_k] = tag_v

print("{}: Parsing TAGS data...".format(time.time()))
for k, v in tag_dict.items():
    pack_dict[k]["TAGS"] = v

f.close()


print("{}: Reading {} files onto memory...".format(time.time(), r_file))
f_cnt = 0
for k, v in pack_dict.items():
    f = open(
        p_path + pack_dict[k]["DIRECTORY"] + "/" + r_file,
        "r",
        newline="\n",
        encoding="UTF-8",
    )
    pack_dict[k]["README"] = "".join(f.readlines())
    f_cnt += 1
    f.close()
print("{}: Total of {:,} {} files read.".format(time.time(), f_cnt, r_file))


print("{}: Reading {} files onto memory...".format(time.time(), s_file))
f_cnt = 0
for k, v in pack_dict.items():
    f = open(
        p_path + pack_dict[k]["DIRECTORY"] + "/" + s_file,
        "r",
        newline="\n",
        encoding="UTF-8",
    )
    parsed_data = []
    line_preffix = "{}{}".format(k, ":")
    for line in f.readlines():
        if line.startswith(line_preffix):
            parsed_data.append(line.removeprefix(line_preffix))
    pack_dict[k]["SLACK_DESC"] = "".join(parsed_data)
    f_cnt += 1
    f.close()
print("{}: Total of {:,} {} files read.".format(time.time(), f_cnt, s_file))


print("{}: Reading {} files onto memory...".format(time.time(), i_file_ext))
f_cnt = 0
for k, v in pack_dict.items():
    f = open(
        p_path + pack_dict[k]["DIRECTORY"] + "/" + k + i_file_ext,
        "r",
        newline="\n",
        encoding="UTF-8",
    )
    for line in f.readlines():
        data = line.split("=")
        if data[0] in ["MAINTAINER", "EMAIL", "HOMEPAGE"]:
            pack_dict[k][data[0]] = (
                data[1].replace('"', "").replace("\n", "") if len(data) > 1 else None
            )
    f_cnt += 1
    f.close()
print("{}: Total of {:,} {} files read.".format(time.time(), f_cnt, i_file_ext))


import mysql.connector

ins_package = "INSERT INTO package (name, version, description, location, directory, readme, slack_desc, maintainer_name, maintainer_email, website_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
row_package = []

ins_tag = "INSERT INTO tag  (package_name, name)  VALUES (%s, %s)"
row_tag = []

ins_requires = "INSERT INTO requires (package_name, name) VALUES (%s, %s)"
row_requires = []

ins_file = "INSERT INTO file (package_name, url) VALUES (%s, %s)"
row_file = []

print("{}: Processing SQL commands...".format(time.time()))
# slackbuilds.package
for pack, details in pack_dict.items():
    row_package.append(
        (
            pack,
            details["VERSION"],
            details["SHORT DESCRIPTION"],
            details["LOCATION"],
            details["DIRECTORY"],
            details["README"],
            details["SLACK_DESC"],
            details["MAINTAINER"] if "MAINTAINER" in details else None,
            details["EMAIL"] if "EMAIL" in details else None,
            details["HOMEPAGE"] if "HOMEPAGE" in details else None,
        )
    )

# slackbuilds.tag
for pack, details in pack_dict.items():
    if "TAGS" in details:
        for tag in details["TAGS"]:
            row_tag.append((pack, tag))

# slackbuilds.requires
for pack, details in pack_dict.items():
    if "REQUIRES" in details:
        for require in details["REQUIRES"]:
            row_requires.append((pack, require))

# slackbuilds.file
for pack, details in pack_dict.items():
    if len(details["DOWNLOAD_x86_64"]) > 0:
        for files in details["DOWNLOAD_x86_64"]:
            row_file.append((pack, files))
    else:
        for files in details["DOWNLOAD"]:
            row_file.append((pack, files))

print("{}: Connecting to '{}' database...".format(time.time(), db_name))
cx = mysql.connector.connect(
    user="root", password="df", host="127.0.0.1", database=db_name
)
if cx and cx.is_connected():
    cr = cx.cursor()

    print("{}: Truncating package table...".format(time.time()))
    cr.execute("TRUNCATE TABLE package")
    cx.commit()
    print("{}: Populating package table...".format(time.time()))
    row_cnt = 0
    for row in row_package:
        cr.execute(ins_package, row)
        row_cnt += 1
    cx.commit()
    print("{}: Total of {:,} rows inserted.".format(time.time(), row_cnt))

    print("{}: Truncating tag table...".format(time.time()))
    cr.execute("TRUNCATE TABLE tag")
    cx.commit()
    print("{}: Populating tag table...".format(time.time()))
    row_cnt = 0
    for row in row_tag:
        cr.execute(ins_tag, row)
        row_cnt += 1
    cx.commit()
    print("{}: Total of {:,} rows inserted.".format(time.time(), row_cnt))

    print("{}: Truncating requires table...".format(time.time()))
    cr.execute("TRUNCATE TABLE requires")
    cx.commit()
    print("{}: Populating requires table...".format(time.time()))
    row_cnt = 0
    for row in row_requires:
        cr.execute(ins_requires, row)
        row_cnt += 1
    cx.commit()
    print("{}: Total of {:,} rows inserted.".format(time.time(), row_cnt))

    print("{}: Truncating file table...".format(time.time()))
    cr.execute("TRUNCATE TABLE file")
    cx.commit()
    print("{}: Populating file table...".format(time.time()))
    row_cnt = 0
    for row in row_file:
        cr.execute(ins_file, row)
        row_cnt += 1
    cx.commit()
    print("{}: Total of {:,} rows inserted.".format(time.time(), row_cnt))

    print("{}: Closing connections and exiting...".format(time.time()))
    cr.close()
    cx.close()
    exit(0)

else:
    print(
        "{}: Could NOT connect to {} database. Halting...".format(time.time(), db_name)
    )
    exit(-1)

"""
-------------------------------------------------------------------------------------------
'AstroImageJ':  {
        "LOCATION": "audio",
        "VERSION": "0.10.4",
        "DOWNLOAD": [
            "https://slackware.uk/~urchlay/src/aeolus-0.10.4.tar.bz2",
            "http://kokkinizita.linuxaudio.org/linuxaudio/downloads/stops-0.4.0.tar.bz2",
        ],
        "DOWNLOAD_x86_64": [],
        "REQUIRES": ["zita-alsa-pcmi", "clxclient", "jack"],
        "SHORT DESCRIPTION": "aeolus (pipe organ emulator)",
        "TAGS": ["aeolus", "pipe organ", "emulation"],
}, ...
"""
