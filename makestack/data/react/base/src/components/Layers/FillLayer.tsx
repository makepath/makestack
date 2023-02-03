// React
import React, { FC, useEffect } from 'react'
import { Map, FillLayerSpecification } from 'maplibre-gl'

// Custom

interface FillLayerProps extends Omit<FillLayerSpecification, 'type'> {
  map: Map
}

const FillLayer: FC<FillLayerProps> = (props: FillLayerProps) => {

  const { map, ...layerOptions } = props
  const type = 'fill'

  useEffect(() => {
    map.addLayer({ type, ...layerOptions })
    return () => {
      map.removeLayer(layerOptions.id)
    }
  }, [])

  return null

}

export default FillLayer
