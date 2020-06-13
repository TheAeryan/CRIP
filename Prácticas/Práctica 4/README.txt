---- Tutorial de Uso ----

La funcionalidad de la práctica se ha distribuido entre tres scripts python diferentes: GenerarClaves.py, GenerarFirma.py y
VerificarFirma.py. Estos ficheros serán ejecutados directamente desde el terminal mediante "python3 <nombre_fichero>".
Hay que seguir los siguientes pasos:

1- Ejecutar GenerarClaves desde la terminal (python3 GenerarClaves.py). Se crearán 2 ficheros,
"clave_publica.txt" que tendrá las claves publica de la firma, y "clave_privada.txt", que tendrá la clave publica más el
valor "x", que es la clave privada.

2- Ejecutar el fichero GenerarFirma (python3 GenerarFirma.py). Después de haber insertado el nombre del fichero, se
creará un fichero, "firma.txt", que tendrá la firma del fichero que queríamos firmar, realizada con la clave privada. El fichero
se lee en modo binario ('rb'), por lo que se puede firmar cualquier tipo de fichero.

3- Ejecutar el fichero VerificarFirma (python3 VerificarFirma.py). Después de haber insertado el nombre del fichero, eso
comprobará si la firma es válida, haciendo uso de la clave pública.

