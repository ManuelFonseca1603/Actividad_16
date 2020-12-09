from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QGraphicsScene
from PySide2.QtCore import Slot
from ui_mainwindow import Ui_MainWindow
from particulas.particula import Particula
from particulas.adm_part import Adm_part
from PySide2.QtGui import QPen, QColor, QTransform
from pprint import pprint, pformat
from particulas.algoritmos import busqueda_amplitud, busqueda_profundidad 


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()

        self.adm_part = Adm_part()    

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.agregar_final_pushButton.clicked.connect(self.click_agregar)
        self.ui.agregar_inicio_pushButton.clicked.connect(self.click_agregar_inicio)
        self.ui.mostrar_pushButton.clicked.connect(self.click_mostrar)

        self.ui.actionAbrir.triggered.connect(self.action_abrir_archivo)
        self.ui.actionGuardar.triggered.connect(self.action_guardar_archivo)

        self.ui.actionOrdenar_por_ID.triggered.connect(self.action_Ordenar_por_ID)
        self.ui.actionOrdenar_por_distancia.triggered.connect(self.action_Ordenar_por_distancia)
        self.ui.actionOrdenar_por_velocidad.triggered.connect(self.action_Ordenar_por_velocidad)

        self.ui.actionGrafo.triggered.connect(self.action_Grafo)

        self.ui.actionBusqueda_profundidad_anchura.triggered.connect(self.action_busqueda)

        self.ui.mostrar_tabla_pushButton.clicked.connect(self.mostrar_tabla)
        self.ui.buscar_pushButton.clicked.connect(self.buscar_id)

        self.ui.dibujar.clicked.connect(self.dibujar)
        self.ui.limpiar.clicked.connect(self.limpiar)

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

    def wheelEvent(self, event):
        if event.delta() > 0:
            self.ui.graphicsView.scale(1.2, 1.2)
        else:
            self.ui.graphicsView.scale(0.8, 0.8)

    @Slot()
    def action_busqueda(self):
        grafo = { }
        for particula in self.adm_part:
            key = particula.destino_x,particula.destino_y
            value = particula.origen_x,particula.origen_y
            if key in grafo:
                grafo[key].append(value)
            else:
                grafo[key] = [value] 

        for particula in self.adm_part:
            key = particula.origen_x,particula.origen_y
            value = particula.destino_x,particula.destino_y
            if key in grafo:
                grafo[key].append(value)
            else:
                grafo[key] = [value]         

        x = origen_x = self.ui.origen_x_spinBox.value()
        y = origen_y = self.ui.origen_y_spinBox.value()
        origen = x,y  
        print('\nVertice de inicio:',x,',',y)
        a = busqueda_profundidad(grafo, origen)
        b = busqueda_amplitud(grafo, origen)
        print(a,b)
           
    @Slot()
    def action_Grafo(self):
        grafo = { }
 
        for particula in self.adm_part:
            key = particula.origen_x,particula.origen_y
            value = (particula.destino_x,particula.destino_y),int(particula.distancia)
            if key in grafo:
                grafo[key].append(value)
            else:
                grafo[key] = [value]

        for particula in self.adm_part:
            key = particula.destino_x,particula.destino_y
            value = (particula.origen_x,particula.origen_y),int(particula.distancia)
            if key in grafo:
                grafo[key].append(value)
            else:
                grafo[key] = [value]            
        
        str = pformat(grafo, width=40, indent=1) 
        print(str)
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.insertPlainText(str)  
        
    @Slot()
    def action_Ordenar_por_ID(self):
        lista = []
        for particula in self.adm_part:
            lista.append(particula)
            lista.sort(key=lambda particula: particula.id) 

        for particula in lista:   
            self.adm_part.ordenar(particula)

    @Slot()
    def action_Ordenar_por_distancia(self):
        lista = []
        for particula in self.adm_part:
            lista.append(particula)
            lista.sort(key=lambda particula: particula.distancia, reverse=True)
        
        for particula in lista:    
            self.adm_part.ordenar(particula)     

    @Slot()
    def action_Ordenar_por_velocidad(self):
        lista = []
        for particula in self.adm_part:
            lista.append(particula)
            lista.sort(key=lambda particula: particula.velocidad)
        
        for particula in lista:    
           self.adm_part.ordenar(particula)               

    @Slot()
    def dibujar(self):
        pen = QPen()
        pen.setWidth(2)

        for particula in self.adm_part:
            r = int(particula.rojo)
            g = int(particula.verde)
            b = int(particula.azul)
            color = QColor(r, g, b)
            pen.setColor(color)

            origen_x = int(particula.origen_x)
            origen_y = int(particula.origen_y)
            destino_x = int(particula.destino_x)
            destino_y = int(particula.destino_y)

            self.scene.addEllipse(origen_x, origen_y, 3, 3, pen)
            self.scene.addEllipse(destino_x, destino_y, 3, 3, pen)
            self.scene.addLine(origen_x+3, origen_y+3, destino_x, destino_y, pen)

    @Slot()
    def limpiar(self):
        self.scene.clear()

    @Slot()
    def buscar_id(self):
        id = self.ui.buscar_spinBox.value()
        
        encontrado = False    
        for particula in self.adm_part:
            if id == particula.id:
                self.ui.tabla.clear()
                self.ui.tabla.setRowCount(1)

                id_widget = QTableWidgetItem(str(particula.id))
                origen_x_widget = QTableWidgetItem(str(particula.origen_x))
                origen_y_widget = QTableWidgetItem(str(particula.origen_y))
                destino_x_widget = QTableWidgetItem(str(particula.destino_x))
                destino_y_widget = QTableWidgetItem(str(particula.destino_y))
                velocidad_widget = QTableWidgetItem(str(particula.velocidad))
                rojo_widget = QTableWidgetItem(str(particula.rojo))
                verde_widget = QTableWidgetItem(str(particula.verde))
                azul_widget = QTableWidgetItem(str(particula.azul))
                distancia_widget = QTableWidgetItem(str(particula.distancia))

                self.ui.tabla.setItem(0,0,id_widget)
                self.ui.tabla.setItem(0,1,origen_x_widget)
                self.ui.tabla.setItem(0,2,origen_y_widget)
                self.ui.tabla.setItem(0,3,destino_x_widget)
                self.ui.tabla.setItem(0,4,destino_y_widget)
                self.ui.tabla.setItem(0,5,velocidad_widget)
                self.ui.tabla.setItem(0,6,rojo_widget)
                self.ui.tabla.setItem(0,7,verde_widget)
                self.ui.tabla.setItem(0,8,azul_widget)
                self.ui.tabla.setItem(0,9,distancia_widget)

                encontrado = True
                return
        if not encontrado:
            QMessageBox.warning(
                self,
                "Atención",
                f'La particula con el ID "{id}" no fue encontrada'   
            )        

    @Slot()
    def mostrar_tabla(self):
        self.ui.tabla.setColumnCount(10) 
        headers = ["ID","Origen en x", "Origen en y", "Destino en x", "Destino en y",
                     "Velocidad", "Rojo", "Verde", "Azul", "Distancia"]
        self.ui.tabla.setHorizontalHeaderLabels(headers)

        self.ui.tabla.setRowCount(len(self.adm_part))  

        row = 0
        for particula in self.adm_part:
            id_widget = QTableWidgetItem(str(particula.id))
            origen_x_widget = QTableWidgetItem(str(particula.origen_x))
            origen_y_widget = QTableWidgetItem(str(particula.origen_y))
            destino_x_widget = QTableWidgetItem(str(particula.destino_x))
            destino_y_widget = QTableWidgetItem(str(particula.destino_y))
            velocidad_widget = QTableWidgetItem(str(particula.velocidad))
            rojo_widget = QTableWidgetItem(str(particula.rojo))
            verde_widget = QTableWidgetItem(str(particula.verde))
            azul_widget = QTableWidgetItem(str(particula.azul))
            distancia_widget = QTableWidgetItem(str(particula.distancia))

            self.ui.tabla.setItem(row,0,id_widget)
            self.ui.tabla.setItem(row,1,origen_x_widget)
            self.ui.tabla.setItem(row,2,origen_y_widget)
            self.ui.tabla.setItem(row,3,destino_x_widget)
            self.ui.tabla.setItem(row,4,destino_y_widget)
            self.ui.tabla.setItem(row,5,velocidad_widget)
            self.ui.tabla.setItem(row,6,rojo_widget)
            self.ui.tabla.setItem(row,7,verde_widget)
            self.ui.tabla.setItem(row,8,azul_widget)
            self.ui.tabla.setItem(row,9,distancia_widget)

            row += 1

    @Slot()
    def action_abrir_archivo(self):
        #print('abrir_archivo')
        ubicacion = QFileDialog.getOpenFileName(
            self,
            'Abrir archivo',
            '.',
            'JSON(*.json)'
        )[0]
        if self.adm_part.abrir(ubicacion):
            QMessageBox.information(
                self,
                "Exito",
                "Se abrió el archivo " + ubicacion
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo abrir el archivo " + ubicacion
            )

    @Slot() 
    def action_guardar_archivo(self):
        #print('guardar_archivo')        
        ubicacion = QFileDialog.getSaveFileName(
            self,
            'Guardar Archivo',
            '.',
            'JSON (*.json)'
        )[0]
        print(ubicacion)
        if self.adm_part.guardar(ubicacion):
            QMessageBox.information(
                self,
                "Exito",
                "Se pudo crear el archivo " + ubicacion
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo crear el archivo " + ubicacion
            )    

    @Slot()
    def click_mostrar(self):
        #self.adm_part.mostrar()
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.insertPlainText(str(self.adm_part))
  
    @Slot()
    def click_agregar(self):
        id = self.ui.id_spinBox.value()
        origen_x = self.ui.origen_x_spinBox.value()
        origen_y = self.ui.origen_y_spinBox.value()
        destino_x = self.ui.destino_x_spinBox.value()
        destino_y = self.ui.destino_y_spinBox.value()
        velocidad = self.ui.velocidad_spinBox.value()
        rojo = self.ui.rojo_spinBox.value()
        azul = self.ui.azul_spinBox.value()
        verde = self.ui.verde_spinBox.value()

        particula = Particula (id,origen_x,origen_y,destino_x,destino_y,velocidad,rojo,verde,azul)
        self.adm_part.agregar_final(particula)    

        #print(id,origen_x,origen_y,destino_x,destino_y,rojo,azul,verde)
        #self.ui.plainTextEdit.insertPlainText(id + origen_x + origen_y +
                                                 #destino_x + destino_y + rojo + azul + verde)

    @Slot()
    def click_agregar_inicio(self):
        id = self.ui.id_spinBox.value()
        origen_x = self.ui.origen_x_spinBox.value()
        origen_y = self.ui.origen_y_spinBox.value()
        destino_x = self.ui.destino_x_spinBox.value()
        destino_y = self.ui.destino_y_spinBox.value()
        velocidad = self.ui.velocidad_spinBox.value()
        rojo = self.ui.rojo_spinBox.value()
        azul = self.ui.azul_spinBox.value()
        verde = self.ui.verde_spinBox.value()   

        particula = Particula(id,origen_x,origen_y,destino_x,destino_y,velocidad,rojo,verde,azul)
        self.adm_part.agregar_inicio(particula)                                            