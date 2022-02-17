// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom/extend-expect';
import { server } from './mocks/server';

beforeAll(() => server.listen())

afterEach(() => server.resetHandlers())

afterAll(() => server.close())

if (typeof window.URL.createObjectURL === 'undefined') {
  const fn = (obj: Blob | MediaSource): string => {
    // Do nothing
    // Mock this function for mapbox-gl to work
    return ''
  };
  window.URL.createObjectURL = fn
}