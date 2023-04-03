import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QAction, QFileDialog, QListWidget, QListWidgetItem, QCheckBox, QLineEdit, QPushButton


class ImageBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Browser")
        self.setWindowIcon(QIcon("icon.png"))

        # 创建界面元素
        self.file_list = QListWidget()
        self.menu_bar = self.menuBar()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.status_bar = self.statusBar()
        self.tool_bar = QWidget()
        self.tool_bar_layout = QVBoxLayout(self.tool_bar)
        self.tool_bar_layout.setAlignment(Qt.AlignTop)
        self.tool_bar.setFixedWidth(200)
        self.tool_bar.setContentsMargins(0, 0, 0, 0)

        # 创建菜单栏
        file_menu = self.menu_bar.addMenu("文件")
        open_action = QAction("打开", self)
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)

        open_folder_action = QAction("打开文件夹", self)
        open_folder_action.triggered.connect(self.open_folder_dialog)
        file_menu.addAction(open_folder_action)

        # 创建工具栏
        self.add_tool_button("关键点", self.show_key_points)
        self.add_tool_button("信息", self.show_info)
        self.add_tool_checkbox("显示网格", self.show_grid)
        self.add_tool_text_input("搜索", self.search)

                # 创建主界面布局
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("文件列表"))
        left_layout.addWidget(self.file_list)
        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(self.tool_bar_layout)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 初始化状态信息
        self.status_bar.showMessage("就绪")

        # 文件列表单击事件
        self.file_list.currentItemChanged.connect(self.show_selected_image)

        # 放大、缩小、适合窗口按钮
        self.add_tool_button("+", self.zoom_in)
        self.add_tool_button("-", self.zoom_out)
        self.add_tool_button("适合窗口", self.fit_window)

        # 图片缩放因子
        self.scale_factor = 1.0

        # 图片根目录
        self.current_folder_path = ""
        

    def add_tool_button(self, text, callback):
        button = QPushButton(text)
        button.clicked.connect(callback)
        self.tool_bar_layout.addWidget(button)

    def add_tool_checkbox(self, text, callback):
        checkbox = QCheckBox(text)
        checkbox.stateChanged.connect(callback)
        self.tool_bar_layout.addWidget(checkbox)

    def add_tool_text_input(self, placeholder, callback):
        text_input = QLineEdit()
        text_input.setPlaceholderText(placeholder)
        text_input.returnPressed.connect(lambda: callback(text_input.text()))
        self.tool_bar_layout.addWidget(text_input)

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "打开文件", ".", "Images (*.png *.xpm *.jpg)")
        if file_name:
            self.show_image(file_name)

    def open_folder_dialog(self):
        folder_name = QFileDialog.getExistingDirectory(self, "打开文件夹", ".")
        self.current_folder_path = folder_name
        if folder_name:
            self.load_folder_images(folder_name)

    def load_folder_images(self, folder_path):
        self.file_list.clear()
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".jpg") or file_name.endswith(".png"):
                self.file_list.addItem(QListWidgetItem(file_name))

        if self.file_list.count() > 0:
            self.file_list.setCurrentRow(0)
            self.show_image(os.path.join(folder_path, self.file_list.currentItem().text()))

    def show_image(self, file_path):
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.status_bar.showMessage("已加载文件：" + file_path)
        self.scale_factor = 1.0
        self.image_label.adjustSize()

    def show_selected_image(self, current_item, previous_item):
        if current_item is not None:
            file_path = os.path.join(self.current_folder_path, current_item.text())
            self.show_image(file_path)

    def show_key_points(self):
        # TODO: 显示关键点信息
        pass

    def show_info(self):
        # TODO: 显示关键点信息
        pass

    def show_grid(self, state):
        # TODO: 显示或隐藏网格
        pass

    def search(self, text):
        # TODO: 在文件列表中搜索文件
        pass

    def zoom_in(self):
        self.scale_image(1.25)

    def zoom_out(self):
        self.scale_image(0.8)

    def fit_window(self):
        self.image_label.adjustSize()
        self.scale_factor = 1.0

    def scale_image(self, factor):
        self.scale_factor *= factor
        self.image_label.setPixmap(self.image_label.pixmap().scaled(
            self.image_label.pixmap().size() * self.scale_factor,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation))
        self.image_label.adjustSize()

if __name__ == "__main__":
    app = QApplication([])
    browser = ImageBrowser()
    browser.show()
    app.exec_()
