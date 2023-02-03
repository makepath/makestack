// React
import React, { FC, useEffect } from 'react'
import { Map, BackgroundLayerSpecification } from 'maplibre-gl'

// Custom

interface BackgroundLayerProps extends Omit<BackgroundLayerSpecification, 'type'> {
  map: Map
}

const BackgroundLayer: FC<BackgroundLayerProps> = (props: BackgroundLayerProps) => {

  const { map, ...layerOptions } = props
  const type = 'background'

  useEffect(() => {
    map.addLayer({ type, ...layerOptions })
    return () => {
      map.removeLayer(layerOptions.id)
    }
  }, [])

  return null

}

export default BackgroundLayer
