# Proyecto 1
App para manejar stock de una ONG. Desarrolllado en Django.

# Enviroment Set Up

## 1) Instalar pipenv (opcional)

Esta seccion es opcional. En caso de no querer realizarla, pasar directamente al paso 2.

```
pip install pipenv
```

Pipenv nos permite instalar dependencias en entornos virtuales. Esto evita que se nos haga un lío con dependencias compartidas entre aplicaciones.

### 1.1) Instalar django en un entorno virtual y correr entorno virtual

```
pipenv install django
```

Esto crea un nuevo directorio con los archivos del entorno. Lo podemos ver escribiendo el comando:

```
pipenv --venv
```

Luego, para ejecutar el entorno virtual corremos el siguiente comando:

```
source [directorio obtenido en comando anterior]/bin/activate
```

## 2) Crear proyecto de django

Para crear un nuevo proyecto, ejecutamos:

```
django-admin startproject [nombre]
```

## 3) Crear apps y correr server

Para crear apps se usa:

```
python manage.py startapp [nombre]
```

Para correr el server se ejecuta:

```
python manage.py runserver [puerto]
```

El parametro *puerto* es opcional. Si no se completa, se utiliza el puerto 8000
