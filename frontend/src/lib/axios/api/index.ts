import axios, { AxiosInstance } from 'axios'

const api: AxiosInstance = axios.create({
  baseURL: window.location.origin.includes("3000") ? "http://localhost:8000/api/v1/" : "/api/v1/",
  timeout: 5000,
});

const geoserverApi: AxiosInstance = axios.create({
  baseURL: window.location.origin.includes("3000") ? "http://localhost:8000/geoserver/" : "/geoserver/",
  timeout: 20000,
});

const toCamel = (s: string) => {
  return s.replace(/([-_][a-z])/ig, ($1) => {
    return $1.toUpperCase()
      .replace('-', '')
      .replace('_', '');
  });
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const isArray = function (a: any) {
  return Array.isArray(a);
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const isObject = function (o: any) {
  return o === Object(o) && !isArray(o) && typeof o !== 'function';
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const keysToCamel = function (o: Record<string, any>): Record<string, any> {
  if (isObject(o)) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const n = {} as any;
    Object.keys(o)
      .forEach((k) => {
        n[toCamel(k)] = keysToCamel(o[k]);
      });
    return n;
  } else if (isArray(o)) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return o.map((i: Record<string, any>) => {
      return keysToCamel(i);
    });
  }
  return o;
};

export const staticApi: AxiosInstance = axios.create({
  baseURL: window.location.origin,
  timeout: 60000,
});

export default api
