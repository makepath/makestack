// React
import React, { FC, useEffect } from 'react'
import { Map, RasterLayerSpecification } from 'maplibre-gl'

// Custom

interface RasterLayerProps extends Omit<RasterLayerSpecification, 'type'> {
  map: Map
}

const RasterLayer: FC<RasterLayerProps> = (props: RasterLayerProps) => {

  const { map, ...layerOptions } = props
  const type = 'raster'

  useEffect(() => {
    map.addLayer({ type, ...layerOptions })
    return () => {
      map.removeLayer(layerOptions.id)
    }
  }, [])

  return null

}

export default RasterLayer
