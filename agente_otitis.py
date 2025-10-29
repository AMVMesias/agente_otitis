"""
Agente de Diagnóstico de Otitis - VERSIÓN MEJORADA CON GRAFO INTERCONECTADO
Explora TODO el grafo y muestra paso a paso el proceso
"""

from collections import deque
import time

class AgenteOtitis:
    
    def __init__(self):
        self.grafo, self.pesos = self._crear_grafo()
        
    def _crear_grafo(self):
        """
        Grafo JERÁRQUICO para diagnóstico de OTITIS - SIN NODO SANO
        
        FLUJO:
        Síntomas leves → Síntomas intermedios → Síntomas graves → OTITIS
        
        Si el algoritmo NO llega a OTITIS después de explorar = SANO (sin nodo explícito)
        
        EJEMPLO:
        - escalofrios → fiebre_alta → secrecion → OTITIS
        - dolor_oido → dolor_punzante → secrecion → OTITIS  
        - Si termina la exploración sin llegar a OTITIS = SANO
        """
        grafo = {
            # NIVEL 1: Síntomas iniciales (leves) - Pueden evolucionar
            "dolor_oido": ["presion_oido", "dolor_punzante"],
            "zumbido": ["presion_oido", "perdida_audicion"],
            
            # NIVEL 2: Síntomas intermedios
            "presion_oido": ["oido_tapado", "dolor_punzante"],
            "fiebre": ["fiebre_alta", "escalofrios"],
            "perdida_audicion": ["oido_tapado"],
            
            # NIVEL 2.5: Síntomas que pueden empeorar
            "escalofrios": ["fiebre_alta"],
            
            # NIVEL 3: Síntomas graves - Pueden llevar a OTITIS
            "oido_tapado": ["secrecion"],
            "dolor_punzante": ["secrecion", "OTITIS"],  # Dolor agudo, puede ir directo
            "fiebre_alta": ["secrecion"],
            
            # NIVEL 4: Síntoma crítico
            "secrecion": ["OTITIS"],  # Secreción del oído → OTITIS
            
            # Nodo final
            "OTITIS": []
        }
        
        # Pesos: importancia del síntoma (0.0 - 1.0)
        pesos = {
            "dolor_oido": 0.3,
            "zumbido": 0.2,
            "presion_oido": 0.4,
            "fiebre": 0.3,
            "perdida_audicion": 0.4,
            "oido_tapado": 0.5,
            "dolor_punzante": 0.7,
            "fiebre_alta": 0.6,
            "escalofrios": 0.25,
            "secrecion": 0.9,
            "OTITIS": 1.0
        }
        
        return grafo, pesos
        
    def obtener_sintomas(self):
        """Obtiene todos los síntomas disponibles (excluyendo OTITIS)"""
        sintomas = set()
        for nodo in self.grafo.keys():
            if nodo != "OTITIS":
                sintomas.add(nodo)
        return sorted(list(sintomas))
    
    def obtener_vecinos(self, nodo):
        """Obtiene los síntomas a los que se puede ir desde un nodo"""
        return self.grafo.get(nodo, [])
    
    def bfs(self, sintoma_inicial):
        """
        BFS - Búsqueda por amplitud desde UN síntoma inicial
        Explora nivel por nivel usando cola (FIFO)
        Retorna todos los pasos de la exploración
        """
        if not sintoma_inicial or sintoma_inicial not in self.grafo:
            return self._resultado_vacio()
        
        inicio = time.time()
        cola = deque([(sintoma_inicial, [sintoma_inicial])])
        visitados = {sintoma_inicial}
        pasos = []
        paso_num = 0
        camino_a_otitis = None
        
        while cola:
            # Guardar estado ANTES de desencolar (para mostrar todo incluyendo el que va a salir)
            paso_num += 1
            cola_visual = [n for n, _ in cola]
            nodo_actual, camino = cola[0]  # Ver qué está en el frente sin sacarlo
            
            pasos.append({
                'paso': paso_num,
                'nodo_actual': nodo_actual,
                'cola': cola_visual.copy(),
                'visitados': visitados.copy(),
                'camino': camino.copy(),
                'en_camino': False
            })
            
            # Ahora sí desencolar
            cola.popleft()
            
            # Si llegamos a OTITIS
            if nodo_actual == "OTITIS":
                camino_a_otitis = camino
                break
            
            # Explorar vecinos y agregarlos a la cola
            vecinos = list(self.grafo.get(nodo_actual, []))
            for vecino in vecinos:
                if vecino not in visitados:
                    visitados.add(vecino)
                    nuevo_camino = camino + [vecino]
                    cola.append((vecino, nuevo_camino))
        
        tiempo_ms = (time.time() - inicio) * 1000
        
        # Determinar resultado
        if camino_a_otitis:
            # Marcar nodos en el camino FINAL
            for paso in pasos:
                if paso['nodo_actual'] in camino_a_otitis:
                    paso['en_camino'] = True
            
            return {
                'encontrado': True,
                'tiene_otitis': True,
                'probabilidad': 0.8,
                'camino_final': camino_a_otitis,
                'pasos': pasos,
                'tiempo_ms': tiempo_ms,
                'nodos_explorados': len(visitados)
            }
        else:
            # NO llegó a OTITIS = Paciente SANO
            return {
                'encontrado': False,
                'tiene_otitis': False,
                'probabilidad': 0.0,
                'camino_final': [],
                'pasos': pasos,
                'tiempo_ms': tiempo_ms,
                'nodos_explorados': len(visitados)
            }
    
    def dfs(self, sintoma_inicial):
        """
        DFS - Búsqueda en profundidad desde UN síntoma inicial
        Explora en profundidad usando pila (LIFO)
        Retorna todos los pasos de la exploración
        """
        if not sintoma_inicial or sintoma_inicial not in self.grafo:
            return self._resultado_vacio()
        
        inicio = time.time()
        pila = [(sintoma_inicial, [sintoma_inicial])]
        visitados = {sintoma_inicial}
        pasos = []
        paso_num = 0
        camino_a_otitis = None
        
        while pila:
            # Guardar estado ANTES de desapilar (para mostrar todo incluyendo el TOPE)
            paso_num += 1
            pila_visual = [n for n, _ in pila]
            nodo_actual, camino = pila[-1]  # Ver qué está en el TOPE sin sacarlo
            
            pasos.append({
                'paso': paso_num,
                'nodo_actual': nodo_actual,
                'pila': pila_visual.copy(),
                'visitados': visitados.copy(),
                'camino': camino.copy(),
                'en_camino': False
            })
            
            # Ahora sí desapilar del TOPE
            pila.pop()
            
            # Si llegamos a OTITIS
            if nodo_actual == "OTITIS":
                camino_a_otitis = camino
                break
            
            # Explorar vecinos (en reversa para mantener orden)
            vecinos = list(self.grafo.get(nodo_actual, []))
            for vecino in reversed(vecinos):
                if vecino not in visitados:
                    visitados.add(vecino)
                    nuevo_camino = camino + [vecino]
                    pila.append((vecino, nuevo_camino))
        
        tiempo_ms = (time.time() - inicio) * 1000
        
        # Determinar resultado
        if camino_a_otitis:
            # Marcar nodos en el camino FINAL
            for paso in pasos:
                if paso['nodo_actual'] in camino_a_otitis:
                    paso['en_camino'] = True
            
            return {
                'encontrado': True,
                'tiene_otitis': True,
                'probabilidad': 0.8,
                'camino_final': camino_a_otitis,
                'pasos': pasos,
                'tiempo_ms': tiempo_ms,
                'nodos_explorados': len(visitados)
            }
        else:
            # NO llegó a OTITIS = Paciente SANO
            return {
                'encontrado': False,
                'tiene_otitis': False,
                'probabilidad': 0.0,
                'camino_final': [],
                'pasos': pasos,
                'tiempo_ms': tiempo_ms,
                'nodos_explorados': len(visitados)
            }
    
    def _calcular_probabilidad(self, sintomas):
        """Calcula la probabilidad promedio de OTITIS basado en síntomas"""
        if not sintomas:
            return 0.0
        
        total = sum(self.pesos.get(s, 0) for s in sintomas)
        return min(1.0, total / len(sintomas))
    
    def _resultado_vacio(self):
        """Resultado cuando no hay síntomas"""
        return {
            'encontrado': False,
            'tiene_otitis': False,
            'probabilidad': 0.0,
            'camino_final': [],
            'sintomas_encontrados': [],
            'pasos': [],
            'tiempo_ms': 0.0,
            'nodos_explorados': 0
        }
    
    def obtener_grafo(self):
        return self.grafo
    
    def formatear_nombre(self, nombre):
        if nombre in ["OTITIS", "SANO"]:
            return nombre
        return nombre.replace("_", " ").title()
