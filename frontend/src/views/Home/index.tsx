// React
import React, { FC } from 'react'
import './index.css';
import Map from 'components/Map';
import Page from 'views/Page';

// Custom

const Home: FC = () => {
  return (
    <Page className="homepage">
      <Map />
    </Page>
  )
}

export default Home
