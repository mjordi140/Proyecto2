# Proyecto 2: Automatización del Proceso de Paletizado mediante Robot Colaborativo Pick and Place

## 📋 Resumen del Proyecto
Automatizar la tarea de clasificación y paletizado utilizando un robot colaborativo, una cinta transportadora y sensores de proximidad, aumentando la eficiencia y reduciendo la dependencia de mano de obra humana.

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
- [x] Scripts básicos de funcionamiento en NiryoStudio (`SCRIPT NIRYOSTUDIO 1.0.py`)
- [x] Script para robot real (`SCRIPT NIRYO REAL 1.0.py`)
- [x] Lógica de detección de sensores (pequeño/grande)
- [x] Movimientos básicos del robot y control de cinta transportadora
- [x] Estructura general del Pick and Place

### 🚧 En Progreso
- [ ] **Calibración de offsets**: Validación y ajuste fino de las posiciones de los 6 espacios de paletizado
- [ ] **Sistema de control remoto**: Interfaz gráfica para gestionar marcha/paro
- [ ] **Base de datos**: Implementación de registro de datos y análisis
- [ ] **Funcionalidades avanzadas**: Modo prueba, monitorización, visualización

### ❌ No Iniciado
- [ ] Interfaz gráfica (GUI) - Control remoto del cliente
- [ ] Base de datos para lectura/escritura de variables
- [ ] Modo "Prueba de funcionamiento"
- [ ] Monitorización en tiempo real de variables
- [ ] Elementos visuales, sonoros y animaciones
- [ ] Sistema de logs y reportes de mejora

---

## 🛠️ Herramientas y Componentes

| Componente | Descripción |
|---|---|
| **Robot** | Niryo Ned2 (robot colaborativo) |
| **Cinta Transportadora** | Para trasladar objetos clasificados |
| **Sensores** | 2 sensores de proximidad infrarrojos (DI1, DI5) |
| **Objetos** | Piezas pequeñas y grandes para paletizar |
| **Biblioteca Python** | `pyniryo` para control del robot |

---

## 📁 Estructura del Proyecto

```
Proyecto2/
├── SCRIPT NIRYO REAL 1.0.py          # Script principal para robot real
├── SCRIPT NIRYOSTUDIO 1.0.py         # Script de pruebas en simulador
├── README.md                         # Este archivo
└── [Pendiente: interfaz gráfica]
└── [Pendiente: base de datos]
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

---

## 🚀 Próximos Pasos

### Fase 2: Calibración y Validación
1. [ ] Calibrar y validar todos los offsets de posicionamiento
2. [ ] Pruebas de funcionamiento con objetos reales
3. [ ] Documentar tiempos de ciclo y eficiencia

### Fase 3: Control Remoto
4. [ ] Diseñar interfaz gráfica (botones start/stop, contador de piezas)
5. [ ] Implementar servidor de comunicación robot-cliente
6. [ ] Agregar estado de sensores en tiempo real

### Fase 4: Base de Datos y Analytics
7. [ ] Configurar base de datos (SQLite/PostgreSQL)
8. [ ] Registrar timestamps y eventos del proceso
9. [ ] Crear dashboard de análisis de datos

### Fase 5: Funcionalidades Avanzadas
10. [ ] Modo prueba para testear cada elemento
11. [ ] Monitorización visual de variables
12. [ ] Elementos sonoros y animaciones
13. [ ] Reportes automáticos de mejora

---

## 📝 Notas Técnicas

### Variables Globales (SCRIPT NIRYO REAL 1.0.py):
- `contador_piezas_pequenyas`: Cuenta de piezas pequeñas paletizadas
- `contador_piezas_grandes`: Cuenta de piezas grandes paletizadas
- `es_grande`: Booleano para identificar tipo de pieza detectada

### IP del Robot:
- Robot Real: `172.16.190.28`
- Simulador (NiryoStudio): `127.0.0.1`

---

## 👥 Equipo y Responsabilidades

- **Desarrollo**: mjordi140
- **Pruebas**: [Pendiente asignar]
- **Calibración**: [Pendiente asignar]

---

## 📚 Referencias y Documentación

- Pyniryo Documentation: [Official Docs](https://docs.niryo.com/)
- Niryo Ned2: [Robot Specifications](https://niryo.com/ned2/)

---

**Última actualización**: Mayo 2026
