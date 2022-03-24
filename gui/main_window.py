
from PySide6.QtWidgets import QWidget, QTabBar, QListWidget, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog, QListWidgetItem

from lib.l5x_file import L5xFile
from lib.l5x_io import L5xModule


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.l5x_file = L5xFile("")

        self.setWindowTitle("l5x Viewer")
        self.setMinimumSize(800, 600)

        self.data_sdi = []
        self.data_sdo = []
        self.data_di = []
        self.data_do = []

        self.main_layout = QVBoxLayout(self)
        self.tab_container = QTabBar()
        self.list = QListWidget()
        self.list_detail = QListWidget()
        self.btn_load = QPushButton("Charger un fichier .l5x")
        self.btn_export = QPushButton("Exporter au format csv")

        self.row_list = QHBoxLayout()
        self.row_list.addWidget(self.list)
        self.row_list.addWidget(self.list_detail)

        self.row_btn = QHBoxLayout()
        self.row_btn.addWidget(self.btn_load)
        self.row_btn.addWidget(self.btn_export)

        self.tab_container.addTab("Entrées SAFETY")
        self.tab_container.addTab("Sorties SAFETY")
        self.tab_container.addTab("Entrées PROCESS")
        self.tab_container.addTab("Sorties PROCESS")

        self.main_layout.addWidget(self.tab_container)
        self.main_layout.addLayout(self.row_list)
        self.main_layout.addLayout(self.row_btn)

        self.btn_load.clicked.connect(self._load_file)
        self.btn_export.clicked.connect(self._export)
        self.tab_container.currentChanged.connect(self._load_data)
        self.list.currentRowChanged.connect(self._get_detail)

        self.current_tab = 0

    def _load_file(self):
        fileName, result = QFileDialog.getOpenFileName(
            self, "Charger un fichier .l5x", '', "Fichier .l5x (*.l5x)")
        if result:
            self.l5x_file = L5xFile(fileName)
            self.data_sdi = self.l5x_file.sdi
            self.data_sdo = self.l5x_file.sdo
            self.data_di = self.l5x_file.di
            self.data_do = self.l5x_file.do
            self._load_data(self.current_tab)

    def _load_data(self, index):
        self.current_tab = index
        self.list_detail.clear()
        self.list.clear()
        match index:
            case 0:
                if self.data_sdi:
                    self._fill_list(self.data_sdi)
            case 1:
                if self.data_sdo:
                    self._fill_list(self.data_sdo)
            case 2:
                if self.data_sdo:
                    self._fill_list(self.data_di)
            case 3:
                if self.data_sdo:
                    self._fill_list(self.data_do)

    def _fill_list(self, values: list):
        byte = 0
        for item in values:
            i = QListWidgetItem(f"BYTE {byte} = {item.name}")
            self.list.addItem(i)
            byte += 1

    def _get_detail(self, index):
        self.list_detail.clear()
        if index >= 0:
            match self.current_tab:
                case 0:
                    if len(self.data_sdi) >= index - 1:
                        self._fill_list_detail(self.data_sdi[index], index)
                case 1:
                    if len(self.data_sdi) >= index - 1:
                        self._fill_list_detail(self.data_sdo[index], index)
                case 2:
                    if len(self.data_sdi) >= index - 1:
                        self._fill_list_detail(self.data_di[index], index)
                case 3:
                    if len(self.data_sdi) >= index - 1:
                        self._fill_list_detail(self.data_do[index], index)

    def _fill_list_detail(self, values: list, index: int):
        for item in values.values:
            i = QListWidgetItem(f"BIT {index}{item.operand} = {item.name}")
            self.list_detail.addItem(i)

    def _export(self):
        file_name, result = QFileDialog.getSaveFileName(
            self, "Enregistrer sous", '', "Fichier .CSV (*.csv)")
        if result:
            if file_name.lower()[-4:] != ".csv":
                file_name += ".csv"
            
            data = "Type;Byte;Name;Bit;Address"
            
            for module in self.data_sdi:
                for add in module.values:
                    data += f"\nSafety input;{module.operand};{module.name};{module.operand}{add.operand};{add.name}"
            for module in self.data_sdo:
                for add in module.values:
                    data += f"\nSafety output;{module.operand};{module.name};{module.operand}{add.operand};{add.name}"
            for module in self.data_di:
                for add in module.values:
                    data += f"\nStandard input;{module.operand};{module.name};{module.operand}{add.operand};{add.name}"
            for module in self.data_do:
                for add in module.values:
                    data += f"\nStandard ouput;{module.operand};{module.name};{module.operand}{add.operand};{add.name}"
            
            
            with open(file_name, "w") as f:
                f.write(data)
                
    