# Proyecto 2: Automatización del Proceso de Paletizado mediante Robot Colaborativo Pick and Place

## 📋 Resumen del Proyecto
Automatizar la tarea de clasificación y paletizado utilizando un robot colaborativo, una cinta transportadora y sensores de proximidad, aumentando la eficiencia y reduciendo la dependencia de mano de obra.

---

## 🎯 Objetivo General
Implementar un sistema completamente automatizado que permita:
- **Automatizar el proceso de paletizado** con un robot colaborativo Niryo Ned2
- **Clasificar objetos** por tamaño (pequeños y grandes) usando sensores infrarrojos
- **Optimizar la eficiencia** del proceso industrial
- **Reducir costos** operacionales y lesiones laborales
- **Habilitar control remoto** con interfaz gráfica
- **Registrar y analizar datos** del proceso para propuestas de mejora

---

## 🔧 Descripción del Proceso Automatizado

### Flujo General:
1. **Colocación**: El robot coloca objeto(s) en la cinta transportadora
2. **Transporte**: La cinta transportadora traslada los objetos hasta ser detectados por sensores infrarrojos
3. **Clasificación**: Se detecta el tipo de objeto (pequeño/grande) con los sensores
4. **Posicionamiento**: El robot posiciona cada objeto en la zona de trabajo usando offsets respecto a una pose central
5. **Finalización**: El proceso termina cuando 6 objetos se han paletizado

### Estrategia de Posicionamiento:
- Se define una **única pose central** en la zona de trabajo
- Los objetos se posicionan en **marcas específicas** usando **offsets** respecto a la pose central
- Objetos pequeños: 3 posiciones (izquierda a derecha, fila superior)
- Objetos grandes: 3 posiciones (izquierda a derecha, fila inferior)

---

## 📊 Estado del Proyecto

### ✅ Completado

#### Backend (Scripts Robot):
- [x] Scripts básicos de funcionamiento en NiryoStudio (`SCRIPT NIRYOSTUDIO 1.0.py`)
- [x] Script para robot real (`SCRIPT NIRYO REAL 1.0.py`)
- [x] Lógica de detección de sensores (pequeño/grande)
- [x] Movimientos básicos del robot y control de cinta transportadora
- [x] Estructura general del Pick and Place

#### Frontend (Interfaz Web):
- [x] **Interfaz gráfica HTML/CSS** (`web/index.html`, `web/estilos.css`)
  - Tema retro (Windows 95/98)
  - Sección de control automático (START/STOP)
  - Sección de control manual (HOME/MOVE)
  - Visualización de estado
  - Contador de piezas paletizadas
  - Visualización de posición actual (X, Y, Z, ROLL, PITCH, YAW)
  - Inputs para control manual de movimiento
  - Actualización automática cada 1 segundo

#### Backend (Servidor):
- [x] **Servidor Flask** (`SERVIDOR.py`)
  - Corre en `127.0.0.1:5000`
  - Endpoint POST `/run_main` - Inicia el proceso automático
  - Endpoint POST `/run_stop` - Detiene el proceso
  - Endpoint `/` - Comprobación de funcionamiento

### 🚧 En Progreso

#### Backend (Servidor - Endpoints faltantes):
- [ ] Endpoint POST `/home` - Mover robot a posición de inicio
- [ ] Endpoint POST `/move` - Mover robot a coordenadas específicas (recibe JSON con X, Y, Z, ROLL, PITCH, YAW)
- [ ] Endpoint GET `/posicion` - Retorna posición actual del robot
- [ ] Endpoint GET `/paletizadas` - Retorna contador de piezas paletizadas

#### General:
- [ ] **Calibración de offsets**: Validación y ajuste fino de las posiciones de los 6 espacios de paletizado
- [ ] **Módulo `prova.py`**: Crear el módulo que contiene las funciones `main()` y `stop()`
- [ ] **Corrección HTML**: IDs de inputs para coordenadas (actualmente busca `inputX`, `inputY`, etc. pero los inputs tienen clase `mov_posiciones`)
- [ ] **Base de datos**: Implementación de registro de datos y análisis

### ❌ No Iniciado
- [ ] Conexión CORS en servidor Flask para evitar problemas de origen cruzado
- [ ] Persistencia de datos (base de datos para lectura/escritura de variables)
- [ ] Modo "Prueba de funcionamiento"
- [ ] Monitorización en tiempo real de variables adicionales
- [ ] Sistema de logs y reportes de mejora
- [ ] Tratamiento de errores en endpoints

---

## 🛠️ Herramientas y Componentes

| Componente | Descripción |
|---|---|
| **Robot** | Niryo Ned2 (robot colaborativo) |
| **Cinta Transportadora** | Para trasladar objetos clasificados |
| **Sensores** | 2 sensores de proximidad infrarrojos (DI1, DI5) |
| **Objetos** | Piezas pequeñas y grandes para paletizar |
| **Biblioteca Python** | `pyniryo` para control del robot |
| **Framework Backend** | Flask (Python) |
| **Frontend** | HTML5, CSS3, JavaScript vanilla |

