import { rest } from 'msw';

export const handlers = [
    rest.get("http://localhost/api/services.json", (req, res, ctx) => {
        return res(
            ctx.json([
                { "client_url": "/world-countries-tile/tile/{z}/{x}/{y}", "default_extent": [-20037508.3427892, -20037508.3427892, 20037508.3427892, 20037508.3427892], "default_height": 256, "default_url": "/world-countries-tile/tile/0/0/0", "default_width": 256, "key": "world-countries-tile", "legend_name": "World Countries tile-legend", "legend_url": "/world-countries-tile/legend", "name": "World Countries tile", "service_page_name": "/world-countries-tile-tile", "service_page_url": "/world-countries-tile", "type": "tile", "service_url": "/world-countries-tile/tile///" },
                { "client_url": "/world-countries-wms?bbox={XMIN},{YMIN},{XMAX},{YMAX}&width=256&height=256", "default_extent": [-20037508.3427892, -20037508.3427892, 20037508.3427892, 20037508.3427892], "default_height": 256, "default_url": "/world-countries-wms?bbox=-20037508.3427892,-20037508.3427892,20037508.3427892,20037508.3427892&width=256&height=256", "default_width": 256, "key": "world-countries-wms", "legend_name": "World Countries wms-legend", "legend_url": "/world-countries-wms/legend", "name": "World Countries wms", "service_page_name": "/world-countries-wms-wms", "service_page_url": "/world-countries-wms", "type": "wms", "service_url": "/world-countries-wms/wms" },
                { "client_url": "/world-countries-image/image/{XMIN}/{YMIN}/{XMAX}/{YMAX}/{width}/{height}", "default_extent": [-20037508.3427892, -20037508.3427892, 20037508.3427892, 20037508.3427892], "default_height": 256, "default_url": "/world-countries-image/image/-20037508.3427892/-20037508.3427892/20037508.3427892/20037508.3427892/256/256", "default_width": 256, "key": "world-countries-image", "legend_name": "World Countries image-legend", "legend_url": "/world-countries-image/legend", "name": "World Countries image", "service_page_name": "/world-countries-image-image", "service_page_url": "/world-countries-image", "type": "image", "service_url": "/world-countries-image/image//////" },
                { "client_url": "/world-countries-geojson/geojson", "default_extent": [-20037508.3427892, -20037508.3427892, 20037508.3427892, 20037508.3427892], "default_height": 256, "default_url": "/world-countries-geojson/geojson", "default_width": 256, "key": "world-countries-geojson", "legend_name": "World Countries geojson-legend", "legend_url": "/world-countries-geojson/legend", "name": "World Countries geojson", "service_page_name": "/world-countries-geojson-geojson", "service_page_url": "/world-countries-geojson", "type": "geojson", "service_url": "/world-countries-geojson/geojson" },
            ])
        )
    }),
    rest.get("http://localhost/api/layers.json", (req, res, ctx) => {
        return res(
            ctx.json([{
                "id": "1",
                "name": "New York",
                "bounds": [
                    [-73.18678109509695, 40.98028936172068],
                    [-74.69260189827584, 40.401680256687314]
                ],
                "categories": [{ "id": "1", "name": "nyc-boroughs-geojson + cities", "tilesets": [{ "id": "1", "name": "nyc-boroughs", "mapshaderKey": "nyc-boroughs-geojson" }, { "id": "2", "name": "world-cities", "mapshaderKey": "world-cities-tile" }] }, { "id": "2", "name": "nyc-boroughs + boundaries", "tilesets": [{ "id": "1", "name": "nyc-boroughs", "mapshaderKey": "nyc-boroughs-tile" }, { "id": "2", "name": "world-boundaries", "mapshaderKey": "world-boundaries-wms" }] }]
            }])
        )
    })
]