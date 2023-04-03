import sys
import os
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QImageReader, QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QFileDialog, QGraphicsPixmapItem, \
                            QGraphicsScene, QMainWindow, QListWidget, QStatusBar, \
                            QAction, QSplitter, QGridLayout, QWidget, QVBoxLayout, QHBoxLayout, \
                            QGraphicsView, QToolBar, QPushButton, QCheckBox, QLineEdit

class ImageBrowserWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.current_scale = 1.0
        self.current_file_path = None

         # File List Widget
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.load_image)

        # Image Viewer
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        # Toolbar
        self.toolbar = QToolBar()

        # Add Open File and Open Folder buttons
        self.open_file_btn = QPushButton("Open File")
        self.open_file_btn.clicked.connect(self.showDialogOpenFile)
        self.toolbar.addWidget(self.open_file_btn)

        self.open_folder_btn = QPushButton("Open Folder")
        self.open_folder_btn.clicked.connect(self.showDialogOpenFolder)
        self.toolbar.addWidget(self.open_folder_btn)

        self.zoom_in_btn = QPushButton('+')
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.toolbar.addWidget(self.zoom_in_btn)

        self.zoom_out_btn = QPushButton('-')
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        self.toolbar.addWidget(self.zoom_out_btn)

        self.zoom_auto_btn = QPushButton('Fit')
        self.zoom_auto_btn.clicked.connect(self.zoom_auto)
        self.toolbar.addWidget(self.zoom_auto_btn)

        # Layout
        hbox = QHBoxLayout()

        # Add QSplitter for independent width adjustment
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.list_widget)
        splitter.addWidget(self.graphics_view)
        hbox.addWidget(splitter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.toolbar)
        main_layout.addLayout(hbox)

        # Status Bar
        self.status_bar = QStatusBar()
        main_layout.addWidget(self.status_bar)
        main_layout.setStretchFactor(self.toolbar, 0)
        main_layout.setStretchFactor(hbox, 1)
        main_layout.setStretchFactor(self.status_bar, 0)

        self.setLayout(main_layout)

        # Set initial width for file list
        font_metrics = self.list_widget.fontMetrics()
        char_width = font_metrics.horizontalAdvance('X')
        self.list_widget.setMinimumWidth(char_width * 20)

        # Set initial size for image viewer
        self.graphics_view.setMinimumSize(600, 300)

        # Set stretch factors for file list and graphics_view
        hbox.setStretchFactor(self.list_widget, 0)
        hbox.setStretchFactor(self.graphics_view, 1)

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
            pixmap = pixmap.scaled(pixmap.width() * scale, pixmap.height() * scale, 
                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
        self.status_bar.showMessage(f"Scale={self.current_scale}")

    def zoom_in(self):
        self.current_scale *= 1.2
        self.load_image_file(self.current_file_path, self.current_scale)
        self.status_bar.showMessage(f"Scale={self.current_scale}")


    def zoom_out(self):
        self.current_scale *= 1 / 1.2
        self.load_image_file(self.current_file_path, self.current_scale)
        self.status_bar.showMessage(f"Scale={self.current_scale}")

    def zoom_auto(self):
        self.graphics_view.fitInView(self.scene.itemsBoundingRect(), mode=Qt.KeepAspectRatio)
        self.status_bar.showMessage(f"Scale={self.current_scale}")


class ImageBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Image Browser')

        # Image Browser Widgets
        self.image_browser_widget1 = ImageBrowserWidget()
        self.image_browser_widget2 = ImageBrowserWidget()

        # Layout with QSplitter for adjustable height
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.image_browser_widget1)
        splitter.addWidget(self.image_browser_widget2)

        # Set stretch factors for widgets in splitter
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        container = QWidget()
        container_layout = QGridLayout()
        container_layout.addWidget(splitter, 0, 0)
        container_layout.setRowStretch(0, 1)
        container.setLayout(container_layout)
        self.setCentralWidget(container)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)


class ImageBrowserApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)

        self.main_window1 = QMainWindow()
        self.main_window1.setWindowTitle("Image Browser 1")
        self.image_browser_widget1 = ImageBrowserWidget()
        self.main_window1.setCentralWidget(self.image_browser_widget1)
        self.main_window1.show()

        self.main_window2 = QMainWindow()
        self.main_window2.setWindowTitle("Image Browser 2")
        self.image_browser_widget2 = ImageBrowserWidget()
        self.main_window2.setCentralWidget(self.image_browser_widget2)
        self.main_window2.show()


def main0():
    app = QApplication(sys.argv)
    window = ImageBrowser()
    window.show()
    sys.exit(app.exec_())

def main1():
    import sys
    app = ImageBrowserApp(sys.argv)
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Single window
    # main0() 
    # 2 windows
    main1()

