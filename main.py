from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HOST, PORT = "0.0.0.0", 8000
BASE = Path(__file__).parent

HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>BlueWhale</title>
    <link rel="icon" type="image/svg+xml" href="/whale-logo.svg">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@700&display=swap" rel="stylesheet">

    <style>
        body {
            margin: 0;
            background-color: #4a6a94;
            color: #eef1f4;
            font-family: "Merriweather", serif;
            text-align: center;
        }
        h1 {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
            margin: 24px 0 0;
            font-size: 2.5rem;
            font-weight: 700;
            padding: 0 20px;
        }
        h1 img {
            height: 1.4em;
            width: auto;
        }
        #status {
            margin-top: 20px;
            font-size: 0.9rem;
            font-weight: 400;
        }
        #map {
            width: 95%;
            max-width: 1400px;
            height: 80vh;
            margin: 15px auto 30px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
    </style>
</head>
<body>
    <h1>
        <img src="/whale-logo.svg" alt="Кит">
        <span>Трекер краснокнижных морских млекопитающих</span>
    </h1>

    <div id="status">Загрузка данных…</div>
    <div id="map"></div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script>
        
        const jsonUrl = "https://www.movebank.org/movebank/service/public/json";
        const study_id = 16880941;                                 
        const animals = ["Mary", "Butterball", "Schaumboch"];      
        const colors = ["#FFFF00", "#0099FF", "#FF00FF"];           
        const maxEvents = 100;                                      
        const sensorType = "gps";                                  

        async function initMap() {
            const { Map, InfoWindow } = await google.maps.importLibrary("maps");
            const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

            const map = new Map(document.getElementById("map"), {
                center: { lat: 20, lng: 0 },
                zoom: 2,
                mapId: "DEMO_MAP_ID"
            });
            const info = new InfoWindow();
            const status = document.getElementById("status");

            $.getJSON(jsonUrl + "?callback=?", {
                study_id: study_id,
                individual_local_identifiers: animals,
                max_events_per_individual: maxEvents,
                sensor_type: sensorType
            }).done(function (data) {
                if (!data.individuals || data.individuals.length === 0) {
                    status.textContent = "Данные не найдены: проверьте ID исследования, имена животных и права доступа.";
                    return;
                }

                const bounds = new google.maps.LatLngBounds();

                data.individuals.forEach(function (ind, i) {
                    const locs = ind.locations;
                    if (!locs || locs.length === 0) return;
                    const color = colors[i % colors.length];

                    // Линия маршрута
                    const path = locs.map(function (l) {
                        return { lat: l.location_lat, lng: l.location_long };
                    });
                    new google.maps.Polyline({
                        path: path,
                        strokeColor: color,
                        strokeOpacity: 0.8,
                        strokeWeight: 2,
                        map: map
                    });
                    path.forEach(function (p) { bounds.extend(p); });

                   
                    const last = locs[locs.length - 1];
                    const dot = document.createElement("div");
                    dot.style.cssText = "width:14px;height:14px;border-radius:50%;border:2px solid #fff;background:" + color;

                    const marker = new AdvancedMarkerElement({
                        map: map,
                        position: { lat: last.location_lat, lng: last.location_long },
                        content: dot,
                        title: ind.individual_local_identifier
                    });
                    marker.addListener("click", function () {
                        info.setContent(
                            "<b>" + ind.individual_local_identifier + "</b><br>" +
                            "Последняя точка: " + new Date(last.timestamp).toLocaleString("ru-RU")
                        );
                        info.open({ map: map, anchor: marker });
                    });
                });

                map.fitBounds(bounds);
                status.textContent = "Показано животных: " + data.individuals.length;
            }).fail(function () {
                status.textContent = "Не удалось загрузить данные из Movebank.";
            });
        }
    </script>
    <script async defer
        src="https://maps.googleapis.com/maps/api/js?key=АПИ_КЛЮЧ&tMap&loading=async">
    </script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/whale-logo.svg":
            icon = BASE / "whale-logo.svg"
            if icon.exists():
                data = icon.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "image/svg+xml")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_error(404)
        else:
            data = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

if __name__ == "__main__":
    print(f"Сервер запущен: http://localhost:{PORT}")
    HTTPServer((HOST, PORT), Handler).serve_forever()