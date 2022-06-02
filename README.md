# Ouraddress

## ¿Que es Ouraddress?

Ouraddress es una aplicacion web/REST API que sirve para obtener la latitud y longitud de una calle, dado su nombre de una calle y su codigo municipal (codigo ine) de cualquier parte de España.

## Caracteristicas

* Interfaz web y tambien soporte REST API amigables y faciles de usar
* Emplea la filosofia "map reduce" asi como distribucion en multiprocesos, esto hace que los tiempos de consultas sean "rapidos" (la rapidez dependera de los recursos disponibles del ordenador).

![](https://tutorials.freshersnow.com/wp-content/uploads/2020/06/MapReduce-Job-Execution-Flow.png)

* Codigo abierto y open source, esto significa, ¡que lo puedes usar de forma libre y gratuita!, da igual que seas una empresa, autonomo o persona individual.
* "Rivaliza" (o esa es la idea) con la API de google maps.

## Instrucciones de instalacion

Para usar Ouraddress solo necesitas hacer tres cosas:

1. Tener [docker](https://docs.docker.com/get-started/overview/) instalado y listo para usar en el ordenador que quieras usar como servidor de ouraddress
2. Clonar este repositorio con git

```
git clone https://github.com/guicalare/ouraddress.git
```

3. Crear y montar el servicio con docker (instrucciones para linux)

```

cd ouraddress
sudo docker build -t ouraddress .
sudo docker run -ti --network host ouraddress:latest

```

¡En total (si ya tenias instalado docker) solo se necesitan 4 lineas en la terminal para poder usar esta herramienta!

```

git clone https://github.com/guicalare/ouraddress.git
cd ouraddress
sudo docker build -t ouraddress .
sudo docker run -ti --network host ouraddress:latest

```

## Instrucciones de uso

Una vez has ejecutado el contenedor de ouraddress, veras que aparecera lo siguiente (de ser asi, ¡vamos por el buen camino! :D )

```

/usr/lib/python3.10/site-packages/thefuzz/fuzz.py:11: UserWarning: Using slow pure-python SequenceMatcher. Install python-Levenshtein to remove this warning
warnings.warn('Using slow pure-python SequenceMatcher. Install python-Levenshtein to remove this warning')
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

```

Esto nos indica que el servidor esta listo para recibir bases de datos y peticiones sobre calles. POr lo que ahora abre tu navegador favorito y dirigete a la ip del servidor http://XXX.XXX.XXX.XXX:800.

Para saber la ip del servidor escribe en la terminal el siguiente comando:

```

ifconfig

```

Y tendras que busclar la ip. Generalmente estas suelen empezar por 192.168.1.XXX o 10.XXX.XXX.XXX . Supongamos que sale la ip 192.168.1.144, pues tendras que escribir en el navegador la direccion http://192.168.1.144:8000 y al hacerlo, ¡veras la interfaz web de Ouraddress!

¡Sigue las instrucciones que aparecen en la web y a correr!

## TODO LIST

* Pestaña de monitorizacion del contenedor
* Pestaña de configuracion de parametros de Ouraddress
* Mejorar interfaz y back end

# ¿Q&A?

## Bases de datos

Ouraddress hace uso de las bases de datos del [Instituto Geografico Nacional de España](https://centrodedescargas.cnig.es/CentroDescargas/index.jsp). Puedes ver las instrucciones para descargar y obtener dichas bases de datos en mi otro repositorio [spain.csv calles residenciales](https://github.com/guicalare/spain.csv/tree/main/Calles%20residenciales).

## Me gusta tu proyecto, como te puedo ayudar

1. Dale una estrella a este repositorio y compartelo con otras personas :D
2. Comenta cualquier problema/sugerencia en [esta seccion](https://github.com/guicalare/ouraddress/issues)

## Ouraddress no me devuelve todas las calles que le he dado

Esto se debe a que Ouraddress tiene un "filtro" a la hora de calcular mediante fuzzy match las similitudes entre las calles que das y las calles que tiene regesitradas en sus bases de datos.

Puedes cambiar el nivel del filtro (min match valid) en el archivo [config.json](https://github.com/guicalare/ouraddress/blob/main/docker-build/config.json) por un valor mucho mas bajo (toma valores entre 0 y 100. Cuanto mas alto sea, mas estricto es con las busquedas/menos busquedas te retorna, mientras que cuanto mas bajo es, menos estricto es con las busquedas/mas busquedas te retornara)

Tambien puedes probar diferentes tipos de bases de datos cambiando en el archivo [config.json](https://github.com/guicalare/ouraddress/blob/main/docker-build/config.json), para ello cambia el valor "search folder" de "./search ddbb/fixed/" a "./search ddbb/no fixed/". Esto lo que hace es cambiar la base de datos de busqueda "españolizada" por la base de datos de busqueda "regionales". En resumen, que en la base de datos "./search ddbb/fixed/" no aparecen las versiones de calles como "rua" o "kalea", mientras que en "./search ddbb/no fixed/" si aparecen las calles como "rua" o "kalea", de forma que aumentas las posibilidades de mejorar el match de las calles.

## Ouraddress va lento

Esto depende del input de datos que le has pasado. Cuanto mas grande sea el fichero, mas tiempo tardara Ouraddress en procesarlo, es por ello que se recomiendo que el archivo que uses tenga lo minimo e indispensable para que Ouraddress haga su trabajo. 

Puedes por otra parte incrementar el numero de trabajadores de Ouraddress modificando la variable instances del archivo [config.json](https://github.com/guicalare/ouraddress/blob/main/docker-build/config.json)
