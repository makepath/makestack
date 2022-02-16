import api, { publicApi, keysToCamel } from '../../lib/axios/api'
import { TileSet, Legend } from 'storage/layers/models';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const getServicesService = async (): Promise<any> => {
  const response = await publicApi.get('/api/services.json')
  return keysToCamel(response.data)
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const getLayersService = async (): Promise<any> => {
  const response = await publicApi.get('/api/layers.json')
  return response.data
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const getLegendService = async (layer: TileSet): Promise<any> => {
  const response = await api.get(`${layer.name}-tile/legend`)
  return response.data as Legend
};