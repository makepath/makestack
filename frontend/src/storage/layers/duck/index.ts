// Models
import { IAction } from 'lib/redux/models'
import { ELayersActionTypes, ILayersState, Region, Legend, TileSet, IActionCheckTilesetPayload, IActionCheckCategoryPayload, MapshaderService } from '../models'

// ACTION TYPES
export const Types = {
  FAILURE: ELayersActionTypes.FAILURE,
  FULFILL: ELayersActionTypes.FULFILL,
  REQUEST: ELayersActionTypes.REQUEST,
  SUCCESS: ELayersActionTypes.SUCCESS,
  ADD_SERVICES: ELayersActionTypes.ADD_SERVICES,
  GET_SERVICES: ELayersActionTypes.GET_SERVICES,
  GET_LAYERS: ELayersActionTypes.GET_LAYERS,
  GET_LEGEND: ELayersActionTypes.GET_LEGEND,
  UPDATE_LEGENDS: ELayersActionTypes.UPDATE_LEGENDS,
  SELECT_REGION: ELayersActionTypes.SELECT_REGION,
  CHECK_CATEGORY: ELayersActionTypes.CHECK_CATEGORY,
  CHECK_TILESET: ELayersActionTypes.CHECK_TILESET,
}

// INITIAL STATE
const initialState: ILayersState = { layers: [], legends: {} }

// REDUCER
export default (
  state: ILayersState = initialState,
  action?: IAction,
): ILayersState => {
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
    case Types.ADD_SERVICES:
      return {
        ...state,
        layers: state.layers.map(layer => ({
          ...layer,
          categories: layer.categories.map(category => ({
            ...category,
            tilesets: category.tilesets.map(tileset => ({
              ...tileset,
              service: action.payload.find((service: MapshaderService) => service.key === tileset.mapshaderKey)
            }))
          }))
        }))
      }
    case Types.UPDATE_LEGENDS:
      return {
        ...state,
        legends: {
          ...state.legends,
          [action.payload.layerId]: action?.payload.legend
        }
      }
    case Types.SELECT_REGION:
      return {
        ...state,
        selectedRegion: action.payload
      }
    case Types.CHECK_CATEGORY:
      if (state.selectedRegion) {
        return {
          ...state,
          selectedRegion: {
            ...state.selectedRegion,
            categories: state.selectedRegion.categories.map(category => ({
              ...category,
              checked: category.id === action.payload.categoryId ? action.payload.checked : category.checked,
              tilesets: category.id === action.payload.categoryId ? category.tilesets.map(tileset => ({
                ...tileset,
                checked: action.payload.checked
              })) : category.tilesets
            }))
          }
        }
      }
      return {
        ...state
      }
    case Types.CHECK_TILESET:
      if (state.selectedRegion) {
        return {
          ...state,
          selectedRegion: {
            ...state.selectedRegion,
            categories: state.selectedRegion.categories.map(category => ({
              ...category,
              tilesets: category.id === action.payload.categoryId ? category.tilesets.map(tileset => ({
                ...tileset,
                checked: tileset.id === action.payload.tilesetId ? action.payload.checked : tileset.checked,
              })) : category.tilesets
            }))
          }
        }
      }
      return {
        ...state
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

export const success = (payload: Partial<ILayersState>): IAction => {
  return {
    type: Types.SUCCESS,
    payload,
  }
}

export const addServices = (payload: MapshaderService[]): IAction => {
  return {
    type: Types.ADD_SERVICES,
    payload,
  }
}

export const getServices = (): IAction => {
  return {
    type: Types.GET_SERVICES,
  }
}

export const getLayers = (): IAction => {
  return {
    type: Types.GET_LAYERS,
  }
}

export const getLegend = (payload: TileSet): IAction => {
  return {
    type: Types.GET_LEGEND,
    payload
  }
}

export const updateLegends = (payload: { layerId: string, legend: Legend }): IAction => {
  return {
    type: Types.UPDATE_LEGENDS,
    payload
  }
}

export const selectRegion = (payload: Region): IAction => {
  return {
    type: Types.SELECT_REGION,
    payload
  }
}

export const checkCategory = (payload: IActionCheckCategoryPayload): IAction => {
  return {
    type: Types.CHECK_CATEGORY,
    payload
  }
}

export const checkTileset = (payload: IActionCheckTilesetPayload): IAction => {
  return {
    type: Types.CHECK_TILESET,
    payload
  }
}

export const actions = {
  failure,
  fulfill,
  request,
  success,
}
