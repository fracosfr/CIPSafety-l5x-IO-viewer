from PySide6.QtWidgets import QWidget, QFileDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from lib.l5x_file import L5xFile
from lib.l5x_io import L5xAddress, L5xModule


class ExportWindow(QWidget):
    def __init__(self, data: L5xFile) -> None:
        super().__init__()
        
        self.l5x_file = data

        self.setWindowTitle("Export CSV")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowFlag(Qt.Tool)
        self.setFixedSize(600, 350)

        self.main_layout = QVBoxLayout(self)

        self.main_layout.addWidget(QLabel("Heading pattern :"))
        self.input_pattern_head = QLineEdit(
            "Type;Byte;Module name;Operand address;Operand name")
        self.main_layout.addWidget(self.input_pattern_head)

        self.main_layout.addWidget(QLabel("Safety inputs pattern :"))
        self.input_pattern_sdi = QLineEdit(
            "Safety input;{byte};{module};{byte}{address};{name}")
        self.main_layout.addWidget(self.input_pattern_sdi)

        self.main_layout.addWidget(QLabel("Safety outputs pattern :"))
        self.input_pattern_sdo = QLineEdit(
            "Safety output;{byte};{module};{byte}{address};{name}")
        self.main_layout.addWidget(self.input_pattern_sdo)

        self.main_layout.addWidget(QLabel("Standard inputs pattern :"))
        self.input_pattern_di = QLineEdit(
            "Standard output;{byte};{module};{byte}{address};{name}")
        self.main_layout.addWidget(self.input_pattern_di)

        self.main_layout.addWidget(QLabel("Standard outputs pattern :"))
        self.input_pattern_do = QLineEdit(
            "Standard output;{byte};{module};{byte}{address};{name}")
        self.main_layout.addWidget(self.input_pattern_do)

        self.btn_export = QPushButton("Exporter")
        self.main_layout.addWidget(self.btn_export)
        self.btn_export.clicked.connect(self._export)

    def _export(self):
        file_name, result = QFileDialog.getSaveFileName(
            self, "Enregistrer sous", '', "Fichier .CSV (*.csv)")
        if result:
            try:
                if file_name.lower()[-4:] != ".csv":
                    file_name += ".csv"

                data = "Type;Byte;Name;Bit;Address"

                for module in self.l5x_file.sdi:
                    for add in module.values:
                        data += f"\n{self._parse_pattern(self.input_pattern_sdi.text(), module, add)}"
                for module in self.l5x_file.sdo:
                    for add in module.values:
                        data += f"\n{self._parse_pattern(self.input_pattern_sdo.text(), module, add)}"
                for module in self.l5x_file.di:
                    for add in module.values:
                        data += f"\n{self._parse_pattern(self.input_pattern_di.text(), module, add)}"
                for module in self.l5x_file.do:
                    for add in module.values:
                        data += f"\n{self._parse_pattern(self.input_pattern_do.text(), module, add)}"

                with open(file_name, "w") as f:
                    f.write(data)
                
                QMessageBox.information(self, "Terminé !", "L'export a été correctement effectué !")
                self.close()

            except:
                QMessageBox.critical(
                    self, "ERREUR !", "Une erreur est survenue lors de l'export !")
                
    def _parse_pattern(self, pattern: str, module: L5xModule, add: L5xAddress) -> str:
        resultat = pattern.replace("{byte}", module.operand)
        resultat = resultat.replace("{module}", module.name)
        resultat = resultat.replace("{name}", add.name)
        resultat = resultat.replace("{address}", add.operand)
        
        return resultat
