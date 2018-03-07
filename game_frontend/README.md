[![js-standard-style](https://cdn.rawgit.com/standard/standard/master/badge.svg)](https://github.com/standard/standard)

# AI:MMO Frontend

## Description

This folder contains the frontend for the AI:MMO game. It is written in single page application written in [React](https://reactjs.org/). We use [Redux](https://redux.js.org/) for state management and [redux-observable](https://redux-observable.js.org/) for handling our side effects (e.g. asynchronous calls). To learn more about how we connect all of these together, feel free to check out our [How does it all work](#how-does-it-all-work) section.

## Installation for Contributors

### Prerequisites

- [Node](https://nodejs.org/en/download/)
- [Parcel](https://parceljs.org/)
- [yarn](https://yarnpkg.com/en/)

### Build dependencies

Once you have cloned this repository, open up your terminal and `cd` into this folder and run:

```
yarn
```

## Usage

### Standalone

It's possible to run the frontend by itself. To do so, run the command below in this folder:

```
parcel index.html
```

### With Django

Coming soon...

### Running Tests

```
yarn test
```

## How does it all work?

A quick outline of the sequence of calls and state management can be useful to understand the
way Redux, RxJS and React can work together to provide our front-end efficiently.

We use [re-ducks](https://medium.freecodecamp.org/scaling-your-redux-app-with-ducks-6115955638be) for our architecture.

### HTML Entry
The entry point to our application is an `index.html` file. This lives at the root of the front-end folder.
The most important part is that it defines a javascript index
page written in React by a `<script>` tag.

### React Entry
The `index.js` file living in the `src` folder will be responsible for a couple of
things:
* It sets the initial state for each of the reducers (see reducers)
* Configures the store using the global initial state mentioned above (see stores)
* Sets the root JSX code, usually our entry container for the page.
* And finally renders the JSX code to the `root` HTML element.

### Containers
As the JSX code is rendered, usually an initial container is specified
there so let's dig deeper (see "a bit on containers vs components")

We tend to structure containers into different folders, then have an `index.js` entry point for each
individual one. This file will map the current global state and the dispatch to the props of the component.
This is done by a `connect(mapStateToPropsFunction, mapDispatchToPropsFunction)(ComponentName)` call.
These functions should be defined there. They should return a *JSON* with the key as
the name of the prop, and the appropriate state or dispatch assigned to it.
This way every time the state changes, it will be connected to the local prop of the component.

We may want to add some user interaction with the state here, for example some logic when
a user presses a button. To do this particular example we can assign a action dispatch function
(connected to the component in the `connect` mentioned above by assigning it to a prop) to a `onClick`
function. This way every time a user presses this button, an action dispatch will be called.


### Actions & Types
Actions are part of the Redux architecture. They usually live in `redux/featutes/FeatureName/actions.js`.
They are simple data elements which are dispatched to the middleware. We define action
types in a file called `types.js`, for example:

``const FETCH_MOVIES = 'features/GhibliMovies/FETCH_MOVIES'``.

These types get imported to the `actions.js` file and get dispatched with the
JSON under the appropriate function. Therefore, the user clicking the button will be taken
to this action dispatch, which refers to the type from `types.js` file.


### A bit on containers vs components

A nice way to think of these is to think of them as smart and dumb components.
A container is a *smart* piece of logic, a component is *not*. Smart in this
context refers to state management. **Components are purely
for UI rendering. They do not access state or alter it**. On the other hand the
containers are **smart, they alter the state in one way or another.**

### Middleware

Actions that get dispatched usually pass through some kind of middleware. In our
case this will `redux-observable` which provide **epics**. We can check which
type is passed into the middlware by `action$.ofType()` and write appropriate logic
in *rxJS*. The result of this is *usually* passed on to the reducer.

### Reducer

Arguably the most important piece of the whole architecture. This specifies how the
application's **state changes** in response to payloads of informations received by
**actions**. Reducers do not *mutate* the state, they create *new* state. Remember,
actions only describe that *something happened*, but don't describe how *application's
state changes*.

In our case we return the new state based on the action (further passed by the
middleware epic).

This is mapped to the state as the reducer was combined with other reducers to form
a store at the start entry of our application (see above).

### Re-rendering

Because our state has been changed and because we have connected
`mapStateToProps` to the container; then our props change and the
React DOM appropriately updates the DOM, thus showing a response from the
page to user action.
