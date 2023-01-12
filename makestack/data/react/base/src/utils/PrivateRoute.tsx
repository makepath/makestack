import React, { ReactElement } from 'react'
import { Route, Navigate } from 'react-router-dom'

interface Props {
  element: React.ReactElement
  path: string
}

const PrivateRoute = ({ element, path }: Props): ReactElement => {
  const token = localStorage.getItem('access_token')

  const renderComponent = () => {
    if (token) {
      return (
        <Route
          path={path}
          element={element}
        />
      )
    }
    return <Navigate to="/" />
  }

  return renderComponent()
}

export default PrivateRoute
