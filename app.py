import webview
import os
import sys

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, filename)

html_path = resource_path('index.html')

webview.create_window(
    title='Bodunde Femi Temitope Weather App',
    url=f'file:///{html_path}',
    width=900,
    height=700,
    resizable=True
)
webview.start()