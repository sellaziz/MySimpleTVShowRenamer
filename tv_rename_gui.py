import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
from PyQt5.QtWidgets import QListWidget, QPushButton, QToolBar, QMenu, QMenuBar
from PyQt5.QtWidgets import QAction, QFileDialog
from PyQt5.QtCore import Qt
from renamer.find_new_name import find_rename
import logging
import os

_divider = "*"*150


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setAcceptDrops(True)
        

        mainLayout = QHBoxLayout()
        # self.photoViewer = ImageLabel()
        self.menuBar = QMenuBar()
        self.menu=QMenu("&File", self)
        self.menuBar.addMenu(self.menu)
        mainLayout.setMenuBar(self.menuBar)
        self._createActions()
        self.menu.addAction(self.openAction)
        self.openAction.triggered.connect(self.onOpenClick)
        self.menu.addAction(self.exitAction)
        self.exitAction.triggered.connect(self.close)
        self.list1=QListWidget()
        mainLayout.addWidget(self.list1)
        self.button=QPushButton()
        self.button.setText("-->")
        self.button.clicked.connect(self.onLaunchClick)
        mainLayout.addWidget(self.button)
        self.list2=QListWidget()
        mainLayout.addWidget(self.list2)

        self.setLayout(mainLayout)
    
    def onOpenClick(self):
        fname=QFileDialog.getOpenFileName(self, 'Open File', '.')
        self.list1.addItem(fname[0])


    def rename(self, filenames,
            dry_run,
            ):
        group_dict, sort_dict, ep_dicts, final_dict = find_rename(filenames)
        # final_dicts = {Best_matched_name: {filename:{Season=int,Episode=int, new_name = str()}}}
        logging.debug(final_dict)
        files=[]
        for file in filenames:
            for best_match in final_dict.keys():
                print(best_match)
                try :
                    files.append(final_dict[best_match][file]['new_name'])
                except:
                    # TODO Case To handle
                    print()
        # for best_match in final_dict.keys():
        #     logging.info(_divider)
        #     logging.info(f"Show : {best_match}")
        #     for filename in final_dict[best_match].keys():
        #         for key, item in group_dict.items():
        #                 for elements in item:
        #                     old_filename, extension = elements
        #                     if filename==old_filename:
        #                         ext=extension
        #         new_name = final_dict[best_match][filename]['new_name']+"."+ext
        #         logging.info(
        #             f"{filename: <65} --> {new_name: <75}")
        #     if not dry_run:
        #         for filename in final_dict[best_match].keys():
        #             ext=None
        #             for key, item in group_dict.items():
        #                 for elements in item:
        #                     old_filename, extension = elements
        #                     if filename==old_filename:
        #                         ext=extension
        #             os.rename(filename, final_dict[best_match][filename]['new_name']+"."+ext)
        return files

    def onLaunchClick(self):
        items = []
        for x in range(self.list1.count()):
            items.append(self.list1.item(x).text())
        print(items)
        logging.basicConfig(level=logging.DEBUG)
        items_relative = [os.path.basename(abs_path) for abs_path in items]
        new_names = self.rename(items_relative, True)
        self.list2.clear()
        for new_name in new_names:
            self.list2.addItem(new_name)




        


    def _createActions(self):
        # Creating actions using the second constructor
        self.openAction = QAction("&Open...", self)
        self.exitAction = QAction("&Exit", self)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
        # if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
        # if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.list1.addItem(file_path)
            # self.set_image(file_path)

            event.accept()
        else:
            event.ignore()

    # def set_image(self, file_path):
    #     self.photoViewer.setPixmap(QPixmap(file_path))

app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())