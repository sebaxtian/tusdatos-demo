# Tusdatos: Prueba técnica Desarrollador Backend Python

Se requiere extraer información de la página web "[Consulta de Procesos Judiciales](https://procesosjudiciales.funcionjudicial.gob.ec/busqueda-filtros)" utilizando técnicas de Web Scraping. La información se debe limpiar y guardar de manera estructurada.

## Punto 1:
Especificación:

Lenguaje de programación: Python.

La página permite realizar búsquedas para Personas Naturales o Personas Jurídicas, utilizando criterios como Actor/Ofendido o Demandado/Procesado. Además, es preciso proporcionar documentos de identidad para Personas Naturales y RUC para Personas Jurídicas. Se adjunta una lista de datos de prueba para facilitar el proceso de extracción de información.

| **Actor/Ofendido** | **Demandado/Procesado** |
|----------------|---------------------|
| 0968599020001  | 1791251237001       |
| 0992339411001  | 0968599020001       |

Teniendo en cuenta los datos de la tabla el scraping debe tener las siguientes características:

* Extraer listado de procesos que genera la búsqueda.
* Distinguir entre los procesos de demandado y demandante. 
* Extraer el detalle para cada proceso.
* Extraer todas las actuaciones judiciales de cada proceso.
* Guardar toda la información de los procesos en base de datos o un archivo (csv, json, etc).
* Crear y documentar un caso de prueba dentro del cual se ejecuten 15 consultas paralelas revisando que no haya un bloqueo por parte de la página de consulta.
* Implementación de tests

Nota: Considerando la potencial cantidad de procesos y subprocesos involucrados, es fundamental identificar el método más eficiente para la extracción de datos.

## Punto 2:
Especificación:

Usar Librerias/Frameworks como Flask o FastApi

Crear un API REST para exponer los datos extraídos en la página de [Consulta de Procesos Judiciales](https://procesosjudiciales.funcionjudicial.gob.ec/busqueda-filtros)

El servicio debe tener las siguientes características:
* Endpoints que puedan exponer la data
* Usar un sistema de autorización y autenticación (el de preferencia)
* Implementación de tests
* Contener una documentación del uso del API.

Opcional: Desarrollar una vista que permita ejecutar la petición a la fuente y una vez terminada ver de forma estructurada la información de los procesos.

Entrega
Compartir repositorio en GitHub.


## Requerimientos

* Linux: Ubuntu 22.04.3 LTS
* Python 3.10+
* Poetry 1.7+
    * [Install Poetry](https://python-poetry.org/docs/#installation)
* Chrome Browser for Testing
    * [Stable](https://googlechromelabs.github.io/chrome-for-testing/#stable)
* Chrome Driver for Testing
    * [Stable](https://googlechromelabs.github.io/chrome-for-testing/#stable)

## ¿Cómo usar?

Lea y ejecute cada paso a continuación:

### Paso 1

Instalar poetry usando el script:

```bash
./install-poetry.sh
```

Agregar poetry al PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Tambien puede agregar poetry al final del archivo .bashrc:

```bash
nano ~/.bashrc
```

### Paso 2

Comando para decirle a poetry qué versión de Python usar para el proyecto actual:

```bash
poetry env use 3.12
```

### Paso 3

Activando el entorno virtual:

```bash
poetry shell
```

### Paso 4

Instalando dependencias:

```bash
poetry install --no-root
```

### Paso 5

Descargue la aplicación Chrome y el driver para pruebas y copie cada uno en la carpeta específica:

* Chrome App: **.webbrowser/app**
* Chrome Driver: **.webbrowser/driver**

### Opcional

Visualización de la información del entorno:

```bash
poetry env info
```

Agrega los paquetes necesarios a su pyproject.toml y los instala:

```bash
poetry add selenium
```

Desactivar el entorno virtual y salir:

```bash
exit
# Para desactivar el entorno virtual sin salir del shell utilice desactivar
deactivate
```

## Ejecutar Proceso

Desde el la raiz del proyecto ejecutar el archivo main de python:

```bash
python main.py
```

---

***Eso es todo por ahora ...***

---

#### Licencia

[MIT License](./LICENSE)

[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1)

#### Acerca de mí

[https://about.me/sebaxtian](https://about.me/sebaxtian)
