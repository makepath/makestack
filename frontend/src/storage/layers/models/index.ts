// Models
import { IBaseState, IAction } from 'lib/redux/models'

export enum ELayersActionTypes {
  FAILURE = 'LAYERS/FAILURE',
  FULFILL = 'LAYERS/FULFILL',
  REQUEST = 'LAYERS/REQUEST',
  SUCCESS = 'LAYERS/SUCCESS',
  ADD_SERVICES = 'LAYERS/ADD_SERVICES',
  GET_SERVICES = 'LAYERS/GET_SERVICES',
  GET_LAYERS = 'LAYERS/GET_LAYERS',
  GET_LEGEND = 'LAYERS/GET_LEGEND',
  UPDATE_LEGENDS = 'LAYERS/UPDATE_LEGENDS',
  SELECT_REGION = 'LAYERS/SELECT_REGION',
  CHECK_CATEGORY = 'LAYERS/CHECK_CATEGORY',
  CHECK_TILESET = 'LAYERS/CHECK_TILESET',
}

export interface TileSet {
  id: string,
  name: string,
  mapshaderKey: string
  service?: MapshaderService,
  checked?: boolean
}

export interface MapshaderService {
  key: string
  name: string
  type: "tile" | "image" | "geojson" | "wms"
  clientUrl: string
  defaultExtent: [number, number, number, number]
  defaultHeight: number
  defaultWidth: number
  legendName: string
  legendUrl: string
}

export interface Category {
  id: string
  name: string
  checked?: boolean
  tilesets: TileSet[]
}

export interface Region {
  id: string
  name: string
  categories: Category[]
  bounds: [[number, number], [number, number]],
}

export type Layers = Region[]

export interface Legends {
  [id: string]: Legend
}

export type Legend = {
  label: string
  value: number
  color: string
}[]


export interface IActionGetServices extends IAction {
  type: ELayersActionTypes.GET_SERVICES
}

export interface IActionGetLayers extends IAction {
  type: ELayersActionTypes.GET_LAYERS
}

export interface IActionGetLegend extends IAction {
  type: ELayersActionTypes.GET_LEGEND
  payload: TileSet
}

export interface IActionSelectRegion extends IAction {
  type: ELayersActionTypes.SELECT_REGION
  payload: Region
}

export interface IActionCheckCategoryPayload {
  categoryId: string
  checked: boolean
}

export interface IActionCheckCategory extends IAction {
  type: ELayersActionTypes.SELECT_REGION
  payload: boolean
}


export interface IActionCheckTilesetPayload {
  categoryId: string
  tilesetId: string
  checked: boolean
}

export interface IActionCheckTileset extends IAction {
  type: ELayersActionTypes.SELECT_REGION
  payload: boolean
}

export interface ILayersState extends IBaseState {
  layers: Layers
  legends: Legends
  selectedRegion?: Region
}
