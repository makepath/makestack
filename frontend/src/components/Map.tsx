// React
import React, { FC, useEffect, useRef } from 'react'
import './Map.css';
import maplibre from 'maplibre-gl'
import mapStyle from '../assets/style.json'

// Custom

const Map: FC = () => {
  const mapRef = useRef<maplibre.Map>()
  const minZoom = 3;
  const maxZoom = 10;

  useEffect(() => {
    const map = new maplibre.Map({
      container: 'map',
      style: mapStyle as maplibre.Style,
      center: [-15.5, 28.5],
      zoom: 3,
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
