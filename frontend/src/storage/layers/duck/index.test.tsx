// Models
import { IActionCheckCategoryPayload, IActionCheckTilesetPayload, ILayersState, Region } from '../models'

// Custom
import reducer, { actions, checkCategory, checkTileset, selectRegion, Types } from './index'

const initialState: ILayersState = { layers: [], legends: {} }

describe('Layer Actions Creators', () => {
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
    const payload: Partial<ILayersState> = {
      layers: [{
        "id": "1",
        "name": "New York",
        "bounds": [
          [-73.18678109509695, 40.98028936172068],
          [-74.69260189827584, 40.401680256687314]
        ],
        "categories": [{
          "id": "1",
          "name": "nyc-boroughs-geojson + cities",
          "tilesets": [{
            "id": "1",
            "name": "nyc-boroughs",
            "mapshaderKey": "nyc-boroughs-geojson"
          }]
        }]
      }],
    }
    const expectedAction = {
      type: Types.SUCCESS,
      payload,
    }
    expect(actions.success(payload)).toEqual(expectedAction)
  })

  it('Should create an action to select a region successfuly', () => {
    const payload: Region = {
      "id": "1",
      "name": "New York",
      "bounds": [
        [-73.18678109509695, 40.98028936172068],
        [-74.69260189827584, 40.401680256687314]
      ],
      "categories": [{
        "id": "1",
        "name": "nyc-boroughs-geojson + cities",
        "tilesets": [{
          "id": "1",
          "name": "nyc-boroughs",
          "mapshaderKey": "nyc-boroughs-geojson"
        }]
      }]
    }
    const expectedAction = {
      type: Types.SELECT_REGION,
      payload,
    }
    expect(selectRegion(payload)).toEqual(expectedAction)
  })

  it('Should create an action to check a category successfuly', () => {
    const payload: IActionCheckCategoryPayload = {
      "categoryId": "1",
      "checked": true,
    }
    const expectedAction = {
      type: Types.CHECK_CATEGORY,
      payload,
    }
    expect(checkCategory(payload)).toEqual(expectedAction)
  })

  it('Should create an action to check a tileset successfuly', () => {
    const payload: IActionCheckTilesetPayload = {
      "categoryId": "1",
      "tilesetId": "1",
      "checked": true,
    }
    const expectedAction = {
      type: Types.CHECK_TILESET,
      payload,
    }
    expect(checkTileset(payload)).toEqual(expectedAction)
  })
})

describe('Layer Reducer', () => {
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
    const payload: Partial<ILayersState> = {
      layers: [],
    }
    expect(reducer(undefined, actions.success(payload))).toEqual({
      ...initialState,
      ...payload,
    })
    expect(reducer(undefined, actions.success(payload))).toHaveProperty(
      'layers',
    )
  })
})
