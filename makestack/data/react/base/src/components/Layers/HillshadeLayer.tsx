// React
import React, { FC, useEffect } from 'react'
import { Map, HillshadeLayerSpecification } from 'maplibre-gl'

// Custom

interface HillshadeLayerProps extends Omit<HillshadeLayerSpecification, 'type'> {
  map: Map
}

const HillshadeLayer: FC<HillshadeLayerProps> = (props: HillshadeLayerProps) => {

  const { map, ...layerOptions } = props
  const type = 'hillshade'

  useEffect(() => {
    map.addLayer({ type, ...layerOptions })
    return () => {
      map.removeLayer(layerOptions.id)
    }
  }, [])

  return null

}

export default HillshadeLayer
