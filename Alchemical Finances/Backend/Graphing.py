import os

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import cm
from numpy import linspace
from Backend.UPK import obtain_sql_value, obtain_sql_list, decimal_places
from calendar import month_name
from math import ceil
from cycler import cycler


class AF_Canvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, facecolor="#f5fbef"):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor=facecolor)
        self.axes = fig.add_subplot(111)
        super(AF_Canvas, self).__init__(fig)


class Generate_Bar_chart:
    def __init__(self, request):
        super().__init__()

        plt.title('Account:  {1} \n Category:  {0} \n Year:  {2}'.format(request[2], request[1], request[3]))
        plt.ylabel('Dollars ($)')
        plt.xlabel('Month')
        positions = range(1,13)
        months = [month_name[x] for x in range(1, 13)]

        raw_monthly_data = []
        refined_monthly_data = []

        for month in range(1, 13):
            if month <= 9:
                month = '0' + str(month)
            else:
                pass
            statement = "SELECT sum(Credit - Debit) FROM {0} WHERE Category='{1}' AND Transaction_Date LIKE '%{2}/{3}/%'".format(request[1], request[2], request[3], month)
            data_point = obtain_sql_value(statement, request[0])
            data_point = data_point[0]
            raw_monthly_data.append(data_point)

        for value in raw_monthly_data:
            if value is None:
                refined_monthly_data.append(0)
            else:
                if value < 0:
                    value = -value
                refined_monthly_data.append(value)

        sorted_monthly_data = [x for x in refined_monthly_data]
        sorted_monthly_data.sort()

        highest_point = int(sorted_monthly_data[-1])

        step_value = None

        if highest_point < 0:
            highest_point += 100
        elif highest_point <= 0:
            highest_point = 0

        plt.yticks(range(0, highest_point, step_value))
        plt.xticks(positions, months, rotation=90)
        plt.bar(positions, refined_monthly_data, width=0.35, align='center')
        plt.show()


# def net_worth_line_graph(database):
#     # SQL raw data acquisition
#     combined_data_statement = "SELECT * FROM NetWorth ORDER BY Date ASC LIMIT 0, 49999"
#     combined_data_tuple = obtain_sql_list(combined_data_statement, database)
#     largest_value_statement = "SELECT Max(Gross) FROM NetWorth"
#     largest_y_value = obtain_sql_value(largest_value_statement, database)
#     largest_y_value = int(float(largest_y_value[0]))
#
#     # placeholder lists and
#     x_date = []
#     y1_gross = []
#     y2_liability = []
#     y3_net = []
#     divisor = 0
#     designation = ""
#
#     # determines the divisor for the y-axis.
#     if largest_y_value >= 1000000:
#         divisor = 10000
#         designation = "ten thousands"
#     elif largest_y_value >= 100000:
#         divisor = 1000
#         designation = "thousands"
#     elif largest_y_value >= 10000:
#         divisor = 100
#         designation = "hundreds"
#     elif largest_y_value >= 1000:
#         divisor = 10
#         designation = "tens"
#     elif largest_y_value < 1000:
#         divisor = 0
#         designation = "dollars"
#
#     # separates the SQL data into their appropriate axis designations
#     for date in combined_data_tuple:
#         x_date.append(date[0])
#         y1_gross.append(int(float(date[1])/divisor))
#         y2_liability.append(int(float(date[2])/divisor))
#         y3_net.append(int(float(date[3])/divisor))
#
#     # determines axis internals and max values. This is to help keep the graph legible with fluctuating input quantities
#     x_interval = ceil(len(x_date)/6)
#     mod_lar_y = largest_y_value / divisor
#     y_max = round(mod_lar_y, -1) + 10
#     y_interval_raw = ceil(mod_lar_y/15)
#     y_interval = round(y_interval_raw, -1)
#
#     plt.plot(x_date, y1_gross, color='#275929', linewidth=1.5)
#     plt.plot(x_date, y3_net, color='#38803B', linewidth=1.5)
#     plt.plot(x_date, y2_liability, color='#803838', linewidth=1.5)
#
#     plt.fill_between(x_date, y1_gross, y3_net, color='#275929')
#     plt.fill_between(x_date, y3_net, y2_liability, color='#38803B')
#     plt.fill_between(x_date, y2_liability, y2=0, color='#803838')
#
#     plt.xticks(np.arange(0, len(x_date), x_interval), rotation=0, ha='left')
#     plt.yticks(np.arange(0, y_max + 10, y_interval), rotation=0)
#     plt.minorticks_on()
#     plt.tick_params(axis='y',
#                     which='major',
#                     grid_alpha=1)
#     plt.tick_params(axis='x',
#                     which='major',
#                     labelsize='8',
#                     pad=6.0,)
#     plt.tick_params(axis='x',
#                     which='minor',
#                     bottom=False)
#
#     plt.ylim(bottom=0)
#     plt.xlim(left=0, right=len(x_date))
#     plt.xlabel('Date (YYY/MM/DD)', labelpad=5)
#     plt.ylabel(f'$ ({designation})', labelpad=5)
#
#     plt.grid(b=True,
#              which='major',
#              axis='y',
#              color='0.10',
#              linestyle='-',
#              linewidth='0.6')
#     plt.grid(b=True,
#              which='minor',
#              axis='y',
#              color='0.2',
#              linestyle='-',
#              linewidth='0.2')
#
#     plt.legend(['Gross', 'Net', 'Liability'],
#                loc=6,
#                bbox_to_anchor=(0.05, 0.25),
#                markerscale=3.0)
#     plt.show()


