#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

import sys
from PySide.QtGui import QApplication
from biopredyn.ui.mainwindow import MainWindow

app = QApplication(sys.argv)
frame = MainWindow()
frame.show()
sys.exit(app.exec_())
