# create_chart.py

from bokeh.models import HoverTool, BoxSelectTool, FactorRange, Range1d, DatetimeTickFormatter
from bokeh.plotting import figure

from database.app import get_data_with_filter_name_and_data


def dict_preparation_for_bokeh(unique_name, period_from, period_to, price_name: str):
    data_db = get_data_with_filter_name_and_data(unique_name, period_from, period_to)

    dict_month_price = {}

    for value in data_db:
        month = value.order_date.strftime("%b")
        year = str(value.order_date.year)
        dict_month_price[f'{month} {year}'] = dict_month_price.get(f'{month} {year}', []) + [getattr(value, price_name)]

    for key, value in dict_month_price.items():
        average_price_per_month = round((sum(value) / len(value)), 1)
        dict_month_price[key] = average_price_per_month

    print(dict_month_price)

    return dict_month_price


def chart_history_price(data_db):

    data = {"Период": [], "Цена_1": [], "Цена_2": [], "Цена_3": [], "Цена_4": []}

    for value in data_db:
        data['Период'].append(str(value.order_date))
        data['Цена_1'].append(value.price_1)
        data['Цена_2'].append(value.price_2)
        data['Цена_3'].append(value.price_3)
        data['Цена_4'].append(value.price_4)

    xdr = FactorRange(factors=data['Период'])
    ydr = Range1d(start=0, end=max(data['Цена_1']) * 1.5)
    y_range = list(range(0, len(data['Период'])))

    tool_list = [HoverTool(), BoxSelectTool()]

    lines = figure(title='Ценовой график',
                   x_range=xdr,
                   y_range=ydr,
                   plot_width=1200,
                   plot_height=500,
                   x_axis_label='Период',
                   y_axis_label='Цена',
                   outline_line_color="#666666",
                   toolbar_location="above",
                   tools=tool_list)

    lines.line(y_range, data['Цена_1'], color='red', legend_label="Цена 1", line_width=1)
    lines.line(y_range, data['Цена_2'], color='blue', legend_label="Цена 2", line_width=1)
    lines.line(y_range, data['Цена_3'], color='orange', legend_label="Цена 3", line_width=1)
    lines.line(y_range, data['Цена_4'], color='black', legend_label="Цена 4", line_width=1)

    lines.xaxis.formatter = DatetimeTickFormatter(
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"])

    lines.xaxis.major_label_orientation = 1
    lines.legend.orientation = "horizontal"
    lines.legend.location = "top_center"

    return lines


def chart_price_seasonality(unique_name, period_from, period_to):

    dict_month_price_1 = dict_preparation_for_bokeh(unique_name, period_from, period_to, 'price_1')
    dict_month_price_2 = dict_preparation_for_bokeh(unique_name, period_from, period_to, 'price_2')
    dict_month_price_3 = dict_preparation_for_bokeh(unique_name, period_from, period_to, 'price_3')
    dict_month_price_4 = dict_preparation_for_bokeh(unique_name, period_from, period_to, 'price_4')

    xdr = FactorRange(factors=list(dict_month_price_1.keys()))
    ydr = Range1d(start=0, end=max(dict_month_price_1.values()) * 1.5)
    y_range = list(range(0, len(dict_month_price_1.keys())))

    tool_list = [HoverTool(), BoxSelectTool()]

    lines = figure(title='Ценовой график',
                   x_range=xdr,
                   y_range=ydr,
                   plot_width=1200,
                   plot_height=500,
                   x_axis_label='Период',
                   y_axis_label='Цена',
                   outline_line_color="#666666",
                   toolbar_location="above",
                   tools=tool_list)

    lines.line(y_range, list(dict_month_price_1.values()), color='red', legend_label="Цена 1", line_width=1)
    lines.line(y_range, list(dict_month_price_2.values()), color='blue', legend_label="Цена 2", line_width=1)
    lines.line(y_range, list(dict_month_price_3.values()), color='orange', legend_label="Цена 3", line_width=1)
    lines.line(y_range, list(dict_month_price_4.values()), color='black', legend_label="Цена 4", line_width=1)

    lines.xaxis.major_label_orientation = 1
    lines.legend.orientation = "horizontal"
    lines.legend.location = "top_center"

    return lines
