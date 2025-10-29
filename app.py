"""
Interfaz Gráfica Mejorada - Diagnóstico de Otitis
Muestra el proceso completo de BFS y DFS paso a paso
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from agente_otitis import AgenteOtitis
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class App:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Diagnóstico de Otitis - BFS y DFS Paso a Paso")
        self.root.geometry("3000x1000")  # Aumentado de 1600x1000 a 1800x1000
        self.root.configure(bg="#ecf0f1")
        
        self.agente = AgenteOtitis()
        self.sintoma_seleccionado = tk.StringVar(value="")  # Para radio buttons
        self.resultado = None
        self.paso_actual = 0
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        # Título
        titulo = tk.Label(
            self.root,
            text="🏥 Sistema de Diagnóstico de Otitis - Búsqueda BFS y DFS",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10
        )
        titulo.pack(fill=tk.X)
        
        # Frame principal
        main = tk.Frame(self.root, bg="#ecf0f1")
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo - DIVIDIDO EN DOS PARTES VERTICALES
        panel_izq = tk.Frame(main, bg="white", relief=tk.RAISED, bd=2)
        panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0,5))
        panel_izq.pack_propagate(False)  # No expandir automáticamente
        panel_izq.config(width=420, height=950)  # Ancho fijo de 420px
        
        # ========== PARTE SUPERIOR: Síntomas y Controles ==========
        panel_superior = tk.Frame(panel_izq, bg="white")
        panel_superior.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        
        tk.Label(
            panel_superior,
            text="📋 Síntomas del Paciente",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            pady=8
        ).pack(fill=tk.X)
        
        tk.Label(
            panel_superior,
            text="Seleccione UN síntoma inicial:",
            font=("Arial", 9, "italic"),
            bg="#ecf0f1",
            fg="#34495e",
            pady=4
        ).pack(fill=tk.X)
        
        # Frame principal que contiene síntomas Y botones lado a lado
        frame_principal_horizontal = tk.Frame(panel_superior, bg="white", height=210)  # Altura aumentada para ver todos los botones
        frame_principal_horizontal.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        frame_principal_horizontal.pack_propagate(False)  # Mantener altura fija
        
        # IZQUIERDA: Frame para síntomas en DOS COLUMNAS
        frame_sintomas_container = tk.Frame(frame_principal_horizontal, bg="white")
        frame_sintomas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Columna izquierda de síntomas
        frame_col_izq = tk.Frame(frame_sintomas_container, bg="white")
        frame_col_izq.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Columna derecha de síntomas
        frame_col_der = tk.Frame(frame_sintomas_container, bg="white")
        frame_col_der.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Configurar pesos para que sean del mismo tamaño
        frame_sintomas_container.grid_columnconfigure(0, weight=1)
        frame_sintomas_container.grid_columnconfigure(1, weight=1)
        frame_sintomas_container.grid_rowconfigure(0, weight=1)
        
        # Distribuir síntomas en dos columnas
        sintomas = self.agente.obtener_sintomas()
        mitad = (len(sintomas) + 1) // 2  # Redondear hacia arriba
        
        for i, sintoma in enumerate(sintomas):
            columna = frame_col_izq if i < mitad else frame_col_der
            tk.Radiobutton(
                columna,
                text=self.agente.formatear_nombre(sintoma),
                variable=self.sintoma_seleccionado,
                value=sintoma,
                font=("Arial", 9),
                bg="white",
                padx=3,
                pady=2,
                anchor="w"
            ).pack(anchor="w", padx=3, pady=1)
        
        # DERECHA: Frame para Modo y Botones
        frame_controles_derecha = tk.Frame(frame_principal_horizontal, bg="white", width=150)
        frame_controles_derecha.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        frame_controles_derecha.pack_propagate(False)
        
        # MODO: Selección de modo de operación
        frame_modo = tk.LabelFrame(frame_controles_derecha, text="Modo", bg="white", font=("Arial", 8, "bold"))
        frame_modo.pack(fill=tk.X, pady=(0, 8))
        
        self.modo_var = tk.StringVar(value="automatico")
        
        tk.Radiobutton(
            frame_modo,
            text="Automático",
            variable=self.modo_var,
            value="automatico",
            bg="white",
            font=("Arial", 7),
            command=self._cambiar_modo
        ).pack(anchor=tk.W, padx=3, pady=1)
        
        tk.Radiobutton(
            frame_modo,
            text="Interactivo",
            variable=self.modo_var,
            value="interactivo",
            bg="white",
            font=("Arial", 7),
            command=self._cambiar_modo
        ).pack(anchor=tk.W, padx=3, pady=1)
        
        # Botones de acción
        frame_botones = tk.Frame(frame_controles_derecha, bg="white")
        frame_botones.pack(fill=tk.BOTH, expand=True)
        # Botones de acción
        frame_botones = tk.Frame(frame_controles_derecha, bg="white")
        frame_botones.pack(fill=tk.BOTH, expand=True)
        
        self.btn_bfs = tk.Button(
            frame_botones,
            text="🔍 BFS",
            command=lambda: self._diagnosticar("BFS"),
            font=("Arial", 9, "bold"),
            bg="#27ae60",
            fg="white",
            pady=10,
            cursor="hand2"
        )
        self.btn_bfs.pack(fill=tk.X, pady=3)
        
        self.btn_dfs = tk.Button(
            frame_botones,
            text="🔍 DFS",
            command=lambda: self._diagnosticar("DFS"),
            font=("Arial", 9, "bold"),
            bg="#2980b9",
            fg="white",
            pady=10,
            cursor="hand2"
        )
        self.btn_dfs.pack(fill=tk.X, pady=3)
        
        tk.Button(
            frame_botones,
            text="🔄 Limpiar",
            command=self._limpiar,
            font=("Arial", 9),
            bg="#95a5a6",
            fg="white",
            pady=8,
            cursor="hand2"
        ).pack(fill=tk.X, pady=3)
        
        # Separador visual entre paneles
        ttk.Separator(panel_izq, orient='horizontal').pack(fill=tk.X, pady=5)
        
        # ========== PARTE INFERIOR: Cola/Pila y Paso a Paso ==========
        panel_inferior = tk.Frame(panel_izq, bg="white")
        panel_inferior.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        # Controles de navegación
        tk.Label(
            panel_inferior,
            text="⏯️ Navegación Paso a Paso",
            font=("Arial", 11, "bold"),
            bg="#34495e",
            fg="white",
            pady=6
        ).pack(fill=tk.X)
        
        nav = tk.Frame(panel_inferior, bg="white")
        nav.pack(fill=tk.X, padx=10, pady=8)
        
        self.btn_anterior = tk.Button(
            nav,
            text="◀",
            command=self._paso_anterior,
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="white",
            state=tk.DISABLED,
            width=3,
            cursor="hand2"
        )
        self.btn_anterior.pack(side=tk.LEFT, padx=2)
        
        self.label_paso = tk.Label(
            nav,
            text="Paso: 0/0",
            font=("Arial", 10, "bold"),
            bg="white"
        )
        self.label_paso.pack(side=tk.LEFT, expand=True)
        
        self.btn_siguiente = tk.Button(
            nav,
            text="▶",
            command=self._paso_siguiente,
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="white",
            state=tk.DISABLED,
            width=3,
            cursor="hand2"
        )
        self.btn_siguiente.pack(side=tk.RIGHT, padx=2)
        
        # Visualización de Cola/Pila
        tk.Label(
            panel_inferior,
            text="◇ Cola/Pila (Estructura de Datos)",
            font=("Arial", 10, "bold"),
            bg="#16a085",
            fg="white",
            pady=6
        ).pack(fill=tk.X)
        
        # Frame para canvas + scrollbar
        frame_canvas_scroll = tk.Frame(panel_inferior, bg="white")
        frame_canvas_scroll.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Canvas para dibujar la cola/pila gráficamente - CON SCROLLBAR
        self.canvas_estructura = tk.Canvas(
            frame_canvas_scroll,
            bg="#f8f9fa",
            highlightthickness=1,
            highlightbackground="#bdc3c7"
        )
        scrollbar = ttk.Scrollbar(frame_canvas_scroll, orient="vertical", command=self.canvas_estructura.yview)
        
        self.canvas_estructura.config(yscrollcommand=scrollbar.set)
        
        self.canvas_estructura.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Panel derecho - Visualización
        panel_der = tk.Frame(main, bg="white", relief=tk.RAISED, bd=2)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5,0))
        
        # Título con botón de ver resultado
        header_frame = tk.Frame(panel_der, bg="#e74c3c")
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text="📊 Visualización del Grafo - Proceso de Búsqueda",
            font=("Arial", 13, "bold"),
            bg="#e74c3c",
            fg="white",
            pady=10
        ).pack(side=tk.LEFT, padx=10)
        
        # Botón para ver historial completo de pasos
        self.btn_historial = tk.Button(
            header_frame,
            text="� Historial de Pasos",
            command=self._mostrar_historial_pasos,
            font=("Arial", 10, "bold"),
            bg="#9b59b6",
            fg="white",
            cursor="hand2",
            state=tk.DISABLED,
            pady=8,
            padx=15
        )
        self.btn_historial.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Frame para grafo (ocupa TODO el espacio)
        self.frame_grafo = tk.Frame(panel_der, bg="white")
        self.frame_grafo.pack(fill=tk.BOTH, expand=False, padx=0, pady=0)
    
    def _cambiar_modo(self):
        """Cambia entre modo automático e interactivo"""
        modo = self.modo_var.get()
        
        if modo == "automatico":
            messagebox.showinfo(
                "Modo Automático",
                "Selecciona UN síntoma inicial.\n\nEl algoritmo explorará automáticamente todos los pasos y podrás navegar con los botones ◄ ►."
            )
        else:
            # Modo interactivo
            messagebox.showinfo(
                "Modo Interactivo",
                "Selecciona UN síntoma inicial.\n\nHaz clic en BFS o DFS y el algoritmo te preguntará paso a paso si presentas cada síntoma."
            )
    
    def _diagnosticar(self, metodo):
        sintoma = self.sintoma_seleccionado.get()
        
        modo = self.modo_var.get()
        
        if not sintoma:
            messagebox.showwarning("Advertencia", "Seleccione UN síntoma inicial para comenzar")
            return
        
        sintoma_inicial = sintoma
        
        if modo == "automatico":
            # MODO 1: Recorrido automático completo
            if metodo == "BFS":
                self.resultado = self.agente.bfs(sintoma_inicial)
            else:
                self.resultado = self.agente.dfs(sintoma_inicial)
            
            self.paso_actual = 0
            self.metodo_usado = metodo
            self.sintomas_seleccionados = [sintoma]
            self._habilitar_navegacion()
            self._actualizar_paso()
            self.btn_historial.config(state=tk.NORMAL)
        
        else:
            # MODO 2: Diagnóstico interactivo - usa el mismo botón BFS/DFS
            self._iniciar_modo_interactivo(metodo, sintoma_inicial)
    
    def _iniciar_modo_interactivo(self, algoritmo, sintoma_inicial):
        """Inicia el modo interactivo con el algoritmo ya seleccionado (BFS o DFS)"""
        # Inicializar estado del algoritmo
        self.estado_interactivo = {
            'algoritmo': algoritmo,
            'camino': [sintoma_inicial],
            'visitados': {sintoma_inicial},
            'paso': 1,
            'encontro_otitis': False
        }
        
        if algoritmo == "BFS":
            from collections import deque
            self.estado_interactivo['cola'] = deque([(sintoma_inicial, [sintoma_inicial])])
        else:  # DFS
            self.estado_interactivo['pila'] = [(sintoma_inicial, [sintoma_inicial])]
        
        # Mostrar primer paso
        self._preguntar_sintoma_interactivo()
    
    def _preguntar_sintoma_interactivo(self):
        """Pregunta al usuario si tiene el siguiente síntoma según BFS/DFS"""
        estado = self.estado_interactivo
        
        # Obtener siguiente nodo según el algoritmo
        if estado['algoritmo'] == "BFS":
            if not estado['cola']:
                self._finalizar_interactivo(False)
                return
            nodo_actual, camino = estado['cola'][0]
        else:  # DFS
            if not estado['pila']:
                self._finalizar_interactivo(False)
                return
            nodo_actual, camino = estado['pila'][-1]
        
        # Si llegamos a OTITIS, mostrar diagnóstico directamente
        if nodo_actual == "OTITIS":
            self._finalizar_interactivo(True)
            return
        
        # Actualizar visualización en la VENTANA PRINCIPAL
        paso_visual = {
            'paso': estado['paso'],
            'nodo_actual': nodo_actual,
            'camino': camino,
            'visitados': estado['visitados'],
            'pila' if estado['algoritmo'] == "DFS" else 'cola': camino
        }
        
        # Mostrar en panel izquierdo (pila/cola)
        self._mostrar_detalle_paso(paso_visual)
        
        # Mostrar grafo actualizado
        self._dibujar_grafo(paso_visual)
        
        # Ventana PEQUEÑA solo para la pregunta
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Paso {estado['paso']} - {estado['algoritmo']}")
        ventana.geometry("450x280")
        ventana.configure(bg="white")
        ventana.grab_set()
        ventana.transient(self.root)  # Mantener encima de la ventana principal
        
        # Centrar ventana
        ventana.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (450 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (280 // 2)
        ventana.geometry(f"450x280+{x}+{y}")
        
        # Encabezado
        tk.Label(
            ventana,
            text=f"PASO {estado['paso']} - {estado['algoritmo']}",
            font=("Arial", 13, "bold"),
            bg="#9b59b6" if estado['algoritmo'] == "DFS" else "#3498db",
            fg="white",
            pady=15
        ).pack(fill=tk.X)
        
        # Pregunta
        tk.Label(
            ventana,
            text="¿Presenta este síntoma?",
            font=("Arial", 12, "bold"),
            bg="white",
            pady=20
        ).pack()
        
        tk.Label(
            ventana,
            text=self.agente.formatear_nombre(nodo_actual),
            font=("Arial", 16, "bold"),
            bg="#ffffcc",
            fg="#d35400",
            pady=20,
            relief=tk.RAISED,
            bd=3
        ).pack(fill=tk.X, padx=40)
        
        # Botones
        frame_botones = tk.Frame(ventana, bg="white")
        frame_botones.pack(pady=25)
        
        tk.Button(
            frame_botones,
            text="✅ SÍ",
            command=lambda: self._respuesta_interactiva(ventana, True, nodo_actual, camino),
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            width=12,
            pady=12,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=15)
        
        tk.Button(
            frame_botones,
            text="❌ NO",
            command=lambda: self._respuesta_interactiva(ventana, False, nodo_actual, camino),
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=12,
            pady=12,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=15)
    
    def _respuesta_interactiva(self, ventana, tiene_sintoma, nodo_actual, camino):
        """Procesa la respuesta del usuario en modo interactivo"""
        ventana.destroy()
        estado = self.estado_interactivo
        
        # Desencolar/desapilar
        if estado['algoritmo'] == "BFS":
            estado['cola'].popleft()
        else:
            estado['pila'].pop()
        
        if tiene_sintoma:
            # Usuario SÍ tiene el síntoma
            if nodo_actual == "OTITIS":
                estado['encontro_otitis'] = True
                estado['camino'] = camino
                self._finalizar_interactivo(True)
                return
            
            # Agregar a camino y explorar vecinos
            estado['camino'] = camino
            vecinos = self.agente.obtener_vecinos(nodo_actual)
            
            # Para DFS: agregar en orden REVERSO (igual que en agente_otitis.py)
            if estado['algoritmo'] == "DFS":
                vecinos = list(reversed(vecinos))
            
            for vecino in vecinos:
                if vecino not in estado['visitados']:
                    estado['visitados'].add(vecino)
                    nuevo_camino = camino + [vecino]
                    
                    if estado['algoritmo'] == "BFS":
                        estado['cola'].append((vecino, nuevo_camino))
                    else:  # DFS
                        estado['pila'].append((vecino, nuevo_camino))
            
            estado['paso'] += 1
            self._preguntar_sintoma_interactivo()
        else:
            # Usuario NO tiene el síntoma - continuar con siguiente en la estructura
            estado['paso'] += 1
            self._preguntar_sintoma_interactivo()
    
    def _finalizar_interactivo(self, tiene_otitis):
        """Muestra el resultado final del diagnóstico interactivo"""
        estado = self.estado_interactivo
        
        if tiene_otitis:
            messagebox.showinfo(
                "Diagnóstico Final",
                f"🔴 DIAGNÓSTICO: OTITIS\n\n"
                f"Algoritmo: {estado['algoritmo']}\n"
                f"Pasos realizados: {estado['paso']}\n"
                f"Nodos explorados: {len(estado['visitados'])}\n\n"
                f"Camino: {' → '.join([self.agente.formatear_nombre(n) for n in estado['camino']])}"
            )
        else:
            messagebox.showinfo(
                "Diagnóstico Final",
                f"✅ DIAGNÓSTICO: PACIENTE SANO\n\n"
                f"Algoritmo: {estado['algoritmo']}\n"
                f"Pasos realizados: {estado['paso']}\n"
                f"No se encontró un camino a OTITIS"
            )
    
    def _mostrar_opciones_interactivas(self, nodo_actual, vecinos, camino_recorrido):
        """DEPRECATED - Método antiguo del modo manual"""
        pass
    
    def _seleccionar_siguiente(self, ventana, vecino, camino_anterior):
        """DEPRECATED - Método antiguo del modo manual"""
        pass
    
    def _mostrar_historial_pasos(self):
        """Muestra TODOS los pasos acumulados en una ventana"""
        if not self.resultado:
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title(f"📜 Historial Completo - {self.metodo_usado}")
        ventana.geometry("900x700")
        ventana.configure(bg="white")
        
        # Título
        tk.Label(
            ventana,
            text=f"� HISTORIAL DE PASOS - {self.metodo_usado}",
            font=("Arial", 16, "bold"),
            bg="#9b59b6",
            fg="white",
            pady=15
        ).pack(fill=tk.X)
        
        # Información general
        info_frame = tk.Frame(ventana, bg="#ecf0f1")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            info_frame,
            text=f"Síntoma inicial: {self.agente.formatear_nombre(self.sintomas_seleccionados[0])}  |  Total de pasos: {len(self.resultado['pasos'])}  |  Nodos explorados: {self.resultado['nodos_explorados']}",
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).pack(pady=5)
        
        # Área de texto con scroll
        frame_texto = tk.Frame(ventana, bg="white")
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        texto = scrolledtext.ScrolledText(
            frame_texto,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#f8f9fa",
            padx=10,
            pady=10
        )
        texto.pack(fill=tk.BOTH, expand=True)
        
        # Generar historial completo
        output = ""
        for paso in self.resultado['pasos']:
            output += "═" * 80 + "\n"
            output += f"PASO {paso['paso']}\n"
            output += "═" * 80 + "\n\n"
            
            # Mostrar acción si existe (agregando vecino)
            if 'accion' in paso:
                output += f"🔹 {paso['accion']}\n\n"
            
            output += f"NODO ACTUAL: {self.agente.formatear_nombre(paso['nodo_actual'])}\n\n"
            
            output += "CAMINO RECORRIDO:\n"
            output += "  " + " → ".join([self.agente.formatear_nombre(n) for n in paso['camino']]) + "\n\n"
            
            # Cola o Pila
            if 'cola' in paso:
                output += "� COLA (BFS - FIFO):\n"
                if paso['cola']:
                    output += "  [SALE] ← "
                    output += " ← ".join([self.agente.formatear_nombre(n) for n in paso['cola']])
                    output += " [ENTRA]\n"
                    output += f"\n  Próximo a procesar: {self.agente.formatear_nombre(paso['cola'][0])}\n"
                else:
                    output += "  (Cola vacía)\n"
            elif 'pila' in paso:
                output += "📚 PILA (DFS - LIFO):\n"
                if paso['pila']:
                    pila_visual = list(reversed(paso['pila']))
                    output += "  [TOPE]\n"
                    for n in pila_visual:
                        output += f"  │ {self.agente.formatear_nombre(n)} │\n"
                    output += "  [BASE]\n"
                    output += f"\n  Próximo a procesar: {self.agente.formatear_nombre(pila_visual[0])}\n"
                else:
                    output += "  (Pila vacía)\n"
            
            output += f"\n✓ Nodos visitados hasta ahora: {len(paso['visitados'])}\n"
            output += "\n\n"
        
        # Resultado final
        output += "═" * 80 + "\n"
        output += "RESULTADO FINAL\n"
        output += "═" * 80 + "\n\n"
        
        if self.resultado['tiene_otitis']:
            output += "🔴 DIAGNÓSTICO: OTITIS DETECTADA\n\n"
            output += "Camino final:\n  "
            output += " → ".join([self.agente.formatear_nombre(n) for n in self.resultado['camino_final']])
            output += "\n"
        else:
            output += "✅ DIAGNÓSTICO: PACIENTE SANO\n\n"
            output += "No se encontró un camino que llegue a OTITIS.\n"
            output += "El algoritmo exploró todos los nodos posibles sin llegar al diagnóstico.\n"
        
        output += f"\n⏱️ Tiempo total: {self.resultado['tiempo_ms']:.3f} ms\n"
        
        texto.insert(tk.END, output)
        texto.config(state=tk.DISABLED)
        
        # Botón cerrar
        tk.Button(
            ventana,
            text="✖ Cerrar",
            command=ventana.destroy,
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            pady=10,
            padx=30
        ).pack(pady=15)
    
    def _habilitar_navegacion(self):
        if self.resultado and self.resultado['pasos']:
            self.btn_siguiente.config(state=tk.NORMAL)
        self.btn_anterior.config(state=tk.DISABLED)
    
    def _paso_anterior(self):
        if self.paso_actual > 0:
            self.paso_actual -= 1
            self._actualizar_paso()
    
    def _paso_siguiente(self):
        if self.resultado and self.paso_actual < len(self.resultado['pasos']) - 1:
            self.paso_actual += 1
            self._actualizar_paso()
    
    def _actualizar_paso(self):
        if not self.resultado or not self.resultado['pasos']:
            return
        
        pasos = self.resultado['pasos']
        total = len(pasos)
        
        # Actualizar botones
        self.btn_anterior.config(state=tk.NORMAL if self.paso_actual > 0 else tk.DISABLED)
        self.btn_siguiente.config(state=tk.NORMAL if self.paso_actual < total - 1 else tk.DISABLED)
        self.label_paso.config(text=f"Paso: {self.paso_actual + 1}/{total}")
        
        paso = pasos[self.paso_actual]
        self._mostrar_detalle_paso(paso)
        self._dibujar_grafo(paso)  # Esto ya incluye la estructura
    
    def _mostrar_detalle_paso(self, paso):
        """Dibuja el CAMINO ACUMULADO y la FRONTERA (cola/pila) de exploración"""
        self.canvas_estructura.delete("all")
        
        # Título del paso
        self.canvas_estructura.create_text(
            175, 12, 
            text=f"PASO {paso['paso']}", 
            font=("Arial", 11, "bold"),
            fill="#2c3e50"
        )
        
        # 1. CAMINO ACUMULADO (lo que se ha recorrido) - MÁS GRANDE
        self.canvas_estructura.create_rectangle(
            5, 28, 345, 178,
            fill="#ecf0f1", outline="#34495e", width=2
        )
        self.canvas_estructura.create_text(
            175, 40,
            text="🗺️ CAMINO RECORRIDO (Memoria)",
            font=("Arial", 10, "bold"),
            fill="#16a085"
        )
        
        # Dibujar el camino como cadena de nodos
        camino = paso.get('camino', [])
        if camino:
            y_pos = 60
            x_start = 15
            max_width = 310
            espacio_x = 65
            
            # Dibujar nodos del camino
            for i, nodo in enumerate(camino):
                nombre = self.agente.formatear_nombre(nodo)[:9]
                x = x_start + (i * espacio_x) % max_width
                
                # Saltar a nueva línea si es necesario
                if i > 0 and (i * espacio_x) % max_width < ((i-1) * espacio_x) % max_width:
                    y_pos += 45
                
                # Color según si es el nodo actual
                color = "#e74c3c" if nodo == paso['nodo_actual'] else "#16a085"
                
                # Círculo del nodo MÁS GRANDE
                radio = 16
                self.canvas_estructura.create_oval(
                    x, y_pos, x + radio*2, y_pos + radio*2,
                    fill=color, outline="black", width=2
                )
                
                # Número de paso
                self.canvas_estructura.create_text(
                    x + radio, y_pos + radio,
                    text=str(i+1),
                    font=("Arial", 10, "bold"),
                    fill="white"
                )
                
                # Nombre debajo MÁS GRANDE
                self.canvas_estructura.create_text(
                    x + radio, y_pos + radio*2 + 10,
                    text=nombre,
                    font=("Arial", 8),
                    fill="#2c3e50"
                )
                
                # Flecha al siguiente
                if i < len(camino) - 1:
                    next_x = x_start + ((i+1) * espacio_x) % max_width
                    # Solo dibujar flecha si está en la misma línea
                    if (i * espacio_x) % max_width < ((i+1) * espacio_x) % max_width:
                        self.canvas_estructura.create_line(
                            x + radio*2, y_pos + radio, 
                            next_x, y_pos + radio,
                            arrow=tk.LAST, fill="#34495e", width=2
                        )
        
        # 2. FRONTERA (Cola/Pila) - Nodos por explorar
        y_frontera = 185
        if 'cola' in paso:
            self._dibujar_cola_fifo(paso, y_frontera)
        elif 'pila' in paso:
            self._dibujar_pila_lifo(paso, y_frontera)
        
        # Información de nodos visitados
        self.canvas_estructura.create_text(
            175, 338,
            text=f"✓ Total Visitados: {len(paso['visitados'])}",
            font=("Arial", 9),
            fill="#27ae60"
        )
    
    def _dibujar_cola_fifo(self, paso, y_inicio=185):
        """Dibuja COLA (FIFO) - Mostrando TODOS los visitados acumulados"""
        # Título
        self.canvas_estructura.create_rectangle(
            10, y_inicio, 340, y_inicio + 30,
            fill="#3498db", outline="black", width=2
        )
        self.canvas_estructura.create_text(
            175, y_inicio + 15,
            text="📋 COLA ACUMULADA (BFS - FIFO)",
            font=("Arial", 10, "bold"),
            fill="white"
        )
        
        # Indicadores
        self.canvas_estructura.create_text(
            50, y_inicio + 45,
            text="INICIO ←",
            font=("Arial", 8, "bold"),
            fill="#16a085"
        )
        self.canvas_estructura.create_text(
            300, y_inicio + 45,
            text="→ ACTUAL",
            font=("Arial", 8, "bold"),
            fill="#e74c3c"
        )
        
        # Obtener el CAMINO como cola acumulada
        cola_acumulada = paso.get('camino', [])
        
        # Dibujar elementos
        if cola_acumulada:
            x_inicio = 40
            ancho = 45
            altura = 30
            y = y_inicio + 65
            
            for i, nodo in enumerate(cola_acumulada[:6]):
                nombre = self.agente.formatear_nombre(nodo)[:6]
                x = x_inicio + (i * (ancho + 3))
                
                # Color: primero verde (inicio), último rojo (actual)
                if i == 0:
                    color = "#16a085"  # Verde - primero
                elif i == len(cola_acumulada)-1:
                    color = "#e74c3c"  # Rojo - actual
                else:
                    color = "#95a5a6"  # Gris
                
                self.canvas_estructura.create_rectangle(
                    x, y, x + ancho, y + altura,
                    fill=color, outline="black", width=2
                )
                self.canvas_estructura.create_text(
                    x + ancho/2, y + altura/2,
                    text=f"{i+1}",
                    font=("Arial", 9, "bold"),
                    fill="white"
                )
                self.canvas_estructura.create_text(
                    x + ancho/2, y + altura + 8,
                    text=nombre,
                    font=("Arial", 7),
                    fill="#2c3e50"
                )
                
                if i < len(cola_acumulada) - 1 and i < 5:
                    self.canvas_estructura.create_text(
                        x + ancho + 1, y + altura/2,
                        text="→",
                        font=("Arial", 10),
                        fill="#34495e"
                    )
            
            if len(cola_acumulada) > 6:
                self.canvas_estructura.create_text(
                    175, y + altura + 20,
                    text=f"+{len(cola_acumulada) - 6} más",
                    font=("Arial", 7, "italic"),
                    fill="#7f8c8d"
                )
        else:
            self.canvas_estructura.create_text(
                175, y_inicio + 70,
                text="(Vacía)",
                font=("Arial", 9, "italic"),
                fill="#7f8c8d"
            )
    
    def _dibujar_pila_lifo(self, paso, y_inicio=185):
        """Dibuja PILA (LIFO) - Mostrando TODOS los visitados acumulados"""
        # Título
        self.canvas_estructura.create_rectangle(
            10, y_inicio, 340, y_inicio + 30,
            fill="#9b59b6", outline="black", width=2
        )
        self.canvas_estructura.create_text(
            175, y_inicio + 15,
            text="📚 PILA ACUMULADA (DFS - LIFO)",
            font=("Arial", 10, "bold"),
            fill="white"
        )
        
        # Indicador
        self.canvas_estructura.create_text(
            175, y_inicio + 40,
            text="↑ TOPE (último visitado) ↑",
            font=("Arial", 8, "bold"),
            fill="#e74c3c"
        )
        
        # Obtener el CAMINO como pila acumulada (todos los nodos visitados en orden)
        pila_acumulada = paso.get('camino', [])
        
        # Dibujar elementos verticalmente
        if pila_acumulada:
            pila_invertida = list(reversed(pila_acumulada))  # TOPE arriba
            
            ancho = 180
            altura = 25
            x = 175 - ancho/2
            y = y_inicio + 60
            
            for i, nodo in enumerate(pila_invertida[:5]):
                nombre = self.agente.formatear_nombre(nodo)
                y_actual = y + (i * (altura + 3))
                
                # Color: TOPE (último visitado) en rojo, BASE (primero) oscuro
                if i == 0:
                    color = "#e74c3c"  # Rojo - TOPE (actual)
                elif i == len(pila_invertida)-1:
                    color = "#34495e"  # Oscuro - BASE (inicial)
                else:
                    color = "#95a5a6"  # Gris
                
                self.canvas_estructura.create_rectangle(
                    x, y_actual, x + ancho, y_actual + altura,
                    fill=color, outline="black", width=2
                )
                self.canvas_estructura.create_text(
                    175, y_actual + altura/2,
                    text=f"{len(pila_acumulada)-i}. {nombre}",
                    font=("Arial", 8, "bold"),
                    fill="white"
                )
            
            if len(pila_acumulada) > 5:
                self.canvas_estructura.create_text(
                    175, y + (5 * (altura + 3)) + 10,
                    text=f"+{len(pila_acumulada) - 5} más abajo",
                    font=("Arial", 7, "italic"),
                    fill="#7f8c8d"
                )
        else:
            self.canvas_estructura.create_text(
                175, y_inicio + 70,
                text="(Vacía)",
                font=("Arial", 9, "italic"),
                fill="#7f8c8d"
            )
    
    def _dibujar_grafo(self, paso):
        # Limpiar SOLO los widgets de grafo, sin destruir el frame
        for widget in self.frame_grafo.winfo_children():
            widget.destroy()
        
        # Crear figura sin bordes ni espacios
        fig = plt.figure(figsize=(14, 11), dpi=80)
        fig.patch.set_facecolor('white')
        ax = fig.add_subplot(111)
        
        # Márgenes ajustados para centrar bien el grafo
        fig.subplots_adjust(left=0.05, right=0.95, top=0.98, bottom=0.05)
        
        G = nx.DiGraph()
        for nodo, vecinos in self.agente.obtener_grafo().items():
            for vecino in vecinos:
                G.add_edge(nodo, vecino)
        
        pos = self._layout_jerarquico()
        
        # Colores
        node_colors = []
        node_sizes = []
        
        nodo_actual = paso['nodo_actual']
        visitados = paso['visitados']
        camino = paso['camino']
        
        for node in G.nodes():
            if node == nodo_actual:
                node_colors.append('#f39c12')  # Naranja - explorando
                node_sizes.append(5000)
            elif node in camino:
                node_colors.append('#27ae60')  # Verde - en camino
                node_sizes.append(4500)
            elif node in visitados:
                node_colors.append('#95a5a6')  # Gris - visitado
                node_sizes.append(4000)
            elif node == "OTITIS":
                node_colors.append('#e74c3c')  # Rojo - objetivo
                node_sizes.append(5500)
            else:
                node_colors.append('#ecf0f1')  # Gris claro - no visitado
                node_sizes.append(4000)
        
        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes,
                               edgecolors='black', linewidths=2.5, ax=ax)
        
        # Dibujar etiquetas CON MEJOR LEGIBILIDAD
        labels = {}
        for node in G.nodes():
            nombre = self.agente.formatear_nombre(node)
            # Separar en dos líneas si es muy largo
            if len(nombre) > 10:
                palabras = nombre.split()
                if len(palabras) >= 2:
                    labels[node] = '\n'.join(palabras)
                else:
                    labels[node] = nombre
            else:
                labels[node] = nombre
        
        nx.draw_networkx_labels(G, pos, labels, font_size=9, font_weight='bold',
                                font_color='black', ax=ax,
                                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                        edgecolor='none', alpha=0.9))
        
        # Dibujar aristas MÁS DELGADAS para no saturar
        nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=18, arrowstyle='-|>',
                              edge_color='#34495e', width=2, ax=ax, alpha=0.6,
                              node_size=node_sizes, min_source_margin=30, min_target_margin=30)
        
        # Leyenda
        from matplotlib.patches import Patch
        legend = [
            Patch(facecolor='#f39c12', edgecolor='black', label='Explorando ahora'),
            Patch(facecolor='#27ae60', edgecolor='black', label='En camino actual'),
            Patch(facecolor='#95a5a6', edgecolor='black', label='Visitado'),
            Patch(facecolor='#ecf0f1', edgecolor='black', label='No visitado'),
            Patch(facecolor='#e74c3c', edgecolor='black', label='OTITIS (objetivo)')
        ]
        ax.legend(handles=legend, loc='upper right', fontsize=10, framealpha=0.95,
                 edgecolor='black', fancybox=True, shadow=True)
        
        ax.set_title(f"Paso {paso['paso']}: Explorando '{self.agente.formatear_nombre(nodo_actual)}'",
                    fontsize=15, fontweight='bold', pad=20, color='#2c3e50')
        
        # Límites ajustados al nuevo layout
        ax.set_xlim(-0.5, 12.5)
        ax.set_ylim(-3.5, 7)
        ax.axis('off')
        
        # Líneas de nivel (opcionales, sutiles) - COMENTADAS para menos desorden
        # for y in [6, 4, 2, 0, -2.5]:
        #     ax.axhline(y=y, color='lightgray', linestyle='--', linewidth=0.5, alpha=0.2)
        
        # Embed en tkinter sin bloqueos
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafo)
        canvas.draw_idle()  # Usar draw_idle en lugar de draw para evitar bloqueos
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        plt.close(fig)
    
    def _layout_jerarquico(self):
        """
        Layout JERÁRQUICO - SIN NODO SANO
        
        ESTRUCTURA MÉDICA:
        Y=6: Síntomas iniciales leves (dolor_oido, zumbido)
        Y=4.5: Síntomas intermedios (presion_oido, fiebre, perdida_audicion)
        Y=3: Escalofríos (puede empeorar)
        Y=1.5: Síntomas graves (oido_tapado, dolor_punzante, fiebre_alta)
        Y=0: Secreción (crítico)
        Y=-2: OTITIS (único diagnóstico explícito)
        
        Si no llega a OTITIS = SANO (sin nodo en el grafo)
        """
        return {
            # NIVEL 1 (Y=6): Síntomas iniciales
            'dolor_oido': (3, 6),
            'zumbido': (9, 6),
            
            # NIVEL 2 (Y=4.5): Síntomas intermedios
            'presion_oido': (2, 4.5),
            'fiebre': (6, 4.5),
            'perdida_audicion': (10, 4.5),
            
            # NIVEL 2.5 (Y=3): Escalofríos (evoluciona)
            'escalofrios': (8, 3),
            
            # NIVEL 3 (Y=1.5): Síntomas graves
            'oido_tapado': (2, 1.5),
            'dolor_punzante': (5, 1.5),
            'fiebre_alta': (8, 1.5),
            
            # NIVEL 4 (Y=0): Síntoma crítico
            'secrecion': (6, 0),
            
            # NIVEL 5 (Y=-2): Diagnóstico
            'OTITIS': (6, -2)
        }
    
    def _limpiar(self):
        self.sintoma_seleccionado.set("")  # Deseleccionar radio button
        self.resultado = None
        self.paso_actual = 0
        self.btn_anterior.config(state=tk.DISABLED)
        self.btn_siguiente.config(state=tk.DISABLED)
        self.btn_historial.config(state=tk.DISABLED)
        self.label_paso.config(text="Paso: 0/0")
        self.canvas_estructura.delete("all")
        for widget in self.frame_grafo.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
