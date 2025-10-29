"""
ALGORITMOS DE BÚSQUEDA BFS Y DFS
================================

Este módulo contiene las implementaciones detalladas y comentadas de los 
algoritmos de Búsqueda en Amplitud (BFS) y Búsqueda en Profundidad (DFS)
utilizados para el diagnóstico de otitis.

Autor: Mesías Orlando Mariscal Oña
Materia: Inteligencia Artificial
Universidad de las Fuerzas Armadas ESPE
"""

from collections import deque
from typing import Dict, List, Set, Tuple, Optional


class AlgoritmosBusqueda:
    """
    Clase que implementa algoritmos de búsqueda en grafos para diagnóstico médico.
    
    Attributes:
        grafo: Diccionario que representa el grafo de síntomas
        objetivo: Nodo objetivo a encontrar (enfermedad a diagnosticar)
    """
    
    def __init__(self, grafo: Dict[str, List[str]], objetivo: str = "OTITIS"):
        """
        Inicializa el motor de búsqueda.
        
        Args:
            grafo: Grafo dirigido representando relaciones síntoma-enfermedad
            objetivo: Nodo objetivo a diagnosticar (default: "OTITIS")
        """
        self.grafo = grafo
        self.objetivo = objetivo
    
    # ========================================================================
    # BÚSQUEDA EN AMPLITUD (BFS - Breadth-First Search)
    # ========================================================================
    
    def busqueda_amplitud(self, nodo_inicial: str) -> Dict:
        """
        Implementa el algoritmo de Búsqueda en Amplitud (BFS).
        
        BFS explora el grafo nivel por nivel, garantizando encontrar el camino
        más corto en grafos no ponderados.
        
        Características:
        - Usa una COLA (FIFO: First In, First Out)
        - Explora todos los vecinos de un nivel antes de pasar al siguiente
        - Garantiza encontrar el camino MÁS CORTO
        - Mayor uso de memoria (almacena todos los nodos de un nivel)
        
        Args:
            nodo_inicial: Síntoma inicial del paciente
            
        Returns:
            Dict con:
                - encontrado (bool): Si se encontró el objetivo
                - pasos (List[Dict]): Lista de pasos del proceso
                - camino_final (List[str]): Camino desde inicio hasta objetivo
                - nodos_visitados (int): Total de nodos explorados
        """
        
        # ====================================================================
        # INICIALIZACIÓN DE ESTRUCTURAS DE DATOS
        # ====================================================================
        
        # Cola FIFO: almacena tuplas (nodo_actual, camino_hasta_nodo)
        # Usamos deque de collections para operaciones O(1) en ambos extremos
        cola = deque()
        cola.append((nodo_inicial, [nodo_inicial]))
        
        # Set de nodos visitados: evita ciclos y revisitas
        # Búsqueda en set es O(1), más eficiente que lista
        visitados = set()
        visitados.add(nodo_inicial)
        
        # Lista que almacena cada paso del algoritmo para visualización
        pasos = []
        
        # Contador de pasos para tracking
        numero_paso = 0
        
        # ====================================================================
        # BUCLE PRINCIPAL DE BFS
        # ====================================================================
        
        while cola:  # Mientras haya nodos por explorar
            
            numero_paso += 1
            
            # Extraer el PRIMERO de la cola (FIFO)
            # En BFS siempre procesamos el nodo más "antiguo" en la cola
            nodo_actual, camino_actual = cola.popleft()
            
            # Guardar estado actual para visualización
            pasos.append({
                'paso': numero_paso,
                'nodo_actual': nodo_actual,
                'camino': camino_actual.copy(),
                'visitados': visitados.copy(),
                'cola': list(cola),  # Snapshot de la cola actual
                'accion': f'Explorando: {nodo_actual}'
            })
            
            # ================================================================
            # VERIFICACIÓN DE OBJETIVO
            # ================================================================
            
            # ¿Hemos llegado al nodo objetivo (OTITIS)?
            if nodo_actual == self.objetivo:
                return {
                    'encontrado': True,
                    'pasos': pasos,
                    'camino_final': camino_actual,
                    'nodos_visitados': len(visitados),
                    'longitud_camino': len(camino_actual),
                    'algoritmo': 'BFS'
                }
            
            # ================================================================
            # EXPANSIÓN DE VECINOS
            # ================================================================
            
            # Obtener vecinos del nodo actual
            vecinos = self.grafo.get(nodo_actual, [])
            
            # Explorar cada vecino
            for vecino in vecinos:
                
                # Solo procesar si NO ha sido visitado
                # Esto evita ciclos infinitos y re-procesamiento
                if vecino not in visitados:
                    
                    # Marcar como visitado INMEDIATAMENTE al agregarlo a la cola
                    # Esto evita que otros caminos lo agreguen de nuevo
                    visitados.add(vecino)
                    
                    # Crear nuevo camino: camino actual + nuevo vecino
                    nuevo_camino = camino_actual + [vecino]
                    
                    # Agregar al FINAL de la cola (FIFO)
                    # Este nodo será procesado después de todos los del nivel actual
                    cola.append((vecino, nuevo_camino))
        
        # ====================================================================
        # NO SE ENCONTRÓ EL OBJETIVO
        # ====================================================================
        
        # Si salimos del bucle sin encontrar el objetivo
        return {
            'encontrado': False,
            'pasos': pasos,
            'camino_final': [],
            'nodos_visitados': len(visitados),
            'longitud_camino': 0,
            'algoritmo': 'BFS'
        }
    
    # ========================================================================
    # BÚSQUEDA EN PROFUNDIDAD (DFS - Depth-First Search)
    # ========================================================================
    
    def busqueda_profundidad(self, nodo_inicial: str) -> Dict:
        """
        Implementa el algoritmo de Búsqueda en Profundidad (DFS).
        
        DFS explora cada rama del grafo hasta el final antes de retroceder.
        
        Características:
        - Usa una PILA (LIFO: Last In, First Out)
        - Explora profundamente cada rama antes de retroceder
        - NO garantiza el camino más corto
        - Menor uso de memoria (solo almacena el camino actual)
        
        Args:
            nodo_inicial: Síntoma inicial del paciente
            
        Returns:
            Dict con:
                - encontrado (bool): Si se encontró el objetivo
                - pasos (List[Dict]): Lista de pasos del proceso
                - camino_final (List[str]): Camino desde inicio hasta objetivo
                - nodos_visitados (int): Total de nodos explorados
        """
        
        # ====================================================================
        # INICIALIZACIÓN DE ESTRUCTURAS DE DATOS
        # ====================================================================
        
        # Pila LIFO: almacena tuplas (nodo_actual, camino_hasta_nodo)
        # En Python, usamos lista común: append() y pop() son LIFO
        pila = []
        pila.append((nodo_inicial, [nodo_inicial]))
        
        # Set de nodos visitados: evita ciclos
        visitados = set()
        visitados.add(nodo_inicial)
        
        # Lista de pasos para visualización
        pasos = []
        
        # Contador de pasos
        numero_paso = 0
        
        # ====================================================================
        # BUCLE PRINCIPAL DE DFS
        # ====================================================================
        
        while pila:  # Mientras haya nodos por explorar
            
            numero_paso += 1
            
            # Extraer el ÚLTIMO de la pila (LIFO)
            # En DFS siempre procesamos el nodo más "reciente"
            nodo_actual, camino_actual = pila.pop()
            
            # Guardar estado actual para visualización
            pasos.append({
                'paso': numero_paso,
                'nodo_actual': nodo_actual,
                'camino': camino_actual.copy(),
                'visitados': visitados.copy(),
                'pila': list(pila),  # Snapshot de la pila actual
                'accion': f'Explorando: {nodo_actual}'
            })
            
            # ================================================================
            # VERIFICACIÓN DE OBJETIVO
            # ================================================================
            
            # ¿Hemos llegado al nodo objetivo (OTITIS)?
            if nodo_actual == self.objetivo:
                return {
                    'encontrado': True,
                    'pasos': pasos,
                    'camino_final': camino_actual,
                    'nodos_visitados': len(visitados),
                    'longitud_camino': len(camino_actual),
                    'algoritmo': 'DFS'
                }
            
            # ================================================================
            # EXPANSIÓN DE VECINOS
            # ================================================================
            
            # Obtener vecinos del nodo actual
            vecinos = self.grafo.get(nodo_actual, [])
            
            # IMPORTANTE: Invertir el orden de vecinos para DFS
            # Esto asegura que el primer vecino en la lista se explore primero
            # (ya que la pila es LIFO)
            for vecino in reversed(vecinos):
                
                # Solo procesar si NO ha sido visitado
                if vecino not in visitados:
                    
                    # Marcar como visitado
                    visitados.add(vecino)
                    
                    # Crear nuevo camino
                    nuevo_camino = camino_actual + [vecino]
                    
                    # Agregar al TOPE de la pila (LIFO)
                    # Este nodo será procesado en la PRÓXIMA iteración
                    pila.append((vecino, nuevo_camino))
        
        # ====================================================================
        # NO SE ENCONTRÓ EL OBJETIVO
        # ====================================================================
        
        return {
            'encontrado': False,
            'pasos': pasos,
            'camino_final': [],
            'nodos_visitados': len(visitados),
            'longitud_camino': 0,
            'algoritmo': 'DFS'
        }


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

