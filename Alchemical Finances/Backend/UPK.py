# File was original planned to solely Generate "Secret" user profile key.
# Currently houses multi-use functions across different files

import secrets
import sqlite3

from pathlib import Path
from sqlite3 import Error

from PyQt5.QtWidgets import QTableWidgetItem, QInputDialog
from PyQt5.QtGui import QColor
from PyQt5 import QtCore, QtGui


# --- Set Database Pathways -----------------------------------------------------------------------------------------
def account_pathway(name):
    name = str(name)
    desired_dir = Path.cwd() / 'data' / 'account'
    desired_dir.mkdir(parents=True, exist_ok=True)
    desired_pathway = 'data/account/' + name
    desired_pathway_str = str(desired_pathway)
    pathList = [desired_pathway, desired_pathway_str]
    return pathList


def receipt_pathway(parentType, ledger, fileName, user):
    parentType = str(parentType)
    modifiedLN = modify_for_sql(ledger)
    fileName = str(fileName)
    target_dir = Path.cwd() / 'Receipts' / user / parentType / modifiedLN
    target_dir.mkdir(parents=True, exist_ok=True)
    receipt_destination = 'Receipts/' + user + '/' + parentType + '/' + modifiedLN + '/' + fileName
    return receipt_destination


def directory_pathway(parentType, ledger, user):
    parentType = str(parentType)
    modifiedLN = modify_for_sql(ledger)
    target_dir = Path.cwd() / 'Receipts' / user / parentType / modifiedLN
    target_dir_string = str(target_dir)
    return target_dir_string


# --- Image Pathway ------------------------------------------------------------------------------------------------
# def image_pathway(parentType, name):
# name = str(name)
# desired_dir = Path.cwd() / 'data' / 'images' / parentType
# desired_dir.mkdir(parents=True, exist_ok=True)
# desired_pathway = 'data/images/' + parentType + '/' + name
# desired_pathway_str = str(desired_pathway)
# return desired_pathway_str


# --- Generates a 7 Digit User ID ----------------------------------------------------------------------------------
def generate_key():
    numberSecret = ""
    numberSecretList = []
    countDown = 7
    while countDown > 0:
        numberSecretList.append(secrets.randbelow(10))
        countDown -= 1
    for num in numberSecretList:
        numberSecret = numberSecret + str(num)
    return numberSecret


# --- Prevents Use of Non Alphanumeric characters ------------------------------------------------------------------
# def check_characters_login(question):
#     checkString = question
#     x = 0
#     badCharacters = ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "=", ":",
#                      "+", "<", "?", ";", "'", "[", "]", "{", "}", '"', "-", ".", ","]
#     for piece in checkString:
#         if piece in badCharacters:
#             x += 1
#         else:
#             pass
#     if x >= 1:
#         return False
#     if x == 0:
#         return True


def check_characters(question, focus):
    checkString = question
    x = 0
    focus_dic = {
        "login": ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "=", ":",
                  "+", "<", "?", ";", "'", "[", "]", "{", "}", '"', "-", ".", ","],
        "general": ["~", "!", "@", "#", "$", "%", "^", "*", "(", ")", "=",
                    "+", "<", "?", ";", "[", "]", "{", "}", '"', "'"],
        "monetary": ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "=", ":",
                     "+", "<", "?", ";", "'", "[", "]", "{", "}", '"', "-", ","],
    }

    badCharacters = focus_dic[focus]

    # goodCharacters = [",", ".", "-", ":", "&"]
    for piece in checkString:
        if piece in badCharacters:
            x += 1
        else:
            pass
    if x >= 1:
        return False
    if x == 0:
        return True


# --- Modifies a ledger name for SQL use ---------------------------------------------------------------------------
def modify_for_sql(tableName):
    modifiedTN = ""
    for letter in tableName:
        if letter == " ":
            modifiedTN += "_"
        else:
            modifiedTN += letter
    return modifiedTN


# --- Check Username for blank spaces ---------------------------------------------------------------------------
def spacing_check(uservalue):
    username = uservalue
    for letter in username:
        if letter == " ":
            return False
        else:
            pass
    return True


# --- Ensures a non-blank input ------------------------------------------------------------------------------------
def find_character(userValue):
    accountName = userValue
    validCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    letterCount = 0
    for letter in accountName:
        if letter.capitalize() in validCharacters:
            letterCount += 1
        else:
            pass
    if letterCount > 0:
        return True
    else:
        return False


