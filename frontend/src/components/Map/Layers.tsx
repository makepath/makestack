// React
import React, { FC, useState, useEffect } from 'react'
import { Card, Row, Slider, Typography, Checkbox, Divider, Collapse, Select } from 'antd'
import { Category, Layers as ILayers, Region, TileSet } from 'storage/layers/models'
import maplibre from 'maplibre-gl'

// Custom
import './Layers.css'
import { useDispatch } from 'react-redux'
import { checkCategory, checkTileset, selectRegion } from 'storage/layers/duck'

const { Title } = Typography
const { Panel } = Collapse
const { Option } = Select;

interface CategoryTilesetProps {
  map: maplibre.Map
  regionId: string
  categoryId: string
  tileset: TileSet
  checked?: boolean
}

const CategoryTileset: FC<CategoryTilesetProps> = (props: CategoryTilesetProps) => {
  const dispatch = useDispatch()
  const [opacity, setOpacity] = useState(100)

  useEffect(() => {
    changeLayerOpacity(opacity)
  }, [opacity])

  useEffect(() => {
    if (props.checked) {
      changeLayerOpacity(opacity)
    } else if (props.checked !== undefined) {
      changeLayerOpacity(0)
    }
  }, [props.checked])

  useEffect(() => {
    if (opacity !== 100) {
      setOpacity(100)
    }
  }, [props.regionId])

  const handleSetOpacity = (value: number) => {
    if (!props.checked) {
      handleCheck(true)
    }
    setOpacity(value)
  }

  const handleCheck = (value: boolean) => {
    dispatch(checkTileset({ categoryId: props.categoryId, tilesetId: props.tileset.id, checked: value }))
  }

  const changeLayerOpacity = (value: number) => {
    const sourceName = `${props.regionId}-${props.categoryId}-${props.tileset.id}`
    const opacityProperty = props.tileset.service?.type === 'tile' || props.tileset.service?.type === 'image' || props.tileset.service?.type === 'wms' ? 'raster-opacity' :
      props.tileset.service?.type === 'geojson' ? 'fill-opacity' : undefined
    if (opacityProperty) {
      const interval = window.setInterval(() => {
        const sourceLoaded = props.map.getSource(sourceName)
        if (sourceLoaded) {
          props.map.setPaintProperty(sourceName + '-tiles', opacityProperty, value / 100)
          window.clearInterval(interval)
        }
      }, 200)
    }
  }

  return (
    <div>
      <Title level={5}>{props.tileset.name}</Title>
      <Row align='middle' wrap={false}>
        <Slider
          value={opacity}
          onChange={value => handleSetOpacity(value)}
          style={{
            width: '100%'
          }}
          trackStyle={{
            backgroundColor: props.checked ? '#177ddc' : '#606060'
          }}
        />
        <Checkbox
          checked={props.checked}
          onChange={event => handleCheck(event.target.checked)}
          style={{ marginLeft: '1rem' }}
        />
      </Row>
    </div>
  )
}

interface LayerCategoryProps {
  map: maplibre.Map
  regionId: string
  category: Category
}

const LayerCategory: FC<LayerCategoryProps> = (props: LayerCategoryProps) => {
  const dispatch = useDispatch()
  const chekcedTilesets = props.category.tilesets.map(tileset => tileset.checked)
  const checkedIndeterminate = props.category.tilesets.some(tileset => tileset.checked) && !props.category.tilesets.every(tileset => tileset.checked)

  useEffect(() => {
    if (chekcedTilesets.every(value => value) && !props.category.checked) {
      handleCheckCategory(true)
    } else if (chekcedTilesets.every(value => !value) && props.category.checked) {
      handleCheckCategory(false)
    }
  }, [chekcedTilesets]);

  const handleCheckCategory = (checked: boolean) => {
    if (checkedIndeterminate) {
      dispatch(checkCategory({ categoryId: props.category.id, checked: true }))
    } else {
      dispatch(checkCategory({ categoryId: props.category.id, checked: checked }))
    }
  }

  return (
    <Panel
      {...props}
      header={props.category.name}
      key={props.category.id}
      extra={
        <Checkbox
          onChange={(e) => handleCheckCategory(e.target.checked)}
          checked={props.category.checked}
          indeterminate={checkedIndeterminate}
          style={{ marginLeft: '1rem' }}
          onClick={event => {
            event.stopPropagation();
          }}
        />
      }
    >
      <div>
        {props.category.tilesets.map(tileset =>
          <CategoryTileset
            key={tileset.id}
            map={props.map}
            regionId={props.regionId}
            categoryId={props.category.id}
            tileset={tileset}
            checked={tileset.checked}
          />
        )}
      </div>
    </Panel>
  )
}

interface LayersProps {
  map: maplibre.Map
  layers: ILayers
  region: Region
  loading?: boolean
}

const Layers: FC<LayersProps> = (props: LayersProps) => {
  const dispatch = useDispatch()

  useEffect(() => {
    const firstCategory = props.region.categories[0]
    if (firstCategory) {
      dispatch(checkCategory({ categoryId: firstCategory.id, checked: true }))
    }
  }, [props.region.id])

  const handleSelectLayer = (layerId: string) => {
    const layer = props.layers.find(layer => layer.id === layerId)
    if (layer) {
      dispatch(selectRegion(layer))
    }
  }

  return (
    <Card className='map-layers'>
      <Title level={4}>Regions</Title>
      <Select className='select-layer' onSelect={handleSelectLayer} value={props.region?.id} loading={props.loading}>
        {props.layers.map(layer =>
          <Option key={layer.id} value={layer.id}>{layer.name}</Option>
        )}
      </Select>
      <Divider />
      <Title level={4}>Tile-sets</Title>
      <Collapse defaultActiveKey={props.region.categories[0].id}>
        {props.region.categories.map((category) =>
          <LayerCategory
            key={category.id}
            map={props.map}
            regionId={props.region.id}
            category={category}
          />
        )}
      </Collapse>
    </Card>
  )
}

export default Layers
