import { Environment } from './environment/environment'
import { DiffResult, DiffItem } from './diff'

export interface GameNode {
    object: any;
    setup(environment: Environment): void;
}

/**
 * Used to enforce the methods needed by the `DiffProcessor`.
 */
export interface DiffHandling {
    add(item: DiffItem): void;
    edit(item: DiffItem): void;
    remove(item: DiffItem): void;
}

/**
 * calls the add, update, and remove methods of its handler on a given `DiffResult`.
 */
export class DiffProcessor {
  handler: DiffHandling

  constructor (handler: DiffHandling) {
    this.handler = handler
  }

  handleDifferences (differences: DiffResult): void {
    for (let entity of differences.deleteList) {
      this.handler.remove(entity)
    }
    for (let entity of differences.editList) {
      this.handler.edit(entity)
    }
    for (let entity of differences.addList) {
      this.handler.add(entity)
    }
  }
}
