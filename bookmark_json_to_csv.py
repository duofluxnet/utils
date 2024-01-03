data = [
    {
        "name": "Mesa (computer graphics) - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Mesa_(computer_graphics)#:~:text=Mesa%2C%20also%20called%20Mesa3D%20and,vendor%2Dspecific%20graphics%20hardware%20drivers.",
    },
    {
        "name": "The Linux Kernel documentation — The Linux Kernel documentation",
        "url": "https://www.kernel.org/doc/html/latest/index.html",
    },
    {
        "name": "General troubleshooting - ArchWiki",
        "url": "https://wiki.archlinux.org/title/General_troubleshooting#Scrollback",
    },
    {
        "name": "Logando automaticamente no Slackware [Dica]",
        "url": "https://www.vivaolinux.com.br/dica/Logando-automaticamente-no-Slackware",
    },
    {"name": "SlackBuilds.org", "url": "https://slackbuilds.org/"},
    {
        "name": "How to mount a qcow2 disk image · GitHub",
        "url": "https://gist.github.com/shamil/62935d9b456a6f9877b5",
    },
    {
        "name": "LKML.ORG - the Linux Kernel Mailing List Archive",
        "url": "https://lkml.org/",
    },
    {
        "name": 'ubuntu - Navigate up and down in "screen" (command) linux - Super User',
        "url": "https://superuser.com/questions/1758690/navigate-up-and-down-in-screen-command-linux",
    },
    {"name": " torvalds/linux", "url": "https://github.com/torvalds/linux"},
    {"name": "Appimage", "url": "https://software.manjaro.org/appimages"},
    {"name": "Electron", "url": "https://www.electronjs.org/apps"},
    {"name": "EveryCircuit", "url": "https://everycircuit.com/app"},
    {"name": "CircuitPython", "url": "https://circuitpython.org/"},
    {
        "name": "Home — Acesso à Informação",
        "url": "https://www.gov.br/acessoainformacao/pt-br",
    },
    {
        "name": "TCP/IP Sockets in C: Practical Guide for Programmers",
        "url": "https://cs.baylor.edu/~donahoo/practical/CSockets/textcode.html",
    },
    {
        "name": "SPARQL 1.1 Query Language",
        "url": "https://www.w3.org/TR/sparql11-query/",
    },
]


for bm in data:
    print(
        '<DT><A HREF="' + bm["url"] + '" ADD_DATE="1702427083">' + bm["name"] + "</A>")
