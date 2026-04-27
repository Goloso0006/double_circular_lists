# Clock App - Reloj Analogico con Lista Doblemente Enlazada Circular

## Descripcion
Este proyecto simula un reloj analogico en Python usando una lista doblemente enlazada circular para modelar el comportamiento ciclico de:

- Horas (0-23)
- Minutos (0-59)
- Segundos (0-59)

La app tiene una interfaz en Streamlit con personalizacion visual del reloj (fondo, esfera y controles), separada por capas para mantener el codigo ordenado.

---

## Estructura Del Proyecto

### application/
Contiene la logica de aplicacion.

- `clock_engine.py`: motor principal del reloj. Sincroniza hora, avanza (`tick`), retrocede y entrega el tiempo actual.
- `__init__.py`: inicializacion del paquete.

### domain/
Contiene el nucleo del dominio (sin dependencia de UI).

- `entities/time_node.py`: nodo de la lista enlazada (valor, next, prev).
- `entities/clock_hand.py`: representa cada aguja y su posicion actual sobre la lista circular.
- `structures/circular_doubly_linked_list.py`: estructura circular doblemente enlazada y operaciones de navegacion.
- `value_objects/clock_time.py`: objeto de valor para hora, minuto y segundo, con formatos de salida.
- `__init__.py`: inicializacion del paquete.

### services/
Servicios externos al dominio.

- `time_service.py`: obtiene la hora real del sistema y la adapta al modelo interno.
- `__init__.py`: inicializacion del paquete.

### presentation/
Capa visual (interfaz de usuario).

- `clock_ui.py`: UI principal en Streamlit. Renderiza controles, entrada manual de hora y el reloj analogico personalizado.
- `streamlit_app.py`: punto de entrada para lanzar la interfaz.
- `__init__.py`: inicializacion del paquete.

### Archivos En La Raiz

- `run_clock_app.bat`: script rapido para ejecutar la app en Windows.
- `README.md`: documentacion del proyecto.
- `.gitignore`: archivos ignorados por Git.

---

## Como Funciona El Reloj

1. Se crean tres listas circulares para horas, minutos y segundos.
2. Cada aguja (`ClockHand`) apunta a un nodo actual.
3. Al ejecutar `tick()`:
- La aguja de segundos avanza una posicion.
- Si pasa de 59 a 00, avanza minutos.
- Si minutos pasa de 59 a 00, avanza horas.

Esto evita condicionales complejos de reinicio porque la estructura circular ya representa el ciclo natural del tiempo.

---

## Ejecucion

### Opcion 1 (recomendada en Windows)
```bash
./run_clock_app.bat
```

### Opcion 2 (manual)
1. Instalar dependencias:
```bash
pip install streamlit matplotlib
```

2. Ejecutar Streamlit:
```bash
streamlit run presentation/streamlit_app.py
```

---

## Cambios Visuales Implementados

- Interfaz en Streamlit con fondo de imagen y capa oscura para mejorar legibilidad.
- Reloj analogico estilizado (esfera, indices, subesferas y agujas).
- Control de ejecucion con boton de estado (iniciar/pausar/reanudar).
- Entrada manual de hora para sincronizar rapidamente.