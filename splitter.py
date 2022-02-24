from posixpath import basename
import sys, os, json, shutil
import magic
from PIL import Image
from numpy import asarray

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
        print(".creado directorio lógico_"+str(len(directories)))
        directories.append(
            {
                "prefix":"_"+str(len(directories)),
                "files":[],
            "size":0.0}
        )
        setFileToAvailableDir(maxPartSizeMB, filesizeMb, directories, filePath)
def isTransparent(imageArray):
    if imageArray.sum() ==0:
        return True
    else:
        return False
def splitDir(fromDir, toDir, maxPartSizeMB, log, skipVoidImages):
    imagesFileType =['image/png']
    directories =[{"prefix":"_0", "size":0.0, "files":[]}]
    print('Generando directorios lógicos')
    for root, dirnames, filenames in os.walk(fromDir):            
        for filename in filenames:
            filePath =os.path.join(root, filename)
            if skipVoidImages=='true':
                filetype =magic.from_file(filePath, mime=True)
                if filetype in imagesFileType:
                    image =Image.open(filePath)
                    imageArray = asarray(image)
                    if isTransparent(imageArray):
                        continue
            filesizeMb =((float(os.path.getsize(filePath))/1024.0)/1024)
            setFileToAvailableDir(maxPartSizeMB, filesizeMb, directories, filePath)
    mainDir =os.path.basename(fromDir)
    print('Generando directorios físicos')
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
        #zipFilePath =os.path.join(fromDir,newDirPath)
        #shutil.make_archive(zipFilePath, 'zip', newDirPath)
        #shutil.rmtree(newDirPath)
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
    skipVoidImages =args[5]
    verifyEmptyDir(toDir)
    splitDir(fromDir, toDir, maxPartSizeMB, log, skipVoidImages)
    print('Operacion finalizada con exito')
except Exception as e:
    print(str(e))
