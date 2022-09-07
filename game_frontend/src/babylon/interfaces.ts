import { DiffResult, DiffItem } from './diff'

/***
 * An interface for implementing the objects that are part of the game world.
 */
export interface GameNode {
  object: any
}

/**
 * Used to enforce the methods needed by the `DiffProcessor`.
 */
export interface DiffHandling {
  add(item: DiffItem): void
  edit(item: DiffItem): void
  remove(item: DiffItem): void
}

/**
 * Calls the add, edit, and remove methods of its handler on a given `DiffResult`.
 * Makes sure these methods happen in a certain order. (remove -> edit -> add)
 */
export class DiffProcessor {
  handler: DiffHandling

  constructor(handler: DiffHandling) {
    this.handler = handler
  }

  handleDifferences(differences: DiffResult): void {
    for (const entity of differences.deleteList) {
      this.handler.remove(entity)
    }
    for (const entity of differences.editList) {
      this.handler.edit(entity)
    }
    for (const entity of differences.addList) {
      this.handler.add(entity)
    }
  }
}
