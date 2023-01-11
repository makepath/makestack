// Models
import { IExampleState } from 'storage/example/models'

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
  example: IExampleState
}