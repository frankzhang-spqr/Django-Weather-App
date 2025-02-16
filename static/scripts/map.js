function initMap(apiKey, containerId, center = [0, 20], zoom = 2) {
    // Convert center coordinates to OpenLayers format
    const mapCenter = ol.proj.fromLonLat(center);

    // Create base layer (OpenStreetMap)
    const baseLayer = new ol.layer.Tile({
        source: new ol.source.OSM(),
        visible: true,
        title: 'Base Map'
    });

    // Create weather layers
    const cloudsLayer = new ol.layer.Tile({
        source: new ol.source.XYZ({
            url: `https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=${apiKey}`,
            crossOrigin: 'anonymous'
        }),
        opacity: 0.6,
        visible: true,
        title: 'Clouds'
    });

    const precipitationLayer = new ol.layer.Tile({
        source: new ol.source.XYZ({
            url: `https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=${apiKey}`,
            crossOrigin: 'anonymous'
        }),
        opacity: 0.6,
        visible: true,
        title: 'Precipitation'
    });

    const temperatureLayer = new ol.layer.Tile({
        source: new ol.source.XYZ({
            url: `https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=${apiKey}`,
            crossOrigin: 'anonymous'
        }),
        opacity: 0.4,
        visible: false,
        title: 'Temperature'
    });

    const windLayer = new ol.layer.Tile({
        source: new ol.source.XYZ({
            url: `https://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid=${apiKey}`,
            crossOrigin: 'anonymous'
        }),
        opacity: 0.5,
        visible: false,
        title: 'Wind Speed'
    });

    // Create map
    const map = new ol.Map({
        target: containerId,
        layers: [baseLayer, cloudsLayer, precipitationLayer, temperatureLayer, windLayer],
        view: new ol.View({
            center: mapCenter,
            zoom: zoom,
            minZoom: 2,
            maxZoom: 18
        }),
        controls: ol.control.defaults().extend([
            new ol.control.ScaleLine(),
            new ol.control.FullScreen(),
            new ol.control.ZoomSlider()
        ])
    });

    // Add layer switcher
    const layerSwitcher = document.createElement('div');
    layerSwitcher.className = 'layer-switcher';
    layerSwitcher.innerHTML = `
        <div class="legend">
            <h4>Weather Layers</h4>
            <label><input type="checkbox" checked data-layer="clouds"> Clouds</label>
            <label><input type="checkbox" checked data-layer="precipitation"> Precipitation</label>
            <label><input type="checkbox" data-layer="temperature"> Temperature</label>
            <label><input type="checkbox" data-layer="wind"> Wind Speed</label>
        </div>
    `;

    document.getElementById(containerId).appendChild(layerSwitcher);

    // Handle layer visibility
    const layers = {
        clouds: cloudsLayer,
        precipitation: precipitationLayer,
        temperature: temperatureLayer,
        wind: windLayer
    };

    const checkboxes = layerSwitcher.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            const layer = layers[e.target.dataset.layer];
            if (layer) {
                layer.setVisible(e.target.checked);
            }
        });
    });

    // Add mouse position control
    const mousePositionControl = new ol.control.MousePosition({
        coordinateFormat: ol.coordinate.createStringXY(4),
        projection: 'EPSG:4326',
        className: 'mouse-position',
        target: document.createElement('div'),
        undefinedHTML: '&nbsp;'
    });
    map.addControl(mousePositionControl);

    // Update map size when container becomes visible
    const observer = new ResizeObserver(() => {
        map.updateSize();
    });
    observer.observe(document.getElementById(containerId));

    return map;
}
