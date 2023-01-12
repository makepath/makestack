// React
import React, { FC, useEffect, useRef } from 'react'
import './Map.css';
import maplibregl from 'maplibre-gl'
import MapStyle from './MapStyle';

// Custom

const Map: FC = () => {
  const mapRef = useRef<maplibregl.Map>()
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
    mapRef.current = map
  }, [])


  return (
    <div id="map" />
  )
}

export default Map
