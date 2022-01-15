from posixpath import basename
import sys, os, json, shutil

def setFileToAvailableDir(maxPartSizeMB, filesizeMb, directories, filePath):
    if filesizeMb > maxPartSizeMB:
        raise Exception('El archivo es mas grande que el limite del paquete')
    setted =False
    for dir in directories:
        if(dir['size'] <maxPartSizeMB and 
            filesizeMb <(maxPartSizeMB-dir['size'])):
            dir['size'] = dir['size']+filesizeMb
            dir['files'].append(filePath)
            setted =True
            break
    if(setted !=True):
        directories.append(
            {
                "prefix":"_"+str(len(directories)),
                "files":[],
            "size":0.0}
        )
        setFileToAvailableDir(maxPartSizeMB, filesizeMb, directories, filePath)

def splitDir(fromDir, toDir, maxPartSizeMB, log):
    directories =[{"prefix":"_0", "size":0.0, "files":[]}]
    for root, dirnames, filenames in os.walk(fromDir):            
        for filename in filenames:
            filesizeMb =((float(os.path.getsize(os.path.join(root, filename)))/1024.0)/1024)
            setFileToAvailableDir(maxPartSizeMB, filesizeMb, directories, os.path.join(root,filename))
    mainDir =os.path.basename(fromDir)
    for newDir in directories:
        newDirName =mainDir+newDir['prefix']
        newDirPath =os.path.join(toDir, newDirName)
        print(".Generando directorio "+newDirPath)
        for filePath in newDir['files']:            
            fromPathFilename =filePath
            toPathFilename =newDirPath+filePath.replace(fromDir, '')
            os.makedirs(os.path.dirname(toPathFilename), exist_ok=True)
            shutil.copy(fromPathFilename, toPathFilename)
        print("..Comprimiendo directorio "+newDirPath)
        zipFilePath =os.path.join(fromDir,newDirPath)
        shutil.make_archive(zipFilePath, 'zip', newDirPath)
        shutil.rmtree(newDirPath)
    if(log =='true'):
        jsonDirectories = json.dumps(directories)
        file =open('packages.json', 'w')
        file.write(jsonDirectories)

def verifyEmptyDir(toDir):
    if len(os.listdir(toDir)):
        raise Exception('El directorio debe estar vacio')

try:
    args =sys.argv
    fromDir =args[1]
    toDir   =args[2]
    maxPartSizeMB =float(args[3])
    log =args[4]
    verifyEmptyDir(toDir)
    splitDir(fromDir, toDir, maxPartSizeMB, log)
    print('Operacion finalizada con exito')
except Exception as e:
    print(str(e))