def ejemplo_uso():
    """
    Ejemplo de cómo utilizar los algoritmos de búsqueda.
    """
    
    # Definir el grafo de síntomas de otitis
    grafo_otitis = {
        'dolor_oido': ['OTITIS'],
        'dolor_punzante': ['OTITIS'],
        'escalofrios': ['fiebre', 'fiebre_alta'],
        'fiebre': ['OTITIS'],
        'fiebre_alta': ['OTITIS'],
        'presion_oido': ['OTITIS'],
        'perdida_audicion': ['OTITIS'],
        'secrecion': ['OTITIS'],
        'oido_tapado': ['OTITIS'],
        'zumbido': ['OTITIS'],
        'OTITIS': []  # Nodo objetivo sin salidas
    }
    
    # Crear instancia del motor de búsqueda
    motor = AlgoritmosBusqueda(grafo_otitis, objetivo="OTITIS")
    
    # Síntoma inicial del paciente
    sintoma_inicial = "escalofrios"
    
    print("="*70)
    print("BÚSQUEDA EN AMPLITUD (BFS)")
    print("="*70)
    
    # Ejecutar BFS
    resultado_bfs = motor.busqueda_amplitud(sintoma_inicial)
    
    print(f"\nObjetivo encontrado: {resultado_bfs['encontrado']}")
    print(f"Camino: {' → '.join(resultado_bfs['camino_final'])}")
    print(f"Longitud del camino: {resultado_bfs['longitud_camino']}")
    print(f"Nodos visitados: {resultado_bfs['nodos_visitados']}")
    print(f"Total de pasos: {len(resultado_bfs['pasos'])}")
    
    print("\n" + "="*70)
    print("BÚSQUEDA EN PROFUNDIDAD (DFS)")
    print("="*70)
    
    # Ejecutar DFS
    resultado_dfs = motor.busqueda_profundidad(sintoma_inicial)
    
    print(f"\nObjetivo encontrado: {resultado_dfs['encontrado']}")
    print(f"Camino: {' → '.join(resultado_dfs['camino_final'])}")
    print(f"Longitud del camino: {resultado_dfs['longitud_camino']}")
    print(f"Nodos visitados: {resultado_dfs['nodos_visitados']}")
    print(f"Total de pasos: {len(resultado_dfs['pasos'])}")
    
    print("\n" + "="*70)
    print("COMPARACIÓN")
    print("="*70)
    print(f"\nBFS - Longitud: {resultado_bfs['longitud_camino']} | "
          f"Pasos: {len(resultado_bfs['pasos'])}")
    print(f"DFS - Longitud: {resultado_dfs['longitud_camino']} | "
          f"Pasos: {len(resultado_dfs['pasos'])}")
    
    if resultado_bfs['longitud_camino'] <= resultado_dfs['longitud_camino']:
        print("\n✅ BFS encontró un camino más corto o igual")
    else:
        print("\n⚠️ DFS encontró un camino más corto (poco común)")