# --- -- Input Dialog to obtain which row to select // Select//Update//Delete --------------------------------------
def user_selection_input(self, tableWidget, text1, text2):
    row, ok = QInputDialog.getInt(self, text1, text2, 1, 1, tableWidget.rowCount(), 1)
    if ok and row:
        return row
    else:
        row = 0
        return row


# --- Checks the first character to ensure it is a letter ----------------------------------------------------------
def first_character_check(userValue):
    tableName = userValue
    validCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if tableName[0].capitalize() in validCharacters:
        return True
    else:
        return False


# --- SQL Functions ------------------------------------------------------------------------------------------------
def specific_sql_statement(statement, database):
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(statement)
    except Error:
        print("Error: 134")
    finally:
        conn.close()


def obtain_sql_value(statement, database):
    rValue = ""
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(statement)
            value = cur.fetchone()
            rValue = value
    except Error:
        rValue = None
        print("Error UPK: 149")
        return rValue
    finally:
        conn.close()
        return rValue


def obtain_sql_list(statement, database):
    rValue = ""
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(statement)
            value = cur.fetchall()
            rValue = value
    except Error:
        print("Error UPK: 165")
    finally:
        conn.close()
        return rValue


# --- Restore Account to active status -----------------------------------------------------------------------------
def switch_sql_tables(destination, origin, identifier, target, database):
    insert_statement = "INSERT INTO " + destination + " SELECT * FROM " + origin + " WHERE " + identifier + "= '" + target + "'"
    delete_statement = "DELETE FROM " + origin + " WHERE " + identifier + "= '" + target + "'"
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(insert_statement)
            cur.execute(delete_statement)
    except Error:
        print("Error: UPK 178")
    finally:
        conn.close()


# --- Net Worth Function --- Obtain Value from Account Summary Page ------------------------------------------------
def set_networth(tablename, database, toggleformatting):
    qtyAssetStatement = "SELECT SUM(Balance) FROM " + tablename + " WHERE ItemType='Asset'"
    qtyLiabilityStatement = "SELECT SUM(Balance) FROM " + tablename + " WHERE ItemType='Liability'"  # AND ParentType='Debt'"
    qtyMoney = obtain_sql_value(qtyAssetStatement, database)
    if qtyMoney[0] is None:
        qtyMoney = "0.00"
    else:
        qtyMoney = qtyMoney[0]

    qtyDebt = obtain_sql_value(qtyLiabilityStatement, database)
    if qtyDebt[0] is None:
        qtyDebt = "0.00"
    else:
        qtyDebt = qtyDebt[0]

    decimal_assets = decimal_places(qtyMoney, 2)
    decimal_debt = decimal_places(qtyDebt, 2)
    netMoney = decimal_assets - decimal_debt

    string_assets = cash_format(decimal_assets, 2)
    string_debt = cash_format(decimal_debt, 2)
    string_net = cash_format(netMoney, 2)

    if toggleformatting == 0:
        moneyList = [string_net[0], string_net[1], string_assets[1], string_debt[1]]
    elif toggleformatting == 1:
        moneyList = [string_assets[0], string_debt[0], string_net[0]]
    else:
        moneyList = ["0.00", "0.00", "0.00", "0.00"]

    return moneyList


# --- format balance for positive or negative --------------------------------------------------------------------------
def cash_format(value, deciplace):
    if value < 0:
        moneyWComma = add_comma(value, deciplace)
        moneyWOComma = "-" + remove_comma(moneyWComma)
        formatString = " ($  " + moneyWComma + ")"
        moneylist = [moneyWOComma, formatString]
        return moneylist
    if value == 0:
        moneyWOComma = "0.00"
        formatString = "  $  -  "
        moneylist = [moneyWOComma, formatString]
        return moneylist
    else:
        moneyWComnma = add_comma(value, deciplace)
        moneyWOComma = remove_comma(moneyWComnma)
        formatString = "  $  " + moneyWComnma + " "
        moneylist = [moneyWOComma, formatString]
        return moneylist


# --- method of formatting labels --------------------------------------------------------------------------------------
def set_font(target, size, bold, weight, underline):
    target.setPointSize(size)
    target.setBold(bold)
    target.setWeight(weight)
    target.setUnderline(underline)


