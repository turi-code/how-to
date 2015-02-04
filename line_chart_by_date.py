# View time-series data as a line chart in Canvas
# This renders a similar chart to http://finance.yahoo.com/echarts?s=GE+Interactive#%7B%22range%22%3A%22max%22%2C%22scale%22%3A%22linear%22%7D
import calendar
import graphlab as gl
import numpy # Requires 'pip install numpy==1.9.1'
sf = gl.SFrame.read_csv('http://real-chart.finance.yahoo.com/table.csv?s=GE&a=00&b=2&c=1962&d=01&e=4&f=2015&g=d&ignore=.csv')
date_as_int = [long(calendar.timegm(d.utctimetuple())) for d in sf['Date'].str_to_datetime()]
bin_edges = numpy.histogram(date_as_int, 499)
sf['bin'] = numpy.digitize(date_as_int, bin_edges[1], True)
sf.groupby('bin', gl.aggregate.AVG('Adj Close')).show(view='Line Chart', x='bin', y='Avg of Adj Close')
