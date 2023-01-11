// Models
import { IAction } from 'lib/redux/models'
import { EExampleActionTypes, IExampleState } from '../models'

// ACTION TYPES
export const Types = {
  FAILURE: EExampleActionTypes.FAILURE,
  FULFILL: EExampleActionTypes.FULFILL,
  REQUEST: EExampleActionTypes.REQUEST,
  SUCCESS: EExampleActionTypes.SUCCESS,
}

// INITIAL STATE
const initialState: IExampleState = {}

// REDUCER
export default (
  state: IExampleState = initialState,
  action?: IAction,
): IExampleState => {
  switch (action?.type) {
    case Types.FAILURE:
      return {
        ...state,
        error: action.payload,
      }
    case Types.FULFILL:
      return {
        ...state,
        loading: false,
      }
    case Types.REQUEST:
      return {
        ...state,
        loading: true,
      }
    case Types.SUCCESS:
      return {
        ...state,
        ...action?.payload,
      }
    default:
      return state
  }
}

// ACTIONS

export const failure = (payload: string): IAction => {
  return {
    type: Types.FAILURE,
    payload,
  }
}

export const fulfill = (): IAction => {
  return {
    type: Types.FULFILL,
  }
}

export const request = (): IAction => {
  return {
    type: Types.REQUEST,
  }
}

export const success = (payload: IExampleState): IAction => {
  return {
    type: Types.SUCCESS,
    payload,
  }
}

export const actions = {
  failure,
  fulfill,
  request,
  success,
}
