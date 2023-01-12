// React & React Native
import React, { ComponentType, FC, ReactElement } from 'react'

// Libraries
import { RenderResult, RenderOptions, render } from '@testing-library/react'

// Custom

type Props = {
  children: JSX.Element
}

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'queries'>,
): RenderResult =>
  render(ui, {
    ...options,
  })

export * from '@testing-library/react'

export { customRender as render }
