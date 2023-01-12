// Models
import { IBaseState } from 'lib/redux/models'

export type Example = string

export enum EExampleActionTypes {
  FAILURE = 'EXAMPLE/FAILURE',
  FULFILL = 'EXAMPLE/FULFILL',
  REQUEST = 'EXAMPLE/REQUEST',
  SUCCESS = 'EXAMPLE/SUCCESS',
}

export interface IExampleState extends IBaseState {
  example?: Example
}
