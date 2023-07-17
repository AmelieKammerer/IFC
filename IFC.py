import sys
import os 
from pathlib import Path
from PIL import Image
from PIL import features
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QGroupBox, QComboBox, QLineEdit, QDialogButtonBox, QLabel, QGridLayout, QLineEdit, QStyleFactory, QMessageBox, QWidget, QScrollArea

global save
save = ([],[])

##Permet à l'exécutable de trouver l'emplacement depuis lequel il est executé
if getattr(sys, 'frozen', False):
    root = os.path.abspath(".")
else:
    root = Path(__file__).parent
    root = str(root).replace(os.path.sep, '/')

##Fonction de message d'alerte
def alert(titre, description):
    warning_box = MessageBox()
    warning_box.setText(description)
    warning_box.setWindowTitle(titre)
    warning_box.setStandardButtons(QMessageBox.Ok)
    warning_box.exec()

##Modifie QmessageBox pour aligner au centre son contenu
class MessageBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid_layout = self.layout()

        qt_msgboxex_icon_label = self.findChild(QLabel, "qt_msgboxex_icon_label")
        qt_msgboxex_icon_label.deleteLater()

        qt_msgbox_label = self.findChild(QLabel, "qt_msgbox_label")
        qt_msgbox_label.setAlignment(Qt.AlignCenter)
        grid_layout.removeWidget(qt_msgbox_label)

        qt_msgbox_buttonbox = self.findChild(QDialogButtonBox, "qt_msgbox_buttonbox")
        grid_layout.removeWidget(qt_msgbox_buttonbox)

        grid_layout.addWidget(qt_msgbox_label, 0, 0)
        grid_layout.addWidget(qt_msgbox_buttonbox, 1, 0, alignment=Qt.AlignCenter)

## Création d'une classe créant l'interface graphique de la fenêtre d'accueil
class IFC(QDialog):
    # Initialisation de la classe: on indique que l'on veut deux zones dans la fenêtre.
    def __init__(self, parent = None):
        super(IFC, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        self.createTextGroupBox()
        #self.createDotsGroupBox()

        main_layout = QGridLayout()
        main_layout.addWidget(self.createTextGroupBox, 0, 0)
        #main_layout.addWidget(self.createDotsGroupBox, 1, 0)

        self.setWindowTitle("IFC")
        self.changeStyle('Fusion')

        self.setLayout(main_layout)

    # Change le style de la fenêtre
    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        QApplication.setPalette(self.originalPalette)

    # Création de la zone où l'utilisateur sélectionnera la/les images à convertir puis le dossier vers lequel sauvegarder les images converties
    def createTextGroupBox(self):
        self.createTextGroupBox = QGroupBox()

        link_o_label = QLabel("Saisir le chemin vers l'image à convertir:")
        self.link_o_entree = QLineEdit("")
        bouton_ajouter = QPushButton("Ajouter")
        bouton_ajouter.setDefault(False)
        bouton_ajouter.clicked.connect(self.ajouter)
        bouton_dossier = QPushButton("Dossier")
        bouton_dossier.setDefault(False)
        bouton_dossier.clicked.connect(self.dossier)
        self.combo_link = QComboBox(self)
        self.combo_link.addItem("Liste d'images à convertir")
        espace = QLabel("")
        link_d_label = QLabel("Saisir le chemin où sauvegarder l'image:")
        self.link_d_entree = QLineEdit("")

        link_layout = QGridLayout()
        link_layout.addWidget(link_o_label, 0, 0)
        link_layout.addWidget(bouton_ajouter, 1, 2)
        link_layout.addWidget(bouton_dossier, 1, 1)
        link_layout.addWidget(self.link_o_entree, 1, 0)
        link_layout.addWidget(self.combo_link, 2, 0, 1 , 4 )
        link_layout.addWidget(espace, 3, 0)
        link_layout.addWidget(link_d_label, 4, 0)
        link_layout.addWidget(self.link_d_entree, 5, 0)

        self.createTextGroupBox.setLayout(link_layout)

    #Bouton Dossier
    def dossier(self):
        format_validation = False

        extensions = Image.registered_extensions()
        supported_extensions = {ex for ex, f in extensions.items() if f in Image.OPEN}
        supported_extensions = list(supported_extensions)
        
        folderpath = QtWidgets.QFileDialog.getOpenFileName(self)
        for i in range(len(supported_extensions)):
            if supported_extensions[i] in folderpath[0]:
                self.link_o_entree.setText(folderpath[0])
                format_validation = True

        if format_validation == False:
            alert("Erreur de format", "Le fichier sélectionné n'est pas pris en charge.")

    #Bouton Ajouter
    def ajouter(self):
        global save
        print(type(save))
        entree = self.link_o_entree.text()

        if entree == "":
            alert("Erreur de champ", "Aucun lien n'a été saisi.")
        else:
            entree_validation = entree.replace(os.path.sep, '/')
            isExist = os.path.exists(entree_validation)

            if isExist == False:
                alert("Erreur de lien", "Le lien saisi n'est pas valide.")
                self.link_o_entree.setText("")
            else:
                save[0].append(entree.replace(os.path.sep, '/'))
                nom_image = entree
                index = nom_image.rindex("/")
                nom_image = entree[(index+1):]
                save[1].append(nom_image)
                


## Crée la fenêtre     
IFC_app = QApplication.instance() 
if not IFC_app:
    IFC_app = QApplication(sys.argv)  

fenetre_IFC = IFC()
fenetre_IFC.resize(600, 0)
fenetre_IFC.show()
IFC_app.exec_()
