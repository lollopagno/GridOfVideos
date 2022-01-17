from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QStyle, QApplication, \
    QFileDialog, QLabel, QFormLayout
from PySide6.QtCore import QDir, Slot
from PySide6.QtGui import QIntValidator
from PySide6 import QtGui

import os
import cv2 as cv
from utility import stackImages, getRandomImageGray, checkIfAllNone

ESCAPE = 27
TAB = 9
SPACE = 32


class GridGui(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.name_window_test = "Test"
        self.name_windom_main = "Grid of videos"

        # Flag window
        self._isTestWindowCreated = False
        self._isMainWindowsCreated = False

        self._isStartingVideo = False

        # Size video
        self._height = None
        self._width = None

        # Rows and columns of the table
        self._rows = None
        self._columns = None

        # Manage videos
        self._path = None
        self._videos = []

        # Button
        self._start_button = QPushButton("Start")
        self._test_button = QPushButton("Test")

        # Label
        self._height_label = QLabel()
        self._height_label.setText("Altezza:")

        self._width_label = QLabel()
        self._width_label.setText("Larghezza:")

        self._rows_label = QLabel()
        self._rows_label.setText("Righe:")

        self._columns_label = QLabel()
        self._columns_label.setText("Colonne:")

        self._folder_label = QLabel()
        self._folder_label.setText("Cartella:")

        self._size_video_label = QLabel()
        self._size_video_label.setText("Risoluzione:")

        # Line edit
        self._height_box = QLineEdit()
        self._height_box.setValidator(QIntValidator())
        self._height_box.setMaxLength(3)
        self._height_box.textChanged.connect(self.on_change_height)

        self._width_box = QLineEdit()
        self._width_box.setValidator(QIntValidator())
        self._width_box.setMaxLength(3)
        self._width_box.textChanged.connect(self.on_change_width)

        self._rows_box = QLineEdit()
        self._rows_box.setValidator(QIntValidator())
        self._rows_box.setMaxLength(2)
        self._rows_box.textChanged.connect(self.on_change_rows)

        self._columns_box = QLineEdit()
        self._columns_box.setValidator(QIntValidator())
        self._columns_box.setMaxLength(2)
        self._columns_box.textChanged.connect(self.on_change_columns)

        self._folder_box = QLineEdit()

        self._open_folder_action = self._folder_box.addAction(QApplication.style().standardIcon(QStyle.SP_DirOpenIcon),
                                                              QLineEdit.TrailingPosition)
        self._open_folder_action.triggered.connect(self.on_open_folder)

        # Form layout
        form = QFormLayout()
        form.addRow(self._height_label, self._height_box)
        form.addRow(self._width_label, self._width_box)
        form.addRow(self._rows_label, self._rows_box)
        form.addRow(self._columns_label, self._columns_box)
        form.addRow(self._folder_label, self._folder_box)

        # Buttons layout
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(self._start_button)
        buttonsLayout.addWidget(self._test_button)

        # Main layout
        vlayout = QVBoxLayout(self)
        vlayout.addLayout(form)
        vlayout.addStretch()
        vlayout.addLayout(buttonsLayout)

        self.resize(400, 150)
        self.setWindowTitle("Videos")
        self.setWindowIcon(QtGui.QIcon("resources/icon.jpg"))

        self._start_button.clicked.connect(self.on_start)
        self._test_button.clicked.connect(self.on_test)

    @Slot()
    def on_open_folder(self):
        self.destroyWindow()
        dir_path = QFileDialog.getExistingDirectory(self, "Open Directory", QDir.homePath(), QFileDialog.ShowDirsOnly)

        if dir_path:
            self._path = QDir(dir_path)
            self._folder_box.setText(QDir.fromNativeSeparators(self._path.path()))
        else:
            self._path = None

        if self._path:
            print(f"[SETTING PATH] {self._path.path()}")

    @Slot()
    def on_change_height(self):
        self.destroyWindow()
        text = self._height_box.text()

        self._height = None
        if text:
            number = int(text)
            if number != 0:
                self._height = number

        print(f"[ON CHANGE HEIGHT]: {self._height}")

    @Slot()
    def on_change_width(self):
        self.destroyWindow()
        text = self._width_box.text()

        self._width = None
        if text:
            number = int(text)
            if number != 0:
                self._width = number

        print(f"[ON CHANGE WIDTH]: {self._width}")

    @Slot()
    def on_change_rows(self):
        self.destroyWindow()
        text = self._rows_box.text()

        self._rows = None
        if text:
            number = int(text)
            if number != 0:
                self._rows = number

        print(f"[ON CHANGE ROWS]: {self._rows}")

    @Slot()
    def on_change_columns(self):
        self.destroyWindow()
        text = self._columns_box.text()

        self._columns = None
        if text:
            number = int(text)
            if number != 0:
                self._columns = number

        print(f"[ON CHANGE COLUMNS]: {self._columns}")

    @Slot()
    def on_start(self):
        """
        Event start button
        """

        if self._rows and self._columns and self._path and self._height and self._width:
            print("On Start")

            self._videos = os.listdir(self._path.path())
            num_videos = self._rows * self._columns

            if len(self._videos) >= num_videos:

                self._isMainWindowsCreated = True
                counter = 0

                # Initialization grid
                grid = [None for _ in range(0, self._columns)]
                capture = [None for _ in range(0, num_videos)]

                for column in range(0, self._columns):
                    grid_row = [None for _ in range(0, self._rows)]
                    dim = (self._width, self._height)

                    for row in range(0, self._rows):
                        cap = cv.VideoCapture(self._path.path() + "/" + self._videos[counter])

                        if cap.grab():
                            print(f"Load video: {self._videos[counter]}")
                            grid_row[row] = cv.resize(cap.retrieve()[1], dim)
                            capture[counter] = cap
                        else:
                            windows = getRandomImageGray(dim)
                            grid_row[row] = cv.resize(windows, dim)
                            capture[counter] = None
                        counter += 1

                    grid[column] = grid_row

                while True:
                    cv.namedWindow(self.name_windom_main)
                    stack = stackImages(1, grid)
                    cv.imshow(self.name_windom_main, stack)
                    key = cv.waitKey(1)

                    if key == ESCAPE:
                        self.destroyWindow()
                        break

                    elif key == SPACE:

                        if self._isStartingVideo:
                            self._isStartingVideo = False
                            break

                        elif not self._isStartingVideo:
                            self._isStartingVideo = True
                            ret = self.run(grid, capture)

                            if checkIfAllNone(capture) or ret:
                                self.destroyWindow()
                                break

                            grid = self.getNextFrame(grid, capture)

    def run(self, grid, capture):
        """
        Run videos.
        """

        result = False
        while self._isMainWindowsCreated:

            if checkIfAllNone(capture):
                self.destroyWindow()
                break

            grid = self.getNextFrame(grid, capture)

            stack = stackImages(1, grid)
            cv.imshow(self.name_windom_main, stack)
            key = cv.waitKey(25)

            if key == ESCAPE:
                self.destroyWindow()
                result = True
                break

            elif key == SPACE:

                if self._isStartingVideo:
                    self._isStartingVideo = False
                    break

        return result

    def getNextFrame(self, grid, capture):
        """
        Get next frame from all videos.
        """

        counter = 0
        for column in range(0, self._columns):
            grid_row = [None for _ in range(0, self._rows)]

            for row in range(0, self._rows):
                cap = capture[counter]
                dim = (self._width, self._height)
                if cap:
                    if cap.grab():
                        grid_row[row] = cv.resize(cap.retrieve()[1], dim)
                        capture[counter] = cap
                    else:
                        cap = cv.VideoCapture(self._path.path() + "/" + self._videos[counter])
                        if cap.grab():
                            grid_row[row] = cv.resize(cap.retrieve()[1], dim)
                            capture[counter] = cap
                        else:
                            window = getRandomImageGray(dim)
                            grid_row[row] = cv.resize(window, dim)
                            capture[counter] = None
                else:
                    window = getRandomImageGray(dim)
                    grid_row[row] = cv.resize(window, dim)
                    capture[counter] = None

                counter += 1

            grid[column] = grid_row

        return grid

    @Slot()
    def on_test(self):
        """
        Event test button
        """

        if self._rows and self._columns and self._width and self._height:
            print("On Test")
            self._isTestWindowCreated = True

            while self._isTestWindowCreated:
                grid = [None for _ in range(0, self._columns)]

                for column in range(0, self._columns):
                    grid_row = [None for _ in range(0, self._rows)]

                    dim = (self._width, self._height)

                    for row in range(0, self._rows):
                        windows = getRandomImageGray(dim)
                        grid_row[row] = cv.resize(windows, dim)

                    grid[column] = grid_row

                stack = stackImages(1, grid)

                cv.namedWindow(self.name_window_test)
                cv.imshow(self.name_window_test, stack)
                key = cv.waitKey(25)

                if key == ESCAPE:
                    self.destroyWindow()

    def destroyWindow(self):
        """
        Destroy windows.
        """

        try:
            cv.destroyAllWindows()
            self._isTestWindowCreated = False
            self._isMainWindowsCreated = False
        except:
            pass
