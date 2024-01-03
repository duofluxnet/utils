import mysql.connector

ins_package = (
    "INSERT INTO package "
    "(name, version, description, location) "
    "VALUES (%s, %s, %s, %s)"
)
# row_package = ("geert", "vanderkelen", "M", "")
# cr.execute(ins_package, row_package)
# emp_no = cr.lastrowid

cx = mysql.connector.connect(
    user="root", password="df", host="127.0.0.1", database="slackbuilds"
)

if cx and cx.is_connected():
    with cx.cursor() as cr:
        rs = cr.execute("SELECT * FROM package")
        rows = cr.fetchall()
        for row in rows:
            print(row)
        cr.close()

    cx.commit()
    cx.close()
    exit(0)

else:
    exit(-1)

"""
/opt/slackbuilds_sync.sh

/opt/slackbuilds/15.0/SLACKBUILDS.TXT:
SLACKBUILD NAME: OpenFOAM
SLACKBUILD LOCATION: ./academic/OpenFOAM
SLACKBUILD FILES: OpenFOAM.SlackBuild OpenFOAM.info OpenFOAM.sh README slack-desc
SLACKBUILD VERSION: 11
SLACKBUILD DOWNLOAD: https://github.com/OpenFOAM/OpenFOAM-11/archive/version-11/OpenFOAM-11-version-11.tar.gz https://github.com/OpenFOAM/ThirdParty-11/archive/version-11/ThirdParty-11-version-11.tar.gz
SLACKBUILD DOWNLOAD_x86_64: 
SLACKBUILD MD5SUM: 81862ded202dc13eb285d399e2ce1741 fcd80fb7fa8d011d1a055cd30323ae58
SLACKBUILD MD5SUM_x86_64: 
SLACKBUILD REQUIRES: openmpi CGAL
SLACKBUILD SHORT DESCRIPTION:  OpenFOAM (computational fluid dynamics)
"""
