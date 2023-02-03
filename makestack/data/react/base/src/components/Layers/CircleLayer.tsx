// React
import React, { FC, useEffect } from 'react'
import { Map, CircleLayerSpecification } from 'maplibre-gl'

// Custom

interface CircleLayerProps extends Omit<CircleLayerSpecification, 'type'> {
  map: Map
}

const CircleLayer: FC<CircleLayerProps> = (props: CircleLayerProps) => {

  const { map, ...layerOptions } = props
  const type = 'circle'

  useEffect(() => {
    map.addLayer({ type, ...layerOptions })
    return () => {
      map.removeLayer(layerOptions.id)
    }
  }, [])

  return null

}

export default CircleLayer
