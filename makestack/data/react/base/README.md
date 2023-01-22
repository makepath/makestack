# Project Created based on Heeds Web Template.

## Available commands

In the project directory, you can run:

### `make start-frontend-dev`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `make frontend-test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `make frontend-build`

Builds the app for production to the `build` folder and copies it to the backend folder so it is hosted directly by Django on staging/production.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.



## Project Structure


`src/assets/` - Static files used by the application
`src/components/` - Here you can add custom React components. Structure this folder as you see fit
`src/declarations/` - TypeScript type declarations
`src/hooks/` - Here you can add custom hooks
`src/lib/` - Third-party libraries configurations
`src/routes/` - React Router configuration
`src/services/` - Async functions for fetching data from configured services, this functions are called using redux-saga to handle all the states between request and response from the server
`src/storage/` - Redux store models actions and sagas
`src/utils/` - Utility components and functions
`src/views/` - Page components rendered by each route at `src/routes/paths.js`

## Adding layers to the map

### TODO: Add code examples for adding new sorces and layers to the map
