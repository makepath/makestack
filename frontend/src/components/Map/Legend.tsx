// React
import React, { FC } from 'react'
import { Card, Row } from 'antd'
import { Legend as ILegend } from 'storage/layers/models'

// Custom
import './Legend.css'

interface LegendProps {
  legend: ILegend
}

const Legend: FC<LegendProps> = (props: LegendProps) => {
  return (
    <Card className='map-legend'>
      Legend
      {props.legend.map(legendItem => {
        <Row>
          <p>{legendItem.label} | {legendItem.value} | {legendItem.color}</p>
        </Row>
      })}
    </Card>
  )
}

export default Legend
