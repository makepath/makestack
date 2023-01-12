// React
import React, { FC } from 'react'
import './index.css';
import { Layout } from 'antd';
import Map from 'components/Map';

// Custom
const { Content } = Layout;

const Home: FC = () => {
  return (
    <Layout className="homepage">
      <Content>
        <Map />
      </Content>
    </Layout>
  )
}

export default Home
