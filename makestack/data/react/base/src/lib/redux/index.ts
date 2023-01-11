// Libraries
import { applyMiddleware, compose, createStore } from 'redux'
import createSagaMiddleware, { SagaMiddleware } from 'redux-saga'
import { createLogger } from 'redux-logger'


// Custom
import appReducer from './reducers'
import sagas from './sagas'

const sagaMiddleware: SagaMiddleware = createSagaMiddleware()

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const middlewares: Array<any> = [sagaMiddleware];

declare global {
  interface Window {
    __REDUX_DEVTOOLS_EXTENSION_COMPOSE__?: typeof compose
  }
}

if (process.env.NODE_ENV === 'development') {
  const logger = createLogger({ collapsed: true });
  middlewares.push(logger);
}

const composeEnhancers: typeof compose =
  window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const store = createStore<any, any, any, any>(
  appReducer,
  composeEnhancers(applyMiddleware(...middlewares))
)

sagaMiddleware.run(sagas)

export default store
