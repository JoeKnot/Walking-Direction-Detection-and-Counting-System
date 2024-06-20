import tkinter as tk
from tkinter import *
from ultralytics import YOLO
import cv2
from PyQt5 import *
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys, os

def window():
    app = QApplication()
    win = QMainWindow
    win.setGeometry(200,200,720,640)
    win.setWindowTitle("GUI")
    label = QtWidgets.QLabel(win)
    label.setText("Hi")

    win.show()
    sys.exit(app.exec_())

window()

