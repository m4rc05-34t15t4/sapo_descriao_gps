import os
from qgis.core import QgsProject, QgsFeature, QgsGeometry, QgsPointXY
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon, QMovie
from qgis.PyQt.QtWidgets import QMessageBox, QDialog, QLineEdit, QPushButton, QVBoxLayout, QApplication, QAction, QLabel
from qgis.utils import iface
from qgis.gui import QgsMapToolEmitPoint
from qgis.gui import QgsMapToolIdentify
from qgis.PyQt.QtCore import Qt, QTimer, QSize

PLUGIN_NAME = "SAPO DESCRICAO"
MENU = "SAPO"

class PluginName:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = self.tr(f'&{MENU}')
        self.toolbar = self.iface.addToolBar(PLUGIN_NAME)
        self.toolbar.setObjectName(PLUGIN_NAME)

        self.gps_layer = QgsProject.instance().mapLayersByName('aux_reambulacao_p')[0]
        self.selection_tool = None
        
    def tr(self, message):
        return QCoreApplication.translate(PLUGIN_NAME, message)

    def add_action(self, icon_path, text, callback, enabled_flag=True, add_to_menu=True, add_to_toolbar=True, status_tip=None, whats_this=None, parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        
        if status_tip is not None:
            action.setStatusTip(status_tip)
            
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        
        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)
            
        if add_to_toolbar:
            self.toolbar.addAction(action)
        
        self.actions.append(action)
        return action

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, 'img/sapo_gps.png')
        self.add_action(icon_path, text=self.tr(f'{PLUGIN_NAME} - GPS'), callback=self.run, parent=self.iface.mainWindow())

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(f'&{MENU}'), action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        self.insert_point_from_gps()

    def insert_point_from_gps(self):
        # Obtenção das coordenadas do GPS
        gps_position = self.get_gps_position()
        if not gps_position:
            QMessageBox.warning(None, 'Erro', 'GPS não disponível ou não conectado.')
            return

        # Abrir diálogo para inserir descrição e coordenadas
        dialog = CoordinatesInputDialog(gps_position)
        if dialog.exec_() == QDialog.Accepted:
            description = dialog.description.text()
            # Pegar as coordenadas do campo combinado
            modified_coordinates = dialog.get_coordinates()
            if modified_coordinates:
                self.add_point_feature(modified_coordinates, description)
                # Abrir ferramenta de aquisição de ponto
                self.activate_point_tool()

    def get_gps_position(self):
        # Obter a instância atual do mapa
        canvas = iface.mapCanvas()
        # Obter a extensão atual do mapa
        extent = canvas.extent()
        # Calcular o centro da extensão
        center_x = (extent.xMinimum() + extent.xMaximum()) / 2
        center_y = (extent.yMinimum() + extent.yMaximum()) / 2

        return QgsPointXY(center_x, center_y)

    def add_point_feature(self, point, description):
        layer = self.gps_layer
        feature = QgsFeature(layer.fields())
        feature.setGeometry(QgsGeometry.fromPointXY(point))
        feature.setAttribute('descricao', description)

        # Iniciar a edição e adicionar a feição
        if not layer.isEditable():
            layer.startEditing()

        if not layer.addFeature(feature):
            QMessageBox.warning(None, 'Erro', 'Falha ao adicionar a feição.')
            return

        if not layer.commitChanges():
            QMessageBox.warning(None, 'Erro', 'Falha ao salvar as mudanças no layer.')
            layer.rollBack()

        # Habilitar a ferramenta de seleção genérica após adicionar o ponto
        self.activate_generic_selection_tool()

    def activate_generic_selection_tool(self):
        # Ativar a ferramenta de seleção genérica
        selection_tool = QgsMapToolIdentify(self.iface.mapCanvas())
        self.iface.mapCanvas().setMapTool(selection_tool)

    def activate_point_tool(self):
        # Ativar a ferramenta de aquisição de ponto
        self.selection_tool = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.iface.mapCanvas().setMapTool(self.selection_tool)


class CoordinatesInputDialog(QDialog):
    def __init__(self, gps_position):
        super().__init__()
        self.setWindowTitle("Inserir Descrição e Coordenadas")

        estilo_input_text = """
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #4CAF50; /* Cor da borda */
                border-radius: 10px;
                background-color: #F0F0F0;
            }
            QLineEdit:focus {
                border: 2px solid #66AFE9; /* Cor da borda quando focado */
                background-color: #FFFFFF;
            }
        """
        
        self.description = QLineEdit(self)
        self.description.setPlaceholderText("Descrição")
        self.description.setStyleSheet(estilo_input_text)

        # Cria um campo para as coordenadas
        self.coordinates = QLineEdit(self)
        self.coordinates.setPlaceholderText("Coordenadas (longitude,latitude)")
        self.coordinates.setText(f"{gps_position.x()}, {gps_position.y()}")  # Preencher com coordenadas GPS
        self.coordinates.setStyleSheet(estilo_input_text)

        # Botão OK
        self.ok_button = QPushButton("OK", self)

        # Estilizar o botão com QSS
        self.ok_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                color: white;
                background-color: #4CAF50; /* Cor de fundo */
                border: none;
                padding: 10px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #45A049; /* Cor quando o mouse estiver sobre o botão */
            }
            QPushButton:pressed {
                background-color: #2E7D32; /* Cor quando o botão estiver pressionado */
            }
        """)

        self.ok_button.clicked.connect(self.accept)

        # Criar um diálogo personalizado
        dialog = QDialog()
        dialog.setWindowTitle("Inserir Descrição")
        layout = QVBoxLayout(dialog)

        # Adicionar GIF animado
        gif_label = QLabel()
        plugin_dir = os.path.dirname(__file__)
        gif = QMovie(os.path.join(plugin_dir, "img/sapo_reambulador_digitando_video.gif"))  # Certifique-se de ter um GIF na pasta do plugin
        gif_label.setMovie(gif)
    
        gif.setScaledSize(QSize(310, 310))
        gif_label.setFixedSize(310, 310)  # Ajuste o tamanho do GIF conforme necessário
        gif_label.setAlignment(Qt.AlignCenter)
        gif.start()
        
        layout.addWidget(gif_label)  
        layout.addWidget(self.description)
        layout.addWidget(self.coordinates)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def get_coordinates(self):
        text = self.coordinates.text()
        try:
            lon, lat = map(float, text.split(','))
            return QgsPointXY(lon, lat)
        except ValueError:
            QMessageBox.warning(None, 'Erro', 'Coordenadas inválidas. Formato esperado: longitude,latitude.')
            return None


def classFactory(iface):
    return PluginName(iface)
