// Models
import IStore, { IAction } from 'lib/redux/models'

// Libraries
import { combineReducers, Reducer } from 'redux'

// Custom
import exampleReducer from 'storage/example/duck'

const appReducer: Reducer<IStore, IAction> = combineReducers({
  example: exampleReducer,
})

export default appReducer
