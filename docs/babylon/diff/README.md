## DiffHandling

`DiffHandling` is an interface for implementing the functions that add, edit and delete entities.

```Typescript
export interface DiffHandling {
    add(item: DiffItem): void;
    edit(item: DiffItem): void;
    delete(item: DiffItem): void;
}
```

Each entity manager should implement `add`, `edit` and `delete` to update its configuration according to the current game state.


## DiffProcessor

`DiffProcessor` is the class that handles differences between game states and updates the manager configuration according to them. It uses a `DiffHandling` handler that receives the full difference between game states and updates the correspondent entity manager's configuration.
