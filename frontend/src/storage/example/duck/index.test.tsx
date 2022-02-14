// Models
import { IExampleState } from '../models'

// Custom
import reducer, { actions, Types } from './index'

const initialState: IExampleState = {}

describe('Example Actions Creators', () => {
  it('Should create an action to handle error', () => {
    const expectedAction = {
      type: Types.FAILURE,
      payload: 'Error Message',
    }
    expect(actions.failure('Error Message')).toEqual(expectedAction)
  })

  it('Should create an action to trigger request', () => {
    const expectedAction = {
      type: Types.REQUEST,
    }
    expect(actions.request()).toEqual(expectedAction)
  })

  it('Should create an action to fulfill request', () => {
    const expectedAction = {
      type: Types.FULFILL,
    }
    expect(actions.fulfill()).toEqual(expectedAction)
  })

  it('Should create an action to update state successfuly', () => {
    const payload: IExampleState = {
      example: 'Test',
    }
    const expectedAction = {
      type: Types.SUCCESS,
      payload,
    }
    expect(actions.success(payload)).toEqual(expectedAction)
  })
})

describe('Example Reducer', () => {
  it('Should return the initial state', () => {
    expect(reducer(undefined, undefined)).toEqual(initialState)
  })

  it('Should handle error message', () => {
    const error = 'Error Message'
    expect(reducer(undefined, actions.failure(error))).toEqual({
      ...initialState,
      error,
    })
  })

  it('Should start content request', () => {
    expect(reducer(undefined, actions.request())).toEqual({
      ...initialState,
      loading: true,
    })
  })

  it('Should finish content request', () => {
    expect(reducer(undefined, actions.fulfill())).toEqual({
      ...initialState,
      loading: false,
    })
  })

  it('Should update state successfully', () => {
    const payload: IExampleState = {
      example: 'Test',
    }
    expect(reducer(undefined, actions.success(payload))).toEqual({
      ...initialState,
      ...payload,
    })
    expect(reducer(undefined, actions.success(payload))).toHaveProperty(
      'example',
    )
  })
})
