import EnvironmentRenderer from './environment';

export interface GameNode {
    object: any
    setup(environmentRenderer: EnvironmentRenderer): void
    onGameStateUpdate(gameState: any): void
}
