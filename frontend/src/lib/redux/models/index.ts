// Models
import { ILayersState } from 'storage/layers/models'

export interface IAction {
  type: string
  payload?: any
}

export interface IBaseState {
  error?: string
  loading?: boolean
  refreshing?: boolean
}

export default interface IStore {
  layers: ILayersState
}