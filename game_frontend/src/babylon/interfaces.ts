import Environment from './environment';

export interface GameNode {
    object: any
    setup(environment: Environment): void
    onGameStateUpdate(gameState: any): void
}
