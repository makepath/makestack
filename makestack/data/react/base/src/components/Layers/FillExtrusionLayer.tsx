// React
import React, { FC, useEffect } from 'react'
import { Map, FillExtrusionLayerSpecification } from 'maplibre-gl'

// Custom

interface FillExtrusionLayerProps extends Omit<FillExtrusionLayerSpecification, 'type'> {
  map: Map
}

const FillExtrusionLayer: FC<FillExtrusionLayerProps> = (props: FillExtrusionLayerProps) => {

  const { map, ...layerOptions } = props
  const type = 'fill-extrusion'

  useEffect(() => {
    map.addLayer({ type, ...layerOptions })
    return () => {
      map.removeLayer(layerOptions.id)
    }
  }, [])

  return null

}

export default FillExtrusionLayer
