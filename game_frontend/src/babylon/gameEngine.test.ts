/* eslint-env jest */
import { MockEnvironment } from '../testHelpers/mockEnvironment'
import GameEngine from './gameEngine'
import AvatarManager from './entities/avatarManager'
import dummyImportMeshAsync from '../testHelpers/dummyImportMeshAsync'
import { DiffItem } from './diff'

let gameEngine: GameEngine
let avatarToAdd: DiffItem
let examplePlayer1: any
let examplePlayer2: any

beforeEach(() => {
  gameEngine = new GameEngine(jest.fn(), new MockEnvironment(true, 'future'))
  gameEngine.populateMap()
  avatarToAdd = new DiffItem(1, {
    health: 5,
    location: {
      x: 0,
      y: 0,
    },
    score: 0,
    id: 1,
    orientation: 'east',
  })
  examplePlayer1 = {
    id: 1,
    location: {
      x: 1,
      y: 1,
    },
  }
  examplePlayer2 = {
    id: 2,
    location: {
      x: 2,
      y: 2,
    },
  }
})

function generateProps(
  cameraCenteredOnUserAvatar: Boolean,
  gameLoaded: Boolean,
  players: any,
  currentAvatarID: Number
) {
  return {
    cameraCenteredOnUserAvatar: cameraCenteredOnUserAvatar,
    gameLoaded: gameLoaded,
    gameState: {
      players: players,
    },
    currentAvatarID: currentAvatarID,
  }
}

describe('GameEngine', () => {
  it('centers the camera on avatar location', async () => {
    const props = generateProps(true, true, { 0: examplePlayer1 }, 1)

    gameEngine.entities.avatars = new AvatarManager(gameEngine.environment, dummyImportMeshAsync)
    gameEngine.entities.setCurrentAvatarID(1)

    await gameEngine.entities.avatars.add(avatarToAdd)

    gameEngine.environmentManager.camera.centerOn = jest.fn()
    gameEngine.centerOn(props)

    expect(gameEngine.environmentManager.camera.centerOn).toBeCalled()
  })

  it('uncenters the camera on avatar location', async () => {
    gameEngine.entities.avatars = new AvatarManager(gameEngine.environment, dummyImportMeshAsync)
    gameEngine.entities.setCurrentAvatarID(1)

    await gameEngine.entities.avatars.add(avatarToAdd)

    gameEngine.environmentManager.camera.unCenter = jest.fn()
    gameEngine.environmentManager.unCenter(gameEngine.entities.avatars.currentAvatarMesh)

    expect(gameEngine.environmentManager.camera.unCenter).toBeCalled()
  })

  it('handles game state updates', () => {
    const previousProps = generateProps(true, true, { 0: examplePlayer1 }, 1)
    const currentProps = generateProps(true, true, { 0: examplePlayer1, 1: examplePlayer2 }, 2)

    gameEngine.entities.onGameStateUpdate = jest.fn()
    gameEngine.entities.setCurrentAvatarID = jest.fn()

    gameEngine.onUpdate(previousProps, currentProps)

    expect(gameEngine.entities.onGameStateUpdate).toBeCalled()
    expect(gameEngine.entities.setCurrentAvatarID).toBeCalled()
  })
})
