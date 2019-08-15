# Generador de datos faker [![Build Status](https://travis-ci.org/PDNMX/data_faker.svg?branch=master)](https://travis-ci.org/PDNMX/data_faker)


## ¿Qué es y para qué sirve?
Es un generador de datos basado en la definición de los datos y su estructura en formato .json

*Utiliza la librería [Faker] para crear datos sintéticos*
*Integra los catálogos y funciones del proyecto [data_generator] del SESNA*
*Valida el CURP y RFC del declarante*
*Actualmente sólo está integrado el del sistema de declaraciones*

## Dependendecias Generales
```
$ conda create --name <env> --file requirements.txt

donde:
  env -> nombre del ambiente donde se cargaran las dependencias
```


## USO
### Preparación de la base de datos
1. Contar con una base de datos mongo previamente configurada.
2. Setear las variables de entorno para la conexion a la base de datos mongo
```
export DATAFAKE_MONGO_HOST=host
export DATAFAKE_MONGO_PORT=port
export DATAFAKE_MONGO_DB_NAME=dbname
export DATAFAKE_MONGO_USER=user
export DATAFAKE_MONGO_PASS=password
```
### Preparación de la definición de datos
1. Se debe editar la definición de la estructura de los datos agregando el tipo de dato "faker" que se desea tener en cada campo, por ejemplo:

```
"results" : {
            "type" : "array",
            "faker": "int:5",                                                           Indica que se deben agregar 5 datos tipo "object" que forman parte de un arreglo
            "items" : {
              "type" : "object",
              "properties" : {
                "id" : {
                  "type" : "string",
                  "description" : "Identificador del declarante con valor alfanumérico",
                  "example" : "a1b2c3d4",
                  "faker": "seed:document_id"                                          Indica que se debe agregar un dato tipo "string" proveniente de la semilla "seed"  
                  ...
```
Para mayor referencia por favor vea el archivo original de [declaraciones.json] y el archivo editado [declaraciones_with_faker.json]


### Sistema 1 .- Declaraciones

Argumentos
```
usage: main.py [-s {1,2,3}] [-n SAMPLES] [-y YEARS]

optional arguments:
  -s {1,2,3}, --sys {1,2,3}         System number
  -n SAMPLES, --samples SAMPLES     Number of samples
  -y YEARS, --years YEARS       Number of years by declarant (integer value)
```
#### Ejemplo

Uso para generar declaraciones ficticias de 5 declarantes en un periodo de 5 años consecutivos.
```
$ python main.py -s 1 -n 5 -y 5

```

### Sistema 2 .-Servidores públicos que intervienen en contrataciones

Argumentos
```
usage: main.py [-s {1,2,3}] [-n SAMPLES] [-y YEARS]

optional arguments:
  -s {1,2,3}, --sys {1,2,3}         System number
  -n SAMPLES, --samples SAMPLES     Number of samples
  -y YEARS, --years YEARS       Number of years by declarant (integer value)
```
#### Ejemplo

Uso para generar documentos ficticios de 5 servidores públicos que intervienen en contrataciones en un periodo de 1 año.
```
$ python main.py -s 2 -n 5 -y 1

```


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen.)


   [Faker]: <https://github.com/joke2k/faker/>
   [data_generator]: <https://github.com/PDNMX/data_generator>
   [declaraciones.json]: <https://github.com/PDNMX/data_faker/blob/master/oas/declaraciones.json>
   [declaraciones_with_faker.json]: <https://github.com/PDNMX/data_faker/blob/master/oas/declaraciones_with_faker.json>
   