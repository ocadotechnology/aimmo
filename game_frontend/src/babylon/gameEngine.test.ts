/* eslint-env jest */
import { MockEnvironment } from '../testHelpers/mockEnvironment'
import GameEngine from './gameEngine'
import AvatarManager from './entities/avatarManager'
import dummyImportMesh from '../testHelpers/dummyImportMesh'
import { DiffItem } from './diff'

let gameEngine: GameEngine

beforeEach(() => {
  gameEngine = new GameEngine(jest.fn(), new MockEnvironment(true))
})

function avatarDiffItem (index: string, orientation: string, location: {x: number, y: number}) {
  return new DiffItem(index, {
    health: 5,
    location: {
      x: location.x,
      y: location.y
    },
    score: 0,
    id: parseInt(index),
    orientation: orientation
  })
}

describe('GameEngine', () => {
  it('centers the camera on avatar location', () => {
    const props = {
      cameraCenteredOnUserAvatar: true,
      gameLoaded: true,
      gameState: {
        players: {
          0: {
            id: 1,
            location: {
              x: 1,
              y: 1
            }
          }
        }
      },
      currentAvatarID: 1
    }

    gameEngine.entities.avatars = new AvatarManager(gameEngine.environment, dummyImportMesh)
    gameEngine.updateCurrentAvatarID(0, 1)

    const avatar = avatarDiffItem('1', 'east', { x: 0, y: 0 })
    gameEngine.entities.avatars.add(avatar)

    console.log(gameEngine.entities.avatars.currentAvatarMesh)

    gameEngine.environmentManager.camera.centerOn = jest.fn()
    gameEngine.centerOn(props)

    expect(gameEngine.environmentManager.camera.centerOn).toBeCalled()
  })

  it('handles updates', () => {
    const previousProps = {
      cameraCenteredOnUserAvatar: true,
      gameLoaded: true,
      gameState: {
        players: {
          0: {
            id: 1,
            location: {
              x: 1,
              y: 1
            }
          }
        }
      },
      currentAvatarID: 1
    }
    const currentProps = {
      cameraCenteredOnUserAvatar: true,
      gameLoaded: true,
      gameState: {
        players: {
          0: {
            id: 1,
            location: {
              x: 1,
              y: 1
            }
          },
          1: {
            id: 2,
            location: {
              x: 2,
              y: 2
            }
          }
        }
      },
      currentAvatarID: 2
    }
    gameEngine.entities.onGameStateUpdate = jest.fn()
    gameEngine.entities.setCurrentAvatarID = jest.fn()

    gameEngine.onUpdate(previousProps, currentProps)

    expect(gameEngine.entities.onGameStateUpdate).toBeCalled()
    expect(gameEngine.entities.setCurrentAvatarID).toBeCalled()
  })
})
