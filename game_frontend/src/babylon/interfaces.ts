import { Environment } from './environment/environment'
import { DiffResult, DiffItem } from './diff'

export interface GameNode {
    object: any;
    setup(environment: Environment): void;
}

export interface DiffHandling {
    add(item: DiffItem): void;
    edit(item: DiffItem): void;
    delete(item: DiffItem): void;
}

export class DiffProcessor {
  handler: DiffHandling

  constructor (handler: DiffHandling) {
    this.handler = handler
  }

  handleDifferences (differences: DiffResult): void {
    for (let entity of differences.deleteList) {
      this.handler.delete(entity)
    }
    for (let entity of differences.editList) {
      this.handler.edit(entity)
    }
    for (let entity of differences.addList) {
      this.handler.add(entity)
    }
  }
}
