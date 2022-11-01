// Models
import IStore, { IAction } from 'lib/redux/models'

// Libraries
import { combineReducers, Reducer } from 'redux'

// Custom
import layersReducer from 'storage/layers/duck'

const appReducer: Reducer<IStore, IAction> = combineReducers({
  layers: layersReducer,
})

export default appReducer