# --- obtain 0.00 or 0.0000 value every time ---------------------------------------------------------------------------
def decimal_places(value, number):
    from decimal import Decimal
    if value == "" or value == " ":
        return value
    else:
        final = round(Decimal(value), number)
        return final


# --- Adds digit commas to values --------------------------------------------------------------------------------------
def add_comma(value, number):
    if value is None:
        value = 0.0
    if value < 0:
        num = 1
    else:  # value >= 0:
        num = 0

    value_as_string = str(value)
    split_value = value_as_string.split('.')

    try:
        split_value[1]
    except IndexError:
        split_value.append("00")

    qty_change_units = len(split_value[1])
    if qty_change_units > number:
        reduce_by = qty_change_units - number
        modified_change = split_value[1][:(qty_change_units - reduce_by)]
        new_value = split_value[0] + modified_change
    elif qty_change_units < number:
        increase_by = number - qty_change_units
        new_units = str(10 ** increase_by)
        new_value = split_value[0] + split_value[1] + new_units[1:]
    else:
        new_value = split_value[0] + split_value[1]

    value_as_string = new_value[num:]
    number_of_digits = len(value_as_string)
    value_of_change = value_as_string[number_of_digits - number:]
    value_of_bills = value_as_string[: number_of_digits - number]
    if len(value_of_bills) == 0:
        value_of_bills = "0"

    inverse_bills = value_of_bills[::-1]
    final_value = ""
    count = 0
    for digit in inverse_bills:
        if count == 0:
            final_value += digit
            count += 1
        elif count % 3 != 0:
            final_value += digit
            count += 1
        elif count % 3 == 0:
            final_value += "," + digit
            count += 1
    final_value = final_value[::-1] + "." + value_of_change
    return final_value


# --- Removes commas from a given value --------------------------------------------------------------------------------
def remove_comma(value):
    displayValue = ""
    for digit in value:
        if digit == ",":
            pass
        elif digit == "-":
            pass
        elif digit == ".":
            displayValue += digit
        else:
            displayValue += digit
    return displayValue


# --- Change Pending transaction Row Color -----------------------------------------------------------------------------
def setColortoRow(tablewidget, rowIndex, color):
    for j in range(0, 9):
        tablewidget.item(rowIndex, j).setBackground(color)


# --- obtain pending color ---------------------------------------------------------------------------------------------
def pending_row_color(value, pending):
    if value == "Pending" and pending == 0:
        pending = 1
    elif value == "Pending" and pending == 1:
        pending = 2
    elif value == "Pending" and pending == 2:
        pending = 1
    else:
        pending = 0
    return pending


# --- DISPLAY LEDGERS --------------------------------------------------------------------------------------------------
def disp_ledgerV1(combobox, tablewidget, database):
    from decimal import Decimal
    tablewidget.setRowCount(0)
    centered = [0, 3]
    ledgerName = combobox.currentText()
    balance = 0
    pending = 0
    if ledgerName == "":
        pass
    else:
        modifiedLN = modify_for_sql(ledgerName)
        sortTable = "SELECT Transaction_Date, Transaction_Method, Transaction_Description, Category, (Credit - Debit), 0, Status, Receipt, Note, Post_Date FROM {0} " \
                    " ORDER BY Transaction_Date ASC LIMIT 0, 49999".format(modifiedLN)
        # 0 - TDate 1 - TMeth 2 - TDesc 3 - Cat 4 - Amount 5 - balance 6 - Status - 7 - Receipt - 8 Notes - 9 Date
        try:
            conn = sqlite3.connect(database)
            with conn:
                cur = conn.cursor()
                cur.execute(sortTable)
                result = cur.fetchall()
                tablewidget.setColumnCount(11)
                for data in result:
                    cur_row = tablewidget.rowCount()
                    tablewidget.insertRow(cur_row)
                    sublist = data[:11]
                    for index, value in enumerate(sublist):
                        if index in centered:
                            item = QTableWidgetItem(value)
                            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                        elif index == 4:
                            balance += Decimal(value)
                            balance = decimal_places(balance, 2)
                            value = cash_format(value, 2)[1]
                            item = QTableWidgetItem(value)
                            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                        elif index == 5:
                            disp_balance = cash_format(balance, 2)[1]
                            item = QTableWidgetItem(disp_balance)
                            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                        elif index == 6:
                            item = QTableWidgetItem(value)
                            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                            if pending == 0 or pending == 2:
                                color = QColor(222, 239, 189)
                            elif pending == 1:
                                color = QColor(208, 232, 161)
                            pending = pending_row_color(value, pending)
                        else:
                            item = QTableWidgetItem(value)
                            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
                        tablewidget.setItem(cur_row, index, QTableWidgetItem(item))
                    if pending == 1 or pending == 2:
                        setColortoRow(tablewidget, cur_row, color)
                tablewidget.setHorizontalHeaderLabels(["Transaction Date",
                                                       "Transaction Method",
                                                       "Transaction Description",
                                                       "Category",
                                                       "Amount",
                                                       "Balance",
                                                       "Status",
                                                       "Receipt",
                                                       "Additional Transaction Notes",
                                                       "Posted Date",
                                                       "Updated Date"])
                tablewidget.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter)
                table_widths = [100, 135, 255, 70, 80, 80, 70, 150, 120]
                for column in range(0, 9, 1):
                    tablewidget.setColumnWidth(column, table_widths[column])
                tablewidget.setColumnHidden(9, True)
                tablewidget.setColumnHidden(10, True)
                tablewidget.resizeRowsToContents()
                tableFont = QtGui.QFont()
                tableFont.setPointSize(7)
                tablewidget.setFont(tableFont)
        except Error:
            print("error: 251")
        finally:
            conn.close()
            tablewidget.scrollToBottom()


