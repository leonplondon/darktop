# Process Manager

## Dependencias

No se requiere de la instalación de dependencias externas

## Requerimientos

Para ejecutar de manera satisfactoria el proyecto, se debe contar con:

- Python instalado en su versión 3.8 o superior
- Sistema operativo Linux, preferiblemente Ubuntu/Kubuntu 18.04 o superior

## Instalación / Ejecución

Para ejecutar la aplicación en un sistema que cumpla con los requerimientos exigidos y estando en el directorio de código fuente, se deben seguir las siguientes instrucciones

### Ejecución como usuario normal

Cuando se va a realizar la ejecución sin permisos especiales, es decir, no se podrán crear procesos en nombre de otros usuarios del sistema

```shell
python3.8 main.py
```

### Ejecución como super-usuario

Si se desean ejecutar procesos, en nombre de otro usuario, se debe contar con un usuario del listado sudoers y ejecutar la aplicación con

```shell
sudo python3.8 main.py
```

## Proceso padre e hijo

En el archivo `dummy.py` se encuentra la lógica que permite ejecutar un proceso de Python que además del proceso principal, genera y se conecta con un proceso hijo. Se aclara que estos procesos no ejecutan una lógica determinada, son solamente `loops` infinitos. Para ejecutar estos procesos de manera adecuada, hay que enviar el UID del usuario que actuará como propietario de los procesos

```shell
CUSTOM_UID=<####> python3.8 dummy.py
```

### Donde

- *CUSTOM_UID* es una variable de entorno
- *`<####>`* debe ser reemplazado por el UID de un usuario del sistema 
