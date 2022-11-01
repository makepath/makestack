// React
import React, { FC, useEffect } from 'react'
import './index.css';
import Page from 'views/Page';
import { Card, Spin } from 'antd';
import Map from 'components/Map';
import { useDispatch, useSelector } from 'react-redux';
import { getLayers, getServices, selectRegion } from 'storage/layers/duck';
import { ILayersState } from 'storage/layers/models';
import IStore from 'lib/redux/models';
import Logo from '../../assets/mapshader-logo.svg'

// Custom

const Home: FC = () => {
  const dispatch = useDispatch()
  const state = useSelector<IStore, ILayersState>((state) => state.layers)
  const { layers, loading } = useSelector<IStore, ILayersState>((state) => state.layers);

  useEffect(() => {
    dispatch(getLayers())
    dispatch(getServices())
  }, [])

  useEffect(() => {
    if (layers.length > 0 && layers[0].categories[0].tilesets[0].service) {
      dispatch(selectRegion(layers[0]))
    }
  }, [layers])
  
  return (
    <Page className="homepage">
      <Card className="logo" bodyStyle={{ padding: '0.75rem' }}>
          <img src={Logo} alt="mapshader" />
        </Card>
        {loading || layers.length === 0 || !state.selectedRegion ?
          <Spin /> :
          <Map {...state} />
        }
    </Page>
  )
}

export default Home
