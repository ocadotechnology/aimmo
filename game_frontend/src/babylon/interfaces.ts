import { Environment } from './environment/environment'
import { DiffResult, DiffItem } from './diff'

export interface GameNode {
    object: any;
    setup(environment: Environment): void;
}

export interface DiffHandling {
    add(item: DiffItem): void;
    update(item: DiffItem): void;
    delete(item: DiffItem): void;
}

export class DiffProcessor {
  handler: DiffHandling

  constructor (handler: DiffHandling) {
    this.handler = handler
  }

  handleDifferences (differences: DiffResult): void {
    for (let avatar of differences.deleteList) {
      this.handler.delete(avatar)
    }
    for (let avatar of differences.editList) {
      this.handler.update(avatar)
    }
    for (let avatar of differences.addList) {
      this.handler.add(avatar)
    }
  }
}
