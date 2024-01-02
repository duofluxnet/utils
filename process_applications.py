from os import walk
from os.path import join
from xdg.DesktopEntry import DesktopEntry

# Name	            24032  (locale=23514)
# GenericName	    13161  (locale=12893)
# Comment   	    11626  (locale=11326)
# Keywords	         1924  (locale= 1857)
# X-KDE-Keywords	 1360  (locale= 1335)
# Exec	              514
# Type	              485
# Categories	      365
# Terminal	          219
# NoDisplay     	  193
# MimeType	          154

for root, dirs, files in walk('/home/df/Desktop/APPLICATIONS'):
    fout = open ('/tmp/fout.csv', "w", encoding="UTF-8")
    print("Desktop File Name", end = '\t', file=fout, flush=False)
    print("Name", end = '\t', file=fout, flush=False)
    print("Generic Name", end = '\t', file=fout, flush=False)
    print("Comments", end = '\t', file=fout, flush=False)
    print("Command", end = '\t', file=fout, flush=False)
    print("Terminal/UI", end = '\t', file=fout, flush=False)
    print("Display", end = '\t', file=fout, flush=False)
    print("Show", end = '\t', file=fout, flush=False)
    print("MIME Types", end = '\t', file=fout, flush=False)
    print("Categories", end = '\t', file=fout, flush=False)
    print("Keywords", end = '', file=fout, flush=False)
    print(end='\n', file=fout, flush=False)

    for file in files:
        de = DesktopEntry(join(root, file))
        print(file, end = '\t', file=fout, flush=False) 
        print(de.getName(), end = '\t', file=fout, flush=False)
        print(de.getGenericName(), end = '\t', file=fout, flush=False)
        print(de.getComment(), end = '\t', file=fout, flush=False)
        print("\"" + de.getExec() + "\"", end = '\t', file=fout, flush=False)
        print("Terminal" if de.getTerminal() else "UI", end = '\t', file=fout, flush=False)
        print("NoDisplay" if de.getNoDisplay() else "OnDisplay", end = '\t', file=fout, flush=False)
        print("Hidden" if de.getHidden() else "Shown", end = '\t', file=fout, flush=False)
        print(", ".join(de.getMimeTypes()), end = '\t', file=fout, flush=False)
        print(", ".join(de.getCategories()), end = '\t', file=fout, flush=False)
        print(", ".join(de.getKeywords()), end = '', file=fout, flush=False)
        print(end='\n', file=fout, flush=False)
        fout.flush()

    fout.close()

"""      
        with open(file_path, "r",  encoding="UTF-8", newline='\n') as f:
            for line in f:
                l = line.strip()
                if l == "":
                    continue
                if l.startswith('#'):
                    continue
                if l.startswith("[Desktop Entry]"):
                    continue
                if l.find('=') > -1:
                    print(line)
                    fout.flush()
            f.close()
"""            