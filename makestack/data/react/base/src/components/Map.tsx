// React
import React, { FC, useEffect, useRef, useState } from 'react'
import './Map.css';
import maplibregl from 'maplibre-gl'
import MapStyle from './MapStyle';
import FillLayer from './Layers/FillLayer';
import RasterLayer from './Layers/RasterLayer';

// Custom

const Map: FC = () => {
  const mapRef = useRef<maplibregl.Map>()
  const [mapObject, setMapObject] = useState<maplibregl.Map>()
  const minZoom = 2;
  const maxZoom = 7;

  useEffect(() => {
    const map = new maplibregl.Map({
      container: 'map',
      style: MapStyle,
      center: [0, 0],
      zoom: 2,
      minZoom: minZoom,
      maxZoom: maxZoom,
    });

    map.on('load', () => {
      map.addSource('countries-geojson', {
        type: 'geojson',
        data: 'http://localhost:5000/world-countries-geojson/geojson'
      })
      map.addSource('countries-raster', {
        type: 'raster',
        tiles: ['http://localhost:5000/world-countries-tile/tile/{z}/{x}/{y}']
      })
      map.addSource('countries-boundaries-raster', {
        type: 'raster',
        tiles: ['http://localhost:5000/world-boundaries-tile/tile/{z}/{x}/{y}']
      })
      setMapObject(map)
    })

    return () => {
      map.remove()
    }

  }, [])


  return (
    <div id="map">
      {mapObject && <RasterLayer map={mapObject} id="countries-raster-layer" source="countries-raster" paint={{ "raster-opacity": 0.5 }} />}
      {mapObject && <RasterLayer map={mapObject} id="countries-boundaries-raster-layer" source="countries-boundaries-raster" />}
      {/*mapObject && <FillLayer map={mapObject} id="fill-layer" source="countries-geojson" paint={{ 'fill-color': '#088', 'fill-opacity': 0.5 }} />*/}
    </div>
  )
}

export default Map
