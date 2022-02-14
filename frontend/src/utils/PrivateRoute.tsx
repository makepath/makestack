import React, { ReactElement } from 'react'
import { Route, Redirect } from 'react-router-dom'

interface Props {
  exact?: boolean
  component: React.FunctionComponent
  path: string
}

const PrivateRoute = ({ exact, component: Component, path }: Props): ReactElement => {
  const token = localStorage.getItem('access_token')

  const renderComponent = () => {
    if (token) {
      return (
        <Route
          exact={exact ? exact : false}
          path={path}
          component={Component}
        />
      )
    }
    return <Redirect to="/" />
  }

  return renderComponent()
}

export default PrivateRoute