def disp_ledgerV2(combobox, tablewidget, database):
    tablewidget.setRowCount(0)
    centered = [0, 2]
    ledgerName = combobox.currentText()
    pending = 0
    if ledgerName == "":
        pass
    else:
        modifiedLN = modify_for_sql(ledgerName)
        sortTable = "SELECT Transaction_Date, Transaction_Description, Category, (Credit - Debit), (Purchased - Sold), Price, Status, Receipt, Note," \
                    " Post_Date, Update_Date FROM {0} ORDER BY Transaction_Date ASC LIMIT 0, 49999".format(modifiedLN)
        # 0 - TDate 1 - TDes 2 - Cat 3 - Amount 4 - Shares 5 - Price 6 - Status - 7 - Receipt - 8 Notes - 9 Date
        try:
            conn = sqlite3.connect(database)
            with conn:
                cur = conn.cursor()
                cur.execute(sortTable)
                result = cur.fetchall()
                tablewidget.setColumnCount(11)
                for data in result:
                    cur_row = tablewidget.rowCount()
                    tablewidget.insertRow(cur_row)
                    sublist = data[:12]
                    for index, value in enumerate(sublist):
                        if index in centered:
                            item = QTableWidgetItem(value)
                            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                        elif index == 3:
                            value = cash_format(value, 2)[1]
                            item = QTableWidgetItem(value)
                            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                        elif index == 4:
                            value = decimal_places(value, 4)
                            item = QTableWidgetItem(str(value))
                            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                        elif index == 5:
                            value = cash_format(value, 4)[1]
                            item = QTableWidgetItem(value)
                            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                        elif index == 6:
                            item = QTableWidgetItem(value)
                            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                            if pending == 0 or pending == 2:
                                color = QColor(222, 239, 189)
                            elif pending == 1:
                                color = QColor(208, 232, 161)
                            pending = pending_row_color(value, pending)
                        else:
                            item = QTableWidgetItem(value)
                            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
                        tablewidget.setItem(cur_row, index, QTableWidgetItem(item))
                    if pending == 1 or pending == 2:
                        setColortoRow(tablewidget, cur_row, color)
                tablewidget.setHorizontalHeaderLabels(["Transaction Date",
                                                       "Transaction Description",
                                                       "Category",
                                                       "Amount",
                                                       "Shares (+/-)",
                                                       "Price/Share",
                                                       "Status",
                                                       "Receipt",
                                                       "Additional Transaction Notes",
                                                       "Posted Date",
                                                       "Updated Date"])
                tablewidget.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter)
                table_widths = [100, 255, 70, 80, 80, 80, 70, 150, 200]
                for column in range(0, 9, 1):
                    tablewidget.setColumnWidth(column, table_widths[column])
                tablewidget.setColumnHidden(9, True)
                tablewidget.setColumnHidden(10, True)
                tablewidget.resizeRowsToContents()
                tableFont = QtGui.QFont()
                tableFont.setPointSize(7)
                tablewidget.setFont(tableFont)
        except Error:
            print("error: 346")
        finally:
            conn.close()
            tablewidget.scrollToBottom()
