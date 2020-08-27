# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019, 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Handles editing a QComponent.

@author: Zlatko Minev, Dennis Wang
@date: 2020
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QTreeView, QAbstractItemView

class QTreeView_Base(QTreeView):

    """This class extends the `QTreeView` class."""

    def __init__(self, parent: QtWidgets.QWidget):
        """
        Args:
            parent (QtWidgets.QWidget): The widget
        """
        QTreeView.__init__(self, parent)
        QTimer.singleShot(200, self.style_me)
        self.expanded.connect(self.resize_on_expand)

    def style_me(self):
        """Style this widget"""
        # Also can do in the ui file, but doesn't always transalte for me for some reason
        self.header().show()
        self.setAutoScroll(False)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.setStyleSheet("""
QTreeView::branch {  border-image: url(none.png); }
        """)

    def autoresize_columns(self, max_width: int = 200):
        """
        Resize columns to content with maximum size.

        Args:
            max (int): Maximum window width (Default: 200)
        """
        # For TreeView: resizeColumnToContents
        # For TableView: resizeColumnsToContents

        columns = self.model().columnCount(None)
        for i in range(columns):
            self.resizeColumnToContents(i)
            width = self.columnWidth(i)
            if width > max_width:
                self.setColumnWidth(i, max_width)

    def resize_on_expand(self):
        """Resize when exposed."""
        self.resizeColumnToContents(0)