---

## 📁 Estructura del Proyecto

```
Proyecto2/
├── SCRIPT NIRYO REAL 1.0.py                      # Script principal para robot real
├── SCRIPT NIRYOSTUDIO 1.0.py                     # Script de pruebas en simulador
├── SCRIPT NIRYO REAL PEQUE;AS Y GRANDES.py       # Script alternativo con clasificación
├── SERVIDOR.py                                    # Servidor Flask (en desarrollo)
├── README.md                                      # Este archivo
└── web/                                           # Interfaz gráfica web
    ├── index.html                                 # HTML principal
    ├── estilos.css                                # Estilos CSS (tema retro)
    ├── bob1.jpg                                   # Fondo de página
    ├── bob2.png                                   # Imagen auxiliar
    ├── dsic.png                                   # Logo DSIC
    └── geeked-patric.jpg                          # Imagen auxiliar
```

---

## 🔌 Configuración de Hardware

### Sensores de Proximidad:
- **PIN_SENSOR_PIEZA_PEQUEÑA**: DI5
- **PIN_SENSOR_PIEZA_GRANDE**: DI1
- **Detección**: 
  - Pieza pequeña: Solo DI5 detecta (LOW)
  - Pieza grande: Ambos detectan (DI1 y DI5 en LOW)

### Poses Principales (Robot Real):
- **POS_INICIAL**: Posición de inicio/reposo
- **POS_COJER_PIEZA**: Coger pieza de la bandeja
- **POS_DEJAR_CONVEYOR**: Dejar pieza en cinta transportadora
- **POS_RECOGER**: Recoger pieza de cinta
- **POS_CENTRO**: Pose central de paletizado
- **offsets_pequeñas**: 3 offsets para objetos pequeños
- **offsets_grandes**: 3 offsets para objetos grandes

### Servidor Flask:
- **Host**: `127.0.0.1`
- **Puerto**: `5000`
- **Protocolo**: HTTP

---

## 🚀 Próximos Pasos

### Fase 2: Completar Servidor Flask
1. [ ] Crear módulo `prova.py` con funciones `main()` y `stop()`
2. [ ] Implementar endpoints faltantes (`/home`, `/move`, `/posicion`, `/paletizadas`)
3. [ ] Configurar CORS para conexiones desde navegador
4. [ ] Corregir IDs en HTML para inputs de coordenadas
5. [ ] Conectar servidor con scripts del robot

### Fase 3: Calibración y Validación
6. [ ] Calibrar y validar todos los offsets de posicionamiento
7. [ ] Pruebas de funcionamiento con objetos reales
8. [ ] Documentar tiempos de ciclo y eficiencia

### Fase 4: Base de Datos y Analytics
9. [ ] Configurar base de datos (SQLite/PostgreSQL)
10. [ ] Registrar timestamps y eventos del proceso
11. [ ] Crear dashboard de análisis de datos

### Fase 5: Funcionalidades Avanzadas
12. [ ] Modo prueba para testear cada elemento
13. [ ] Monitorización visual de variables adicionales
14. [ ] Elementos sonoros y animaciones
15. [ ] Reportes automáticos de mejora
16. [ ] Tratamiento robusto de errores

---

## 📝 Notas Técnicas

### Variables Globales (SCRIPT NIRYO REAL 1.0.py):
- `contador_piezas_pequenyas`: Cuenta de piezas pequeñas paletizadas
- `contador_piezas_grandes`: Cuenta de piezas grandes paletizadas
- `es_grande`: Booleano para identificar tipo de pieza detectada

### IP del Robot:
- Robot Real: `172.16.190.28`
- Simulador (NiryoStudio): `127.0.0.1`

### Endpoints del Servidor Flask:

| Método | Endpoint | Estado | Descripción |
|--------|----------|--------|-------------|
| GET | `/` | ✅ Implementado | Comprobación de funcionamiento |
| POST | `/run_main` | ✅ Implementado | Inicia el proceso automático |
| POST | `/run_stop` | ✅ Implementado | Detiene el proceso |
| POST | `/home` | ❌ Pendiente | Mover robot a posición de inicio |
| POST | `/move` | ❌ Pendiente | Mover robot a coordenadas (JSON) |
| GET | `/posicion` | ❌ Pendiente | Retorna posición actual |
| GET | `/paletizadas` | ❌ Pendiente | Retorna contador de piezas |

---

## 👥 Equipo y Responsabilidades

- **Desarrollo**: Jordi Martinez, Teo Verdu, Samuel Climent
- **Robot Niryo**: Jordi Martinez
- **Servidor Flask**: Samuel Climent
- **Base de Datos**: Teo Verdu
- **Interfaz web**: Jordi Martinez, Samuel Climent, Teo Verdu

---

## 📚 Referencias y Documentación

- Pyniryo Documentation: [Official Docs](https://docs.niryo.com/)
- Niryo Ned2: [Robot Specifications](https://niryo.com/ned2/)
- Flask Documentation: [Official Docs](https://flask.palletsprojects.com/)

---

**Última actualización**: Mayo 2026
