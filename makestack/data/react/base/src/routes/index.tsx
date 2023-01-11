// Models
import { Route as TRoute } from 'lib/models'

// React
import React, { FC } from 'react'

// Libraries
import { Routes, BrowserRouter as Router, Route } from 'react-router-dom'

// Custom
import PrivateRoute from '../utils/PrivateRoute'
import paths from './paths'

const RouterContainer: FC = () => {
  return (
    <Router>
      <Routes>
        {paths.map((route: TRoute) => {
          if (route.private) {
            return (
              <PrivateRoute
                key={route.path}
                element={<route.component />}
                path={route.path}
              />
            );
          }
          return (
            <Route
              key={route.path}
              path={route.path}
              element={<route.component />}
            />
          );
        })}
      </Routes>
    </Router>
  );
};

export default RouterContainer
