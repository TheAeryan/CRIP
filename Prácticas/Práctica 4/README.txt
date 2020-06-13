Este archivo no tiene main sino que simplemente se compone de los distintos ficheros dividos por cada parte de la firma.
Para ejecutar el todo:

1- Ejecutar antes el GenerarClaves desde la terminal (python3 GenerarClaves.py). Se creeran 2 ficheros,
"clave_publica.txt" que tendrá las claves publica de la firma, y "clave_privada.txt", que tendrá la clave publica mas el
valor "x", que es clave privada

2- Ejecutar  el fichero GenerarFirma (python3 GenerarFirma.py). Después haber insertado el nombre del fichero, se
creerá un fichero, "firma.txt". qué tendrá la firma del fichero qué queriamos firmar, hecha con la clave privada.

3- Ejecutar el fichero VerificarFirma (python3 VerificarFirma.py). Después haber insertado el nombre del fichero, eso
comprobará si la firma es valida, leyendo la clave publica.