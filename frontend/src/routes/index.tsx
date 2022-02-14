// Models
import { Route as TRoute } from 'lib/models'

// React
import React, { FC } from 'react'

// Libraries
import { Switch, BrowserRouter as Router, Route } from 'react-router-dom'

// Custom
import PrivateRoute from '../utils/PrivateRoute'
import paths from './paths'

const RouterContainer: FC = () => {
  return (
    <Router>
      <Switch>
        {paths.map((route: TRoute) => {
          if (route.private) {
            return (
              <PrivateRoute
                exact
                component={route.component}
                path={route.path}
              />
            );
          }
          return (
            <Route
              exact
              path={route.path}
              component={route.component}
              key={route.path}
            />
          );
        })}
      </Switch>
    </Router>
  );
};

export default RouterContainer
