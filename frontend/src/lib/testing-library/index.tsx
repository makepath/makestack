// React & React Native
import React, { FC, ReactElement } from 'react'

// Libraries
import { RenderOptions, render } from '@testing-library/react'
import { Provider } from 'react-redux'
import store from 'lib/redux'

// Custom

const AllTheProviders: FC = ({ children }) => {
  return (
    <Provider store={store}>
      {children}
    </Provider>
  )
}

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>,
) => render(ui, { wrapper: AllTheProviders, ...options })

export * from '@testing-library/react'
export { customRender as render }
