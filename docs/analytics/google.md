# Analytics 2: Eletric Googaloo

This document will show you how to create new google analytics events for Kurono.

Google analytics events in React+Redux are done through the use of Epics. Epics are functions which take a stream of actions and return another stream of actions.

This means that if you're looking to add new analytics event you will need to find what action relates to what you are measuring. Below is an example used to measure how often the "Run code" button is pressed in the code editor.

```Javascript
const postCodeAnalyticsEpic = action$ =>
  action$.pipe(
    ofType(types.POST_CODE_REQUEST),
    mapTo(analyticActions.sendAnalyticsEvent('Kurono', 'Click', 'Run Code'))
  )
```

Here, we can see that the function `postCodeAnalyticsEpic` takes in an action, checks that the action is the one we want, and if it is, maps the action to our analytics event action. Note, we must include `ofType(types.POST_CODE_REQUEST)` as in Redux actions are passed through to all of the epics, so we need to make sure we're only dealing with the ones we're interested in.

Finally, there are a number of arguments passed into the `sendAnalyticsEvent()` action. These correspond to what the action will appear as on the Google analytics dashboard, so discussing with whoever relies on this the most (Most likely the PO [Product Owner]) to agree on how to catagorise the event would be advisable.
