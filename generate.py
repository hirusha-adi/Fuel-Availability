"""
NOTES

start at
    7.4887197, 80.3597918 - Kurunegala Town

inside head
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">

before body
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">

at end of body
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script>

"""

import folium
import os
from database.mongo import Stations
from database.settings import JawgToken


class Colors:
    available = "228B22"
    notAvailable = "8B0000"


class GenerateMap:
    def __init__(self) -> None:
        self._map = folium.Map(location=[7.4887197, 80.3597918], zoom_start=15)
        self._data = None
        self._save_path = None

    def loadData(self):
        self._data = Stations.getAllStations()

    def addMarkers(self, petrol: bool = True, diesel: bool = True):
        if self._data is None:
            self.loadData()
        if (petrol and diesel):
            for item in self._data:
                folium.Marker(
                    item['coordinates'],
                    popup=f'''Petrol: <strong style="color: #{Colors.available if item["availablitiy"]["petrol"] == True else Colors.notAvailable}">{'Available' if item["availablitiy"]["petrol"] == True else 'Not Available'}</strong><br><br>Diesel: <strong style="color: #{Colors.available if item["availablitiy"]["diesel"] == True else Colors.notAvailable}">{'Available' if item["availablitiy"]["diesel"] == True else 'Not Available'}</strong><br><br><a href="https://www.google.com/maps/search/?api=1&query={item['coordinates'][0]},{item['coordinates'][1]}" target="_blank" rel="noopener noreferrer">Visit</a><br><br><a href="/amount/{str(item['id'])}" >More Info</a>''',
                    tooltip=item['name']
                ).add_to(self._map)
        elif petrol:
            for item in self._data:
                if item["availablitiy"]["petrol"] == True:
                    folium.Marker(
                        item['coordinates'],
                        popup=f'''Petrol: <strong style="color: #{Colors.available if item["availablitiy"]["petrol"] == True else Colors.notAvailable}">{'Available' if item["availablitiy"]["petrol"] == True else 'Not Available'}</strong><br><br>Diesel: <strong style="color: #{Colors.available if item["availablitiy"]["diesel"] == True else Colors.notAvailable}">{'Available' if item["availablitiy"]["diesel"] == True else 'Not Available'}</strong><br><br><a href="https://www.google.com/maps/search/?api=1&query={item['coordinates'][0]},{item['coordinates'][1]}" target="_blank" rel="noopener noreferrer">Visit</a><br><br><a href="/amount/{str(item['id'])}" >More Info</a>''',
                        tooltip=item['name']
                    ).add_to(self._map)
        elif diesel:
            for item in self._data:
                if item["availablitiy"]["diesel"] == True:
                    folium.Marker(
                        item['coordinates'],
                        popup=f'''Petrol: <strong style="color: #{Colors.available if item["availablitiy"]["petrol"] == True else Colors.notAvailable}">{'Available' if item["availablitiy"]["petrol"] == True else 'Not Available'}</strong><br><br>Diesel: <strong style="color: #{Colors.available if item["availablitiy"]["diesel"] == True else Colors.notAvailable}">{'Available' if item["availablitiy"]["diesel"] == True else 'Not Available'}</strong><br><br><a href="https://www.google.com/maps/search/?api=1&query={item['coordinates'][0]},{item['coordinates'][1]}" target="_blank" rel="noopener noreferrer">Visit</a><br><br><a href="/amount/{str(item['id'])}" >More Info</a>''',
                        tooltip=item['name']
                    ).add_to(self._map)

    def save(self, path=None):
        if path is None:
            path = 'map.html'
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

    def fixHtml(self):
        with open(self._save_path, 'r', encoding='utf-8') as _file:
            html = str(_file.read()).replace(
                "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css",
                "https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css"
            ).replace(
                "height: 100.0%;",
                "height: 93.0%;"
            ).replace(
                "</body>",
                '<script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js"></script><script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script></body>'
            ).replace(
                "<body>",
                """<link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}"><body><nav class="navbar navbar-expand-lg navbar-dark bg-dark"><a class="navbar-brand" href="/"><img src="{{ url_for('static', filename='images/logo-text.png') }}" alt="Fuel Availability" width="200px"></a><button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button><div class="collapse navbar-collapse" id="navbarSupportedContent"><ul class="navbar-nav mr-auto"><li class="nav-item active"><a class="nav-link" href="/map">Map <span class="sr-only">(current)</span></a></li><li class="nav-item"><a class="nav-link" href="/">Home</a></li><li class="nav-item dropdown"><a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Filter</a><div class="dropdown-menu" aria-labelledby="navbarDropdown"><a class="dropdown-item" onclick="showRadiusOnMap()">by Location</a><div class="dropdown-divider"></div><a class="dropdown-item" href="/map/petrol">by Petrol</a><a class="dropdown-item" href="/map/diesel">by Diesel</a><div class="dropdown-divider"></div><a class="dropdown-item" href="/map">Clear Filters</a></div></li></ul><div class="form-inline my-2 my-lg-0"><button class="btn btn-outline-success my-2 my-sm-0" type="submit"><a href="/login" style="color: #fff;text-decoration: none;">Login</a></button></div></div></nav>"""
            ).replace(
                """top: 0.0%;
                }
            </style>""",
                """top: 0.0%;
                }
                body {
                    background-color: #343a40;
                }
            </style>"""
            )

            y = html.split("""</body>
<script>""")
            a = y[1].strip()
            b = a.split(" ")[1]  # map name
            c = "var tile_layer_" + \
                a.split("var tile_layer_")[1].split(
                    ");")[0] + ");"  # remove this
            p = """
            var Jawg_Matrix = L.tileLayer('https://{s}.tile.jawg.io/jawg-matrix/{z}/{x}/{y}{r}.png?access-token={accessToken}', {
                    attribution: '<a href="http://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    minZoom: 0,
                    maxZoom: 22,
                    subdomains: 'abcd',
                    accessToken: '""" + JawgToken + """'
                });
            Jawg_Matrix.addTo(""" + b + """)
            """
            z = html.replace(c, p)

        with open(self._save_path, 'w', encoding='utf-8') as _file:
            _file.write(z.replace(
                """</script>""",
                """
            function showRadiusOnMap() {
                if (navigator.geolocation) {
                    position = navigator.geolocation.getCurrentPosition(
                        function (position) {
                            const lat = position.coords.latitude;
                            const lon = position.coords.longitude;
                            var circle = L.circle(
                                [lat, lon],
                                {
                                    radius: 7500
                                }
                            )
                            circle.addTo(""" + b + """);
                        },
                        function (err) {
                            alert(`Please provide location access and try again!`)
                        }
                    );
                }
            }
            </script>
                """
            ))

    def run(self, path='map.html', petrol: bool = True, diesel: bool = True):
        self.loadData()
        self.addMarkers(petrol=petrol, diesel=diesel)
        self.save(path=path)
        self.fixHtml()


if __name__ == "__main__":
    obj = GenerateMap()
    obj.run(path=os.path.join(os.getcwd(), 'templates', 'map.html'))