def net_worth_line_graph(database):
    # SQL raw data acquisition
    combined_data_statement = "SELECT * FROM NetWorth ORDER BY Date ASC LIMIT 0, 49999"
    combined_data_tuple = obtain_sql_list(combined_data_statement, database)
    largest_value_statement = "SELECT Gross FROM NetWorth"
    largest_y_tuple = obtain_sql_list(largest_value_statement, database)
    largest_y_raw = []

    for grossinput in largest_y_tuple:
        largest_y_raw.append(int(float(grossinput[0])))

    largest_y_value = max(largest_y_raw)

    # placeholder lists and
    x_date = []
    y1_gross = []
    y1_gross_fill = []
    y2_liability = []
    y2_liability_fill = []
    y3_net = []
    y3_net_fill = []
    divisor = 0
    designation = ""

    # determines the divisor for the y-axis.
    if largest_y_value >= 1000000:
        divisor = 10000
        designation = "ten thousands"
    elif largest_y_value >= 100000:
        divisor = 1000
        designation = "thousands"
    elif largest_y_value >= 10000:
        divisor = 100
        designation = "hundreds"
    elif largest_y_value >= 1000:
        divisor = 10
        designation = "tens"
    elif largest_y_value < 1000:
        divisor = 1
        designation = "dollars"

    # separates the SQL data into their appropriate axis designations
    for date in combined_data_tuple:
        x_date.append(date[0])
        y1_gross.append(int(float(date[1])/divisor))
        y1_gross_fill.append(int(float(date[1])/divisor) - 1)
        y2_liability.append(int(float(date[2])/divisor))
        y2_liability_fill.append(int(float(date[2])/divisor) - 1)
        y3_net.append(int(float(date[3])/divisor))
        y3_net_fill.append(int(float(date[3])/divisor) - 1)

    # determines axis internals and max values. This is to help keep the graph legible with fluctuating input quantities
    x_interval = ceil(len(x_date)/6)
    mod_lar_y = largest_y_value / divisor
    y_max = round(mod_lar_y, -1) + 10
    y_interval_raw = ceil(mod_lar_y/15)
    y_interval = round(y_interval_raw, -1)
    if y_interval == 0:
        y_interval += 1

    lg_data = [x_date, y1_gross, y2_liability, y3_net, x_interval, y_interval, y_max, designation, y1_gross_fill, y2_liability_fill, y3_net_fill]
    return lg_data


