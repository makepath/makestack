// React
import React, { FC } from 'react'
import './Page.css';
import { Layout } from 'antd';

// Custom
const { Content } = Layout;

interface PageProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
}

const Page: FC<PageProps> = (props: PageProps) => {
  const { children, ...contentProps } = props
  return (
    <Layout className="homepage">
      <Content {...contentProps}>
        {children}
      </Content>
    </Layout>
  )
}

export default Page
