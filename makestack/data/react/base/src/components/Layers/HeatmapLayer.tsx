// React
import React, { FC, useEffect } from 'react'
import { Map, HeatmapLayerSpecification } from 'maplibre-gl'

// Custom

interface HeatmapLayerProps extends Omit<HeatmapLayerSpecification, 'type'> {
  map: Map
}

const HeatmapLayer: FC<HeatmapLayerProps> = (props: HeatmapLayerProps) => {

  const { map, ...layerOptions } = props
  const type = 'heatmap'

  useEffect(() => {
    map.addLayer({ type, ...layerOptions })
    return () => {
      map.removeLayer(layerOptions.id)
    }
  }, [])

  return null

}

export default HeatmapLayer
