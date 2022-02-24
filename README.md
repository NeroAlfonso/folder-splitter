## folder-splitter  
Esta herramienta permite crear archivos .zip que pueden ser descomprimidos de forma individual (selecciona archivos) y respeta las rutas originales.  
#### ¿Como usar? 
- /ruta/origen = directorio a separar y comprimir
- /ruta/destino = directorio donde se almacenarán los archivos resultantes (comprimidos)
- tamaño = tamaño en MB de cada uno de los archivos. Los archivos tendrán este tamaño o el máximo cercano posible, debido a la selección de archivos  
- registro = genera una especificación de los paquetes creados en formato .json (true o false)  
- omitirImágenesVacías = omite las imágenes que son solo transparencia (true o false)  
`
python3 splitter.py /ruta/origen /ruta/destino tamaño registro omitirImágenesVacías
`  
Ejemplo:
`
python3 splitter.py /home/louis/archivos /home/louis/archivos_comprimidos 50 true true
`  
Ejemplo docker:
`
docker run -it --rm -e MAX_FILE_SIZE=<tamaño> -e LOG=<registro> -e SKIP_VOID_IMAGES=<omitirImágenesVacías> --entrypoint ./entrypoint.sh -v </ruta/origen>:/app/src -v </ruta/destino>:/app/dst -v <RUTA_FOLDER_SPLITTER>:/app --network=<NETWORK> python_folder_splitter:1.0.0
`  
> Esta instrucción generará una serie de archivos comprimidos en el directorio /home/louis/archivos_comprimidos que no superarán los 50MB de tamaño y contendrán los archivos del directorio /home/louis/archivos. Además generará una especificación de los paquetes creados (packages.json). También omitirá las imágenes que contienen solo una transparencia