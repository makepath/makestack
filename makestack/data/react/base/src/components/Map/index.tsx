// React
import React, { FC, useEffect, useRef, useState } from 'react'
import './index.css';
import maplibregl from 'maplibre-gl'
import MapStyle from './MapStyle';
import FillLayer from '../Layers/FillLayer';

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
      map.addSource('countries', {
        type: 'geojson',
        data: 'http://localhost:5000/world-countries-geojson/geojson'
      })
      setMapObject(map)
    })

    return () => {
      map.remove()
    }

  }, [])


  return (
    <div id="map">
      {mapObject && <FillLayer map={mapObject} id="fill-layer" source="countries" paint={{ 'fill-color': '#088', 'fill-opacity': 0.5 }} />}
    </div>
  )
}

export default Map
