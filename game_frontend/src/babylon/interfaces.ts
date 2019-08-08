import { Environment } from './environment/environment'
import { DiffResult } from './diff'

export interface GameNode {
    object: any;
    setup(environment: Environment): void;
}

export interface DiffHandling {
    handleDifferences(differences: DiffResult): void;
}
