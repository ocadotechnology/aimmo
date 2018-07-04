[![js-standard-style](https://cdn.rawgit.com/standard/standard/master/badge.svg)](https://github.com/standard/standard)



# AI:MMO Frontend

## Description

This folder contains the frontend for the AI:MMO game. It is a single page application using [React](https://reactjs.org/). We use [Redux](https://redux.js.org/) for state management and [redux-observable](https://redux-observable.js.org/) for handling our side effects (e.g. asynchronous calls). To learn more about how we connect all of these together, feel free to check out our [How does it all work](#how-does-it-all-work) section.

## Installation for Contributors

### Requirements

- [Node](https://nodejs.org/en/download/)
- [Parcel](https://parceljs.org/)
- [yarn](https://yarnpkg.com/en/)

### Build dependencies

Once you have cloned this repository, run the command below in this folder:

```
yarn
```

## Usage

### Standalone

It's possible to run the frontend by itself. To do so, run the command below in this folder. **Note:** the Unity WebGL build will not show in standalone mode and you will need to run the project with Django.

```
parcel index.html
```

### With Django

Our Django runner calls `djangoBundler.js` when running the project for you so nothing special needs to done! Run this command in the root of this repository (make sure you are in your virtualenv):

```
./run.py -k
```

`djangoBundler.js` is a custom `parcel-bundler` we use to make sure we generate a Django template as an entry point for the React code.

### Running Tests

```
yarn test
```

## Contributing

- tests
- standard style guide (state exceptions)


## How does it all work?

### Prequisite Reading

If you are new to React and Redux we recommend reading these resources:

- [React tutorial](https://reactjs.org/tutorial/tutorial.html)
- [Thinking in React](https://reactjs.org/docs/thinking-in-react.html)
- [Redux and React tutorial](https://www.valentinog.com/blog/react-redux-tutorial-beginners/)

In order to make sure our project structure is scalable we use [re-ducks](https://medium.freecodecamp.org/scaling-your-redux-app-with-ducks-6115955638be).

### Optional reading

The links here aren't necessary for helping you contribute straight away but they will help you out as you get more comfortable with our project:

- [Jest testing cheatsheet](https://devhints.io/jest)
- [Redux Observables](https://redux-observable.js.org/)
- [RxJS Marble Testing](https://github.com/ReactiveX/rxjs/blob/master/doc/writing-marble-tests.md)

### How we integrate with Django

Coming soon...

### Technology Stack

- React
- Redux
- redux-observable
- styled-components

#### For developers

- Parcel
- StandardJS
- Babel

#### For testing

- Jest
- Enzyme

### Building for Production

Coming soon...
