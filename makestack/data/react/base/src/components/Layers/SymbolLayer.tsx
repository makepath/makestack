// React
import React, { FC, useEffect } from 'react'
import { Map, SymbolLayerSpecification } from 'maplibre-gl'

// Custom

interface SymbolLayerProps extends Omit<SymbolLayerSpecification, 'type'> {
  map: Map
}

const SymbolLayer: FC<SymbolLayerProps> = (props: SymbolLayerProps) => {

  const { map, ...layerOptions } = props
  const type = 'symbol'

  useEffect(() => {
    map.addLayer({ type, ...layerOptions })
    return () => {
      map.removeLayer(layerOptions.id)
    }
  }, [])

  return null

}

export default SymbolLayer
