// Libraries
import { SagaIterator } from 'redux-saga'
import { all, fork } from 'redux-saga/effects'

// Custom
import exampleSagas from 'storage/example/saga'

export default function* rootSaga(): SagaIterator {
  yield all([fork(exampleSagas)])
}