def nested_snapshot(database, graph_focus):
    if graph_focus == "Asset":
        parenttypes = ["Bank", "Cash", "CD", "Equity", "Treasury", "Retirement", ]
    elif graph_focus == "Liability":
        parenttypes = ["Debt", "Credit"]
    else:
        parenttypes = ["Bank"]

    bank_accounts = []
    cash_accounts = []
    cd_accounts = []
    equity_accounts = []
    treasury_accounts = []
    retirement_accounts = []
    debt_accounts = []
    credit_accounts = []
    flat_values = []
    sizes = []

    parentType_dict = {
        "Bank": bank_accounts,
        "Cash": cash_accounts,
        "CD": cd_accounts,
        "Equity": equity_accounts,
        "Treasury": treasury_accounts,
        "Retirement": retirement_accounts,
        "Debt": debt_accounts,
        "Credit": credit_accounts,
    }

    gross_statement = "SELECT SUM(Balance) FROM Account_Summary WHERE ItemType='{0}'".format(graph_focus)
    gross_worth = obtain_sql_value(gross_statement, database)[0]

    if gross_worth <= 0 or gross_worth is None:
        gross_worth = 1

    for parent in parenttypes:
        size_statement = "SELECT SUM(Balance) FROM Account_Summary WHERE ParentType='{0}'".format(parent)
        value = obtain_sql_value(size_statement, database)[0]
        if value is None or value < 0:
            value = 0
        percentage = (float(value) / float(gross_worth)) * 100
        percentage = decimal_places(percentage, 2)
        sizes.append(percentage)

        balance_statement = "SELECT Balance FROM Account_Summary WHERE ParentType='{0}'".format(parent)
        account_balances = obtain_sql_list(balance_statement, database)
        account_balances.sort(reverse=True)
        for balance in account_balances:
            correction = balance[0]
            if correction < 0:
                correction = 0
            parentType_dict[parent].append(correction)
            flat_values.append(correction)

    if graph_focus == "Asset":
        sum_balances = [sum(bank_accounts), sum(cash_accounts), sum(cd_accounts), sum(equity_accounts), sum(treasury_accounts), sum(retirement_accounts)]
        cmap = plt.cm.BuGn
        outer_colors = [*cmap(np.linspace(1, .33, 6))]
        inner_colors = [*cmap(np.linspace(0.6, .1, len(bank_accounts))),
                        *cmap(np.linspace(0.6, .1, len(cash_accounts))),
                        *cmap(np.linspace(0.6, .1, len(cd_accounts))),
                        *cmap(np.linspace(0.6, .1, len(equity_accounts))),
                        *cmap(np.linspace(0.6, .1, len(treasury_accounts))),
                        *cmap(np.linspace(0.6, .1, len(retirement_accounts))),
                        ]

    elif graph_focus == "Liability":
        sum_balances = [sum(debt_accounts), sum(credit_accounts)]
        cmap = plt.cm.OrRd
        outer_colors = [*cmap(np.linspace(0.8, .33, 2))]
        inner_colors = [*cmap(np.linspace(0.6, .1, len(debt_accounts))),
                        *cmap(np.linspace(0.6, .1, len(credit_accounts))),
                        ]

    else:
        sum_balances = [sum(bank_accounts)]
        cmap = plt.cm.Greys
        outer_colors = [*cmap(np.linspace(0.8, .33, 6))]
        inner_colors = [*cmap(np.linspace(0.6, .1, len(debt_accounts))),
                        ]

    target_values = [sum_balances, outer_colors, flat_values, inner_colors, sizes]

    return target_values


if __name__ == "__main__":
    database = os.path.join(os.getcwd(), '..', 'data/account/b8aem6j45m5r36ghs.db')
    net_worth_line_graph(database)
