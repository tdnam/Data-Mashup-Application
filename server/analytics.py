import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from db import *

# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

plotly.tools.set_credentials_file(username='tdnam39', api_key='u5U0YaYraKTmTlDyvtok')

def get_analytics():
	""" Get the analytics and open it in a new tab. """
	data = [go.Bar(
				x=get_all_char_name(),
				y=get_all_count()
		)]
	py.plot(data, filename='basic-bar')
