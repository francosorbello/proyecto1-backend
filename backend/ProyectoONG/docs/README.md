# Documentación Backend

## Generar documentación

En la carpeta `docs` correr el comando:

```
make html
```

## Instrucciones de instalación

Esta sección explica el proceso de instalación de los paquetes y cómo se generó la documentación original. Para volver a obtenerla no es necesario realizar todos estos pasos, en cambio se debe utilizar el comando explicado en la sección anterior.

Para generar la documentación, se utilizaron 2 paquetes:

```
pip install -U Sphinx
pip install sphinx-rtd-theme
```

### 1. Generar archivos de configuración

Crear una carpeta "docs" y abrirla en consola.

```
mkdir docs
cd docs/
```

Correr el comando:

```
sphinx-quickstart
```

Este comando tiene varias opciones. En ellas se debe seleccionar:

```
Selected root path: .

Separate source and build directories (y/n) [n]: n

Name prefix for templates and static dir [_]: _

Project name: ProyectoONG
Author name(s): Franco Sorbello, Mariel Volman
Project release []: 0.1

Project language [en]: en

Source file suffix [.rst]: .rst

Name of your master document (without suffix) [index]: index

Do you want to use the epub builder (y/n) [n]: n

autodoc: automatically insert docstrings from modules (y/n) [n]: y
doctest: automatically test code snippets in doctest blocks (y/n) [n]: y
intersphinx: link between Sphinx documentation of different projects (y/n) [n]: n
todo: write “todo” entries that can be shown or hidden on build (y/n) [n]: n
coverage: checks for documentation coverage (y/n) [n]: n
imgmath: include math, rendered as PNG or SVG images (y/n) [n]: n
mathjax: include math, rendered in the browser by MathJax (y/n) [n]: n
ifconfig: conditional inclusion of content based on config values (y/n) [n]: n
viewcode: include links to the source code of documented Python objects (y/n) [n]: n
githubpages: create .nojekyll file to publish the document on GitHub pages (y/n) [n]: n

Create Makefile? (y/n) [y]: y
Create Windows command file? (y/n) [y]: y
```

Una vez hecho esto, correr el siguiente comando:

```
make html
```

### 2. Configurar sphinx para que funcione con django.

En el archivo conf.py, añadir las siguientes líneas:

```python
...

import os
import sys
import django
sys.path.insert(0, os.path.abspath('../../'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'ProyectoONG.settings'
django.setup()

...
```

Además, buscar la línea "html_theme = 'alabaster'" y cambiar por "sphinx_rtd_theme"

### 3. Añadir las apps a la documentación

Correr el siguiente comando:

```
sphinx-apidoc -o source/ ../
```

Esto añade archivos que describen qué partes del código documentar. Una vez hecho esto, correr

```
make html
```

## Sources

https://github.com/finsberg/sphinx-tutorial

http://www.marinamele.com/2014/03/document-your-django-projects.html

https://www.freecodecamp.org/news/sphinx-for-django-documentation-2454e924b3bc/

http://www.wonderousponder.com/how-to-document-django-applications-with-sphinx/
