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


        main_layout = QGridLayout()
        main_layout.addWidget(self.createTextGroupBox, 0, 0)

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
        bouton_fichier = QPushButton("Fichiers")
        bouton_fichier.setDefault(False)
        bouton_fichier.clicked.connect(self.fichier)
        self.combo_link = QComboBox(self)
        self.combo_link.addItem("Liste d'images à convertir (Selectionnez une image pour la retirer de la liste)")
        self.combo_link.currentTextChanged.connect(self.on_combolink_changed)
        bouton_clear = QPushButton("Vider la liste")
        bouton_clear.setDefault(False)
        bouton_clear.clicked.connect(self.clear)
        espace = QLabel("")
        link_d_label = QLabel("Saisir le chemin où sauvegarder l'image:")
        self.link_d_entree = QLineEdit("")
        bouton_dossier = QPushButton("Dossiers")
        bouton_dossier.setDefault(False)
        bouton_dossier.clicked.connect(self.dossier)
        bouton_clear_dossier = QPushButton("Vider le champ")
        bouton_clear_dossier.setDefault(False)
        bouton_clear_dossier.clicked.connect(self.clear_dossier)
        self.combo_exts = QComboBox(self)

        self.combo_exts.addItem("Selectionnez le format dans lequel convertir votre / vos image(s)")
        extensions = Image.registered_extensions()
        supported_extensions = {ex for ex, f in extensions.items() if f in Image.OPEN}
        supported_extensions = list(supported_extensions)
        supported_extensions = sorted(supported_extensions)
        for i in range(len(supported_extensions)):
            supported_extensions[i] = supported_extensions[i].replace(".", "")
            self.combo_exts.addItem(supported_extensions[i])

        bouton_conversion = QPushButton("Lancer la conversion")
        bouton_conversion.setDefault(False)
        bouton_conversion.clicked.connect(self.conversion)

        link_layout = QGridLayout()
        link_layout.addWidget(link_o_label, 0, 0)
        link_layout.addWidget(bouton_ajouter, 1, 2)
        link_layout.addWidget(bouton_fichier, 1, 1)
        link_layout.addWidget(self.link_o_entree, 1, 0)
        link_layout.addWidget(self.combo_link, 2, 0, 1 , 2 )
        link_layout.addWidget(bouton_clear, 2, 2)
        link_layout.addWidget(espace, 3, 0)
        link_layout.addWidget(link_d_label, 4, 0)
        link_layout.addWidget(self.link_d_entree, 5, 0)
        link_layout.addWidget(bouton_dossier, 5, 1)
        link_layout.addWidget(bouton_clear_dossier, 5, 2)
        link_layout.addWidget(self.combo_exts, 6, 0)
        link_layout.addWidget(bouton_conversion, 6, 1, 1, 3)

        self.createTextGroupBox.setLayout(link_layout)

    #Bouton fichier
    def fichier(self):
        format_validation = False

        extensions = Image.registered_extensions()
        supported_extensions = {ex for ex, f in extensions.items() if f in Image.OPEN}
        supported_extensions = list(supported_extensions)
        
        filepath = QtWidgets.QFileDialog.getOpenFileNames(self)
        print(filepath)
        for i in range(len(supported_extensions)):
            for y in range(len(filepath[0])):
                if supported_extensions[i] in filepath[0][y]:
                    path = str(filepath[0])
                    path = path.replace("[", "")
                    path = path.replace("]", "")
                    path = path.replace("'", "")
                    self.link_o_entree.setText(path)
                    format_validation = True

        for i in range(len(filepath[0])):
            if format_validation == False and filepath[0][i] != "":
                alert("Erreur de format", "Le fichier sélectionné n'est pas pris en charge.")
                return

    #Bouton Clear
    def clear(self):
        global save

        confirm_box = MessageBox()
        confirm_box.setText("Êtes vous sûr·e de vouloir vider la liste d'images ?")
        confirm_box.setWindowTitle("Validation de la suppression")
        confirm_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        confirm_value = confirm_box.exec()

        if confirm_value == QMessageBox.Ok:
            save = ([],[])
            self.combo_maker()
        else:
            return

    #Bouton Ajouter
    def ajouter(self):
        global save
        entree = self.link_o_entree.text()

        if "," in entree:
                entree = entree.split(", ")
        else:
            entree = [entree]

        if entree == "":
            alert("Erreur de champ", "Aucun lien n'a été saisi.")
        else:
            for i in range(len(entree)):
                entree_validation = (entree[i]).replace(os.path.sep, '/')
                isExist = os.path.exists(entree_validation)

                if isExist == False:
                    alert("Erreur de lien", f'Le lien {entree[i]} saisi n\'est pas valide.')
                    self.link_o_entree.setText("")
                else:
                    save[0].append((entree[i]).replace(os.path.sep, '/'))
                    nom_image = entree[i]
                    index = nom_image.rindex("/")
                    nom_image = entree[i][(index+1):]
                    if nom_image in save[1]:
                        alert("Erreur de nom", "Cette image est déjà dans la liste.")
                        self.link_o_entree.setText("")
                    else:
                        save[1].append(nom_image)
                        self.link_o_entree.setText("")
                        self.combo_maker()

    #Bouton Dossier
    def dossier(self):
        global save

        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.link_d_entree.setText(folderpath)

    #Bouton Dossier
    def clear_dossier(self):
        self.link_d_entree.setText("")

    #Bouton Conversion
    def conversion(self):
        global save
        
        if save[0] == [] or self.link_d_entree.text() == "" or self.combo_exts.currentText() == "Selectionnez le format dans lequel convertir votre / vos image(s)":
            alert("Erreur de lancement", "Une ou plusieurs erreurs sont survenues: vérifiez d'avoir au moins une image à convertir, d'avoir sélectionné un dossier où sauvegarder les résulats ainsi que d'avoir choisi un format de conversion.")
        else:
            folderpath = self.link_d_entree.text()
            isExist = os.path.exists(folderpath)

            if isExist == False:
                alert("Erreur de lien", "Le lien entré dans le champ n'est pas valide.")
            else:
                for i in range(len(save[0])):
                    index = (save[1][i]).index(".")
                    nom = (save[1][i])[:index]

                    try:
                        image = Image.open(save[0][i])
                        nom_final = f'{self.link_d_entree.text()}/{nom}.{self.combo_exts.currentText()}'
                        image.save(nom_final, format = self.combo_exts.currentText(), lossless = True)
                    except OSError:
                        image = Image.open(save[0][i])
                        nom_final = f'{self.link_d_entree.text()}/{nom}.{self.combo_exts.currentText()}'
                        image = image.convert('RGB')
                        image.save(nom_final, format = self.combo_exts.currentText(), lossless = True)
                    
                confirm_box = MessageBox()
                confirm_box.setText("La conversion est terminée, voulez vous quitter l'application?")
                confirm_box.setWindowTitle("Validation de fin de conversion")
                confirm_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                confirm_value = confirm_box.exec()

                if confirm_value == QMessageBox.Ok:
                    sys.exit()

    #Met à jour la liste de presets
    def combo_maker(self):
        global save 

        self.combo_link.clear()
        self.combo_link.addItem("Liste d'images à convertir (Selectionnez une image pour la retirer de la liste)")

        for i in range(len(save[1])):
            self.combo_link.addItem(save[1][i])

    #Detecte le changement de statut de la liste combolink
    def on_combolink_changed(self):
        
        if self.combo_link.currentText() != "" and self.combo_link.currentText() != "Liste d'images à convertir (Selectionnez une image pour la retirer de la liste)":
            confirm_box = MessageBox()
            confirm_box.setText("Êtes vous sûr·e de vouloir supprimer cette image de la liste ?")
            confirm_box.setWindowTitle("Validation de la suppression")
            confirm_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            confirm_value = confirm_box.exec()

            if confirm_value == QMessageBox.Ok:
                global save
                for i in range(len(save[1])):
                    if self.combo_link.currentText() in save[1][i]:
                        del save[0][i]
                        del save[1][i]
                        self.combo_maker()
            else:
                return

## Crée la fenêtre     
IFC_app = QApplication.instance() 
if not IFC_app:
    IFC_app = QApplication(sys.argv)  

fenetre_IFC = IFC()
fenetre_IFC.resize(600, 0)
fenetre_IFC.show()
IFC_app.exec_()
