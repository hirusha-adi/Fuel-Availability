"""
NOTES

start at
    7.4887197, 80.3597918 - Kurunegala Town

inside head
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">

at end of body
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script>

"""

import folium
import os
import json
from bs4 import BeautifulSoup


class Colors:
    available = "228B22"
    notAvailable = "8B0000"


class GenerateMap:
    def __init__(self) -> None:
        self._map = folium.Map(location=[7.4887197, 80.3597918], zoom_start=15)
        self._data_file_path = os.path.join('database', 'data.json')
        self._data = None
        self._save_path = None

    def loadData(self):
        with open(self._data_file_path, 'r', encoding='utf-8') as _file:
            self._data = json.load(_file)

    def addMarkers(self):
        if self._data is None:
            self.loadData()
        for item in self._data:
            folium.Marker(
                item['coordinates'],
                popup=f'''Petrol: <strong style="color: #{Colors.available}">{'Available' if item["availablitiy"]["petrol"] == True else 'Not Available'}</strong><br><br>Diesel: <strong style="color: #{Colors.notAvailable}">{'Available' if item["availablitiy"]["diesel"] == True else 'Not Available'}</strong>''',
                tooltip=item['name']
            ).add_to(self._map)

    def save(self, path='map.html'):
        self._save_path = str(path)
        if not self._save_path.endswith('html'):
            self._save_path += '.html'
        if os.path.isfile(self._save_path):
            os.remove(self._save_path)
        try:
            self._map.save(self._save_path)
        except Exception as e:
            print('ERROR:', e)
            return True

    def fixHtml(self, html):
        pass

    def reformatHtml(self, path=None):
        if path is None:
            self._save_path = str(path)

        if not self._save_path.endswith('html'):
            self._save_path += '.html'

        with open(self._save_path, 'r', encoding='utf-8') as _file:
            soup = BeautifulSoup(str(_file.read()), 'html.parser').prettify()

        with open(self._save_path, 'w', encoding='utf-8') as _file:
            _file.write(soup)

    def run(self):
        self.loadData()
        self.addMarkers()
        self.save()


obj = GenerateMap()
obj.run()
