import React from 'react'
import { render } from '@testing-library/react'
import App from './App'


describe('Tests for the whole application', () => {
  it('should render the application', () => {
    const { container } = render(<App />)
    expect(container).toBeTruthy()
  })
})
