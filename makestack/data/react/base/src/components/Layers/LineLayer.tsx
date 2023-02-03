// React
import React, { FC, useEffect } from 'react'
import { Map, LineLayerSpecification } from 'maplibre-gl'

// Custom

interface LineLayerProps extends Omit<LineLayerSpecification, 'type'> {
  map: Map
}

const LineLayer: FC<LineLayerProps> = (props: LineLayerProps) => {

  const { map, ...layerOptions } = props
  const type = 'line'

  useEffect(() => {
    map.addLayer({ type, ...layerOptions })
    return () => {
      map.removeLayer(layerOptions.id)
    }
  }, [])

  return null

}

export default LineLayer
