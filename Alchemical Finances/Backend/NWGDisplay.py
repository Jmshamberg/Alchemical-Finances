import sys
import sqlite3
import numpy as np

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFrame, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor

from sqlite3 import Error

from Backend.Graphing import AF_Canvas, net_worth_line_graph
from Backend.UPK import set_font, cash_format
from Frontend.NetworthUi import Ui_Dialog


class NetWorthGraph(QDialog):
    remove_tab_NWG = QtCore.pyqtSignal(str)

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self, parent, database):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.refUserDB = database
        self.ui.labelTest.setText("Hello")

        self.graphTitle = QLabel(self)
        self.graphTitle.setGeometry(450, 30, 350, 30)
        self.graphTitle.setText("Account Net Worth over Time")
        titleFont = QtGui.QFont()
        set_font(titleFont, 24, True, 65, False)
        self.graphTitle.setFont(titleFont)

        # --- Creation and Insertion of Graph ----------------------------------------------------------------------------
        self.lgraphCanvas = AF_Canvas(self, width=5, height=4, dpi=400)
        self.lgFrame = QFrame(self)
        self.lgFrame.setGeometry(50, 50, 1100, 600)
        self.lgFrame.setMaximumWidth(1100)
        self.lgFrame.setFrameStyle(0)

        self.lgLayout = QVBoxLayout(self.lgFrame)
        self.lgLayout.addWidget(self.lgraphCanvas)
        self.update_lg_plot(self.lgraphCanvas)

        self.grossLegend = QLabel(self)
        # add 70 to the x-axis value from where the rectangle starts
        # subtract 7 from the y-axis value
        self.grossLegend.setGeometry(415, 640, 100, 25)
        self.grossLegend.setText("Gross Worth")
        legendFont = QtGui.QFont()
        # set_font(target, size=int, bold=bool, weight=int, underline=bool)
        set_font(legendFont, 12, False, 65, False)
        self.grossLegend.setFont(legendFont)

        self.netLegend = QLabel(self)
        self.netLegend.setGeometry(590, 640, 100, 25)
        self.netLegend.setText("Net Worth")
        self.netLegend.setFont(legendFont)

        self.liabilityLegend = QLabel(self)
        self.liabilityLegend.setGeometry(755, 640, 125, 25)
        self.liabilityLegend.setText("Active Liabilities")
        self.liabilityLegend.setFont(legendFont)

        self.peakvalues = self.obtainPeakValues()
        # obtaining dates & value for peak Gross and Net Worth
        self.peakgross = QLabel(self)
        dataFont = QtGui.QFont()
        set_font(dataFont, 12, False, 65, False)
        self.peakgross.setGeometry(80, 680, 510, 25)
        self.peakgross.setFont(dataFont)

        self.mingross = QLabel(self)
        self.mingross.setGeometry(610, 680, 510, 25)
        self.mingross.setFont(dataFont)

        self.peaknet = QLabel(self)
        self.peaknet.setGeometry(80, 705, 510, 25)
        self.peaknet.setFont(dataFont)

        self.minnet = QLabel(self)
        self.minnet.setGeometry(610, 705, 510, 25)
        self.minnet.setFont(dataFont)

        self.peakliability = QLabel(self)
        self.peakliability.setGeometry(80, 730, 510, 25)
        self.peakliability.setFont(dataFont)

        self.minliability = QLabel(self)
        self.minliability.setGeometry(610, 730, 510, 25)
        self.minliability.setFont(dataFont)

        self.peakgross.setText(f"Peak Gross Worth         Date: {self.peakvalues[0][0]}    Value: {self.peakvalues[0][1]}")
        self.mingross.setText(f"Low Gross Worth        Date: {self.peakvalues[0][2]}    Value: {self.peakvalues[0][3]}")
        self.peaknet.setText(f"Peak Net Worth            Date: {self.peakvalues[1][0]}    Value: {self.peakvalues[1][1]}")
        self.minnet.setText(f"Low Net Worth           Date: {self.peakvalues[1][2]}    Value: {self.peakvalues[1][3]}")
        self.peakliability.setText(f"Peak Liabilities Worth    Date: {self.peakvalues[2][0]}    Value: {self.peakvalues[2][1]}")
        self.minliability.setText(f"Low Liabilities Worth   Date: {self.peakvalues[2][2]}    Value: {self.peakvalues[2][3]}")

        self.PeakFrame = QFrame(self)
        self.PeakFrame.setGeometry(74, 678, 516, 79)
        self.PeakFrame.setMaximumWidth(520)
        self.PeakFrame.setFrameStyle(1)

        self.minFrame = QFrame(self)
        self.minFrame.setGeometry(604, 678, 516, 79)
        self.minFrame.setMaximumWidth(520)
        self.minFrame.setFrameStyle(1)

        self.ui.labelTest.hide()
        self.show()

    def update_lg_plot(self, canvas):
        lg_data = net_worth_line_graph(database=self.refUserDB)

        # [X-axis, Y1-axis = gross, Y2-axis = liability, Y3-axis = net, x-interval, y_interval, y-max, y-axis units, y1-Fill, y2-Fill, y3-Fill]
        canvas.axes.clear()
        canvas.axes.plot(lg_data[0], lg_data[1], color='#000000', linewidth=0.55)  # Gross
        canvas.axes.plot(lg_data[0], lg_data[3], color='#000000', linewidth=0.55)  # Net
        canvas.axes.plot(lg_data[0], lg_data[2], color='#000000', linewidth=0.55)  # Liability

        canvas.axes.fill_between(lg_data[0], lg_data[8], lg_data[3], color='#275929')  # Gross-Net
        canvas.axes.fill_between(lg_data[0], lg_data[10], lg_data[2], color='#38803B')  # Net-Liability
        canvas.axes.fill_between(lg_data[0], lg_data[9], y2=0, color='#803838')        # Liability-O

        x_points = np.arange(0, len(lg_data[0]), lg_data[4])
        x_labels = [lg_data[0][x] for x in x_points]
        canvas.axes.set_xticks(x_points)
        canvas.axes.set_xticklabels(x_labels, ha='left')
        canvas.axes.set_yticks(np.arange(0, lg_data[6] + 10, lg_data[5]))

        canvas.axes.minorticks_on()
        canvas.axes.tick_params(axis='y', which='major', labelsize='3', grid_alpha=1, width=0.5)
        canvas.axes.tick_params(axis='y', which='minor', width=0.25)
        canvas.axes.tick_params(axis='x', which='major', labelsize='3', pad=2.0, width=0.5)
        canvas.axes.tick_params(axis='x', which='minor', bottom=False, width=0.25)

        canvas.axes.set_ylim(bottom=0)
        canvas.axes.set_xlim(left=0, right=len(lg_data[0]))
        canvas.axes.set_xlabel('Date (YYYY/MM/DD) ', labelpad=3, size='3')
        canvas.axes.set_ylabel(f'$ ({lg_data[7]})', labelpad=3, size='3')

        canvas.axes.grid(b=True,
                         which='major',
                         axis='y',
                         color='0.10',
                         linestyle='-',
                         linewidth='0.4')

        canvas.axes.grid(b=True,
                         which='minor',
                         axis='y',
                         color='0.35',
                         linestyle='-',
                         linewidth='0.2')

        # canvas.axes.legend(['Gross', 'Net', 'Liability'],
        #                    loc=6,
        #                    bbox_to_anchor=(0.05, 0.25),
        #                    markerscale=3.0,
        #                    fontsize='3',)

        pos = [0.11, 0.15, 0.85, 0.80]
        canvas.axes.set_position(pos, which='both')
        canvas.draw()

    def paintEvent(self, event):
        manual_legend = QPainter()
        manual_legend.begin(self)
        self.drawRectangle(manual_legend)
        manual_legend.end()

    def drawRectangle(self, target_object):
        color = QColor(0, 0, 0)
        color.setNamedColor('#000000')
        target_object.setPen(color)

        target_object.setBrush(QColor(39, 89, 41))
        target_object.drawRect(345, 645, 50, 12)

        target_object.setBrush(QColor(56, 128, 59))
        target_object.drawRect(520, 645, 50, 12)

        target_object.setBrush(QColor(128, 56, 56))
        target_object.drawRect(685, 645, 50, 12)

    def obtainPeakValues(self):
        statement = "SELECT * FROM NetWorth"
        # Date, Gross, Liabilities, Net
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(statement)
                row = cur.fetchall()
        except Error:
            print("Error: NWGDisplay 161")
        finally:
            conn.close()

            row.sort(key=lambda tup: (tup[1], tup[0]), reverse=True)
            grosspeakformat = cash_format(float(row[0][1]), 2)
            grossminformat = cash_format(float(row[-1][1]), 2)
            gross = [row[0][0], str(grosspeakformat[1]), row[-1][0], str(grossminformat[1])]

            row.sort(key=lambda tup: (tup[3], tup[0]), reverse=True)
            netpeakformat = cash_format(float(row[0][3]), 2)
            netminformat = cash_format(float(row[-1][3]), 2)
            net = [row[0][0], str(netpeakformat[1]), row[-1][0], str(netminformat[1])]

            row.sort(key=lambda tup: (tup[2], tup[0]), reverse=True)
            liabilitypeakformat = cash_format(float(row[0][2]), 2)
            liabilitypeakdate = row[0][0]
            row.sort(key=lambda tup: (tup[2], tup[0]), reverse=False)
            liabilityminformat = cash_format(float(row[0][2]), 2)
            liability = [liabilitypeakdate, str(liabilitypeakformat[1]), row[0][0], str(liabilityminformat[1])]

            peakdata = (gross, net, liability)
            # print(peakdata)
            return peakdata

    def trigger_del_tab(self):
        self.remove_tab_NWG.emit("NWG")

    def closeEvent(self, event):
        event.ignore()
        self.trigger_del_tab()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    lily = NetWorthGraph()
    lily.show()
    sys.exit(app.exec_())