# ============================================================================
# ANÁLISIS DE COMPLEJIDAD
# ============================================================================

"""
COMPLEJIDAD COMPUTACIONAL:

BFS (Búsqueda en Amplitud):
- Tiempo: O(V + E) donde V = vértices, E = aristas
  - Cada nodo se visita una vez: O(V)
  - Cada arista se examina una vez: O(E)
  
- Espacio: O(V)
  - Cola puede contener todos los nodos de un nivel
  - En el peor caso: O(V)

DFS (Búsqueda en Profundidad):
- Tiempo: O(V + E)
  - Misma complejidad temporal que BFS
  - Cada nodo se visita una vez, cada arista se examina una vez
  
- Espacio: O(V)
  - Pila contiene el camino actual
  - En el peor caso (línea recta): O(V)
  - En promedio (árbol balanceado): O(log V)

COMPARACIÓN PARA GRAFO DE OTITIS:
- V = 11 nodos (10 síntomas + 1 enfermedad)
- E ≈ 12 aristas
- Ambos algoritmos: O(11 + 12) = O(23) ≈ O(1) (constante para este caso)

CONCLUSIÓN:
Para grafos pequeños como el de otitis, la diferencia de rendimiento es 
despreciable. La elección depende de otros factores:
- BFS: Si necesitas el camino MÁS CORTO
- DFS: Si necesitas usar MENOS MEMORIA
"""


# ============================================================================
# PROPIEDADES DE LOS ALGORITMOS
# ============================================================================

"""
PROPIEDADES CLAVE:

BFS:
✅ Completo: Siempre encuentra solución si existe
✅ Óptimo: Encuentra el camino más corto (grafos no ponderados)
✅ Sistemático: Explora ordenadamente por niveles
❌ Memoria: Requiere más memoria

DFS:
✅ Completo: En grafos finitos con detección de ciclos
❌ Óptimo: NO garantiza el camino más corto
✅ Memoria: Usa menos memoria
❌ Puede quedar atrapado en ramas profundas

PARA DIAGNÓSTICO MÉDICO:
- BFS es PREFERIBLE porque:
  1. El camino más corto = razonamiento más directo
  2. Más fácil de explicar al paciente
  3. Menos inferencias = menos probabilidad de error
  4. Exploración sistemática = más confiable
"""


if __name__ == "__main__":
    # Ejecutar ejemplo
    ejemplo_uso()
