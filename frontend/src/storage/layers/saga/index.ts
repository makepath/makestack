// Libraries
import { SagaIterator } from '@redux-saga/types'
import { all, call, put, takeEvery, takeLatest } from 'redux-saga/effects'
import { IActionGetLegend, Layers, Legend, MapshaderService } from '../models'
import { Types, actions, addServices, updateLegends } from '../duck';
import { getServicesService, getLayersService, getLegendService } from 'services/layers';

const { failure, fulfill, request, success } = actions

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function* getServicesSaga(): Generator<any, any, any> {
  yield put(request())
  try {
    const services: MapshaderService[] = yield call(getServicesService)
    if (services) {
      yield put(addServices(services))
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (error: any) {
    yield put(failure(error.message))
  } finally {
    yield put(fulfill())
  }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any,
export function* getLayersSaga(): Generator<any, any, any> {
  yield put(request())
  try {
    const layers: Layers = yield call(getLayersService)
    if (layers) {
      yield put(success({
        layers: layers
      }))
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (error: any) {
    yield put(failure(error.message))
  } finally {
    yield put(fulfill())
  }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function* getLegendSaga(action: IActionGetLegend): Generator<any, any, any> {
  yield put(request())
  try {
    const legend: Legend = yield call(getLegendService, action.payload)
    if (legend) {
      yield put(updateLegends({
        layerId: action.payload.id,
        legend: legend
      }))
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (error: any) {
    yield put(failure(error.message))
  } finally {
    yield put(fulfill())
  }
}

export default function* layersSagas(): SagaIterator {
  yield all([
    takeLatest(Types.GET_SERVICES, getServicesSaga),
    takeLatest(Types.GET_LAYERS, getLayersSaga),
    takeEvery(Types.GET_LEGEND, getLegendSaga),
  ])
}
