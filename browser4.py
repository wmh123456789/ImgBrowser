import sys
import os
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QImageReader, QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QFileDialog, QGraphicsPixmapItem, QGraphicsScene, QMainWindow, QListWidget, QMenu, QMenuBar, QAction, QSplitter, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QGraphicsView, QToolBar, QPushButton, QCheckBox, QLineEdit

class ImageBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_scale = 1.0
        self.current_file_path = None
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Image Browser')

        # Menu Bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        openFile = QAction('Open File', self)
        openFile.triggered.connect(self.showDialogOpenFile)
        fileMenu.addAction(openFile)

        openFolder = QAction('Open Folder', self)
        openFolder.triggered.connect(self.showDialogOpenFolder)
        fileMenu.addAction(openFolder)

        # File List Widget
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.load_image)

        # Image Viewer
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        # Set initial width for file list
        font_metrics = self.list_widget.fontMetrics()
        char_width = font_metrics.horizontalAdvance('X')
        self.list_widget.setMinimumWidth(char_width * 20)

        # Set initial size for image viewer
        self.graphics_view.setMinimumSize(800, 600)

        # Toolbar
        self.toolbar = self.addToolBar("Tools")
        self.zoom_in_btn = QPushButton('+')
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.toolbar.addWidget(self.zoom_in_btn)

        self.zoom_out_btn = QPushButton('-')
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        self.toolbar.addWidget(self.zoom_out_btn)

        self.zoom_auto_btn = QPushButton('Fit')
        self.zoom_auto_btn.clicked.connect(self.zoom_auto)
        self.toolbar.addWidget(self.zoom_auto_btn)

        # Status Bar
        self.status_bar = self.statusBar()

        # Layouts
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.list_widget)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.graphics_view)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        
        # Using QSplitter for adjustable width
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.list_widget)
        splitter.addWidget(self.graphics_view)
        self.setCentralWidget(splitter)


    def showDialogOpenFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', os.getenv('HOME'), "Images (*.jpg *.png)")

        if fname[0]:
            self.load_image_file(fname[0])

    def showDialogOpenFolder(self):
        dname = QFileDialog.getExistingDirectory(self, 'Select Folder', os.getenv('HOME'), QFileDialog.ShowDirsOnly)

        if dname:
            self.load_folder(dname)

    def load_folder(self, folder_path):
        self.list_widget.clear()
        self.image_files = []

        for file in os.listdir(folder_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.list_widget.addItem(file)
                self.image_files.append(os.path.join(folder_path, file))

    def load_image_file(self, file_path, scale=1):
        self.current_file_path = file_path
        self.status_bar.showMessage("Loading image...")
        pixmap = QPixmap(file_path)
        if scale > 0:
            pixmap = pixmap.scaled(pixmap.width() * scale, pixmap.height() * scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        item = QGraphicsPixmapItem(pixmap)
        self.scene.clear()
        self.scene.addItem(item)
        self.graphics_view.setScene(self.scene)
        if scale <= 0:
            self.zoom_auto()
        self.status_bar.showMessage("Image loaded")



    def load_image(self, item):
        index = self.list_widget.row(item)
        file_path = self.image_files[index]
        self.load_image_file(file_path, -1)

    def zoom_in(self):
        self.current_scale *= 1.2
        self.load_image_file(self.current_file_path, self.current_scale)

    def zoom_out(self):
        self.current_scale *= 1 / 1.2
        self.load_image_file(self.current_file_path, self.current_scale)

    def zoom_auto(self):
        self.graphics_view.fitInView(self.scene.itemsBoundingRect(), mode=Qt.KeepAspectRatio)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageBrowser()
    window.show()
    sys.exit(app.exec_())