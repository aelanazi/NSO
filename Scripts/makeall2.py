import os

path = "/usr/local/nsoadmin/NSO_RUN_DIR/packages/"
dirs = os.listdir( path )
for dir in dirs:
	if(dir != "makeall.py" and (dir.startswith('c') or dir.startswith('l'))):
		cwd = os.getcwd()
 		os.chdir(cwd+"/"+dir+"/src")
		os.system("make clean")
		os.system("make all")
		os.chdir("../../")
