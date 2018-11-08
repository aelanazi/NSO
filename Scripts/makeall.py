import os

path = "/usr/local/nsoadmin/NSO_RUN_DIR/packages/"
dirs = os.listdir( path )
for dir in dirs:
	if(dir != "makeall.py" and (dir.startswith('ea') or dir.startswith('el') or dir.startswith('mef'))):
		cwd = os.getcwd()
 		os.chdir(cwd+"/"+dir+"/src")
		os.system("make clean")
		os.system("make all")
		os.chdir("../../")

