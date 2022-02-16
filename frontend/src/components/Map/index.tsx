// React
import React, { FC, useEffect, useRef, useState } from 'react'
import './index.css';
import maplibre from 'maplibre-gl'
import mapStyle from '../../assets/style.json'
import { ILayersState, Region, TileSet } from 'storage/layers/models';
// import { getLegend } from 'storage/layers/duck';
// import { useDispatch } from 'react-redux';
// import Legend from './Legend';
import Layers from './Layers';

// Custom

const mapshaderUrl = 'http://localhost:5000/'

interface MapProps extends ILayersState {
  preloadAllLayers?: boolean
}

const Map: FC<MapProps> = (props: MapProps) => {
  // const dispatch = useDispatch()
  const mapRef = useRef<maplibre.Map>()
  // const [legend, setLegend] = useState<ILegend>()
  const [mapLoading, setMapLoading] = useState(true)
  const minZoom = 3;
  const maxZoom = 15;

  useEffect(() => {
    const map = new maplibre.Map({
      container: 'map',
      style: mapStyle as maplibre.Style,
      center: [-15.5, 28.5],
      zoom: 3,
      minZoom: minZoom,
      maxZoom: maxZoom,
    });

    map.on('load', () => {
      if (mapRef.current) {
        if (props.preloadAllLayers) {
          props.layers.forEach(layer => {
            addLayer(layer)
          })
        }
        else if (props.selectedRegion) {
          addLayer(props.selectedRegion)
        }
      }
      setMapLoading(false)
    });
    // Uncomment this snippet to console.log current map bounds on move end
    /*map.on('moveend', () => {
      console.log(mapRef.current?.getBounds())
    })*/
    mapRef.current = map
  }, [])

  useEffect(() => {
    updateLayers()
    if (mapRef.current && props.selectedRegion?.bounds) {
      mapRef.current.fitBounds(props.selectedRegion.bounds)
    }
  }, [props.selectedRegion?.id])

  /*useEffect(() => {
    if (props.selectedRegion?.id) {
      const currentLegend = props.legends[props.selectedRegion?.id]
      if (currentLegend) {
        setLegend(currentLegend)
      }
    }
  }, [props.legends])*/

  const addLayer = (layer: Region) => {
    layer.categories.forEach(category => {
      category.tilesets.forEach(tileset => {
        const sourceName = `${layer.id}-${category.id}-${tileset.id}`
        addTileset(sourceName, tileset)
      })
    })
  }

  const addTileset = (sourceName: string, tileset: TileSet) => {
    const sourceLoaded = mapRef.current?.getSource(sourceName)
    if (mapRef.current && !sourceLoaded) {
      const service = tileset.service
      if (service) {
        const type = service.type === "tile" || service.type === "wms" ? "raster" : service.type
        const layerType = service.type === "tile" || service.type === "wms" || service.type === "image" ? "raster" :
          service.type === "geojson" ? "fill" :
            service.type
        const layerStyle = service.type === "tile" || service.type === "wms" ? { paint: { "raster-opacity": 0, } } :
          service.type === "geojson" ? { paint: { "fill-opacity": 0, "fill-color": '#ffffff' } } :
            {}
        const sourceDict = service.type === "tile" || service.type === "wms" ? { tiles: [mapshaderUrl + service.clientUrl.replace("-wms?bbox", "-wms/wms?bbox").replace("{XMIN},{YMIN},{XMAX},{YMAX}", "{bbox-epsg-3857}")] } :
          service.type === 'geojson' ? { data: mapshaderUrl + service.clientUrl } : {}
        mapRef.current.addSource(sourceName, {
          type: type,
          ...sourceDict
        })
        mapRef.current.addLayer({
          id: sourceName + '-tiles',
          source: sourceName,
          type: layerType,
          ...layerStyle,
          layout: {
            visibility: 'none'
          }
        })
      }
    }
  }

  /* const currentLegend = props.legends[layer.id]
  if (currentLegend) {
    setLegend(currentLegend)
  } else {
    dispatch(getLegend(layer))
  }*/

  const updateLayers = () => {
    props.layers.forEach(layer => {
      layer.categories.forEach(category => {
        category.tilesets.forEach(tileset => {
          const interval = window.setInterval(() => {
            const sourceName = `${layer.id}-${category.id}-${tileset.id}`
            const sourceLoaded = mapRef.current?.getSource(sourceName)
            if (!sourceLoaded && layer.id === props.selectedRegion?.id) {
              addTileset(sourceName, tileset)
            }
            if (mapRef.current && mapRef.current.isStyleLoaded() && sourceLoaded) {
              mapRef.current.setLayoutProperty(
                sourceName + '-tiles',
                'visibility',
                layer.id === props.selectedRegion?.id ? 'visible' : 'none',
              )
              window.clearInterval(interval)
            }
          }, 200)
        })
      })
    })
  }

  return (
    <div id="map">
      {/*legend &&
        <Legend legend={legend} />
      */}
      {!mapLoading && mapRef.current && props.selectedRegion &&
        <Layers
          map={mapRef.current}
          layers={props.layers}
          region={props.selectedRegion}
          loading={props.loading}
        />
      }
    </div>
  )
}

export default Map
