# Sistema de Diagnóstico de Otitis - BFS y DFS

## 🎯 Descripción
Agente inteligente que diagnostica otitis usando algoritmos de búsqueda en grafos.
Muestra el proceso **paso a paso** de cómo BFS y DFS recorren el grafo.

## 🚀 Ejecutar
```bash
python app.py
```

## 📋 Archivos
- `app.py` - Aplicación principal con interfaz gráfica
- `agente_otitis.py` - Lógica del agente (BFS y DFS con pasos detallados)
- `requirements.txt` - Dependencias

## 🔍 Cómo usar
1. Selecciona síntomas del paciente (checkboxes)
2. Haz clic en "BFS" o "DFS" para diagnosticar
3. Usa los botones **◀ Anterior / Siguiente ▶** para ver el proceso paso a paso
4. Observa cómo el algoritmo explora el grafo en cada paso

## 📊 Diferencias BFS vs DFS

### BFS (Búsqueda en Amplitud)
- Usa una **COLA** (FIFO - primero en entrar, primero en salir)
- Explora **nivel por nivel**
- Garantiza encontrar el **camino más corto**
- Más exhaustivo

### DFS (Búsqueda en Profundidad)
- Usa una **PILA** (LIFO - último en entrar, primero en salir)
- Explora **profundidad primero**
- Puede encontrar caminos más largos
- Más rápido en algunos casos

## 🎨 Visualización
La aplicación muestra:
- **Naranja**: Nodo siendo explorado ahora
- **Verde**: Nodos en el camino actual
- **Gris**: Nodos ya visitados
- **Gris claro**: Nodos no visitados
- **Rojo**: OTITIS (objetivo)

## ⚠️ Nota
Sistema educativo. NO usar para diagnósticos reales.
