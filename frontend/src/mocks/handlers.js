import { rest } from 'msw';
import services from './data/services.json'
import layers from './data/layers.json'

export const handlers = [
    rest.get("http://localhost/api/services.json", (req, res, ctx) => {
        return res(
            ctx.json(services)
        )
    }),
    rest.get("http://localhost/api/layers.json", (req, res, ctx) => {
        return res(
            ctx.json(layers)
        )
    })
]