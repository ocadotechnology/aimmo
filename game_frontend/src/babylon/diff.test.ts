/* eslint-env jest */
import diff from './diff'

describe('diff', () => {
  it('returns nothing if arrays are equal', () => {
    var previous = [1, 2, 3, 4, 5]
    var current = [1, 2, 3, 4, 5]

    var difference = diff(previous, current)

    expect(difference).toEqual({ addList: [], deleteList: [], editList: [] })
  })

  it('returns add changes if elements have been added', () => {
    var previous = [1, 2, 3]
    var current = [1, 2, 3, 4]

    var difference = diff(previous, current)

    expect(difference).toEqual({ addList: [4], deleteList: [], editList: [] })
  })

  it('returns add changes if initial array is empty', () => {
    var previous = []
    var current = [1, 2]

    var difference = diff(previous, current)

    expect(difference).toEqual({ addList: [1, 2], deleteList: [], editList: [] })
  })

  it('returns delete changes if elements have been removed', () => {
    var previous = [1, 2]
    var current = [1]

    var difference = diff(previous, current)

    expect(difference).toEqual({ addList: [], deleteList: [2], editList: [] })
  })

  it('returns edit changes if elements have been changed', () => {
    var previous = [{ 1: 'a' }, { 2: 'b' }]
    var current = [{ 1: 'a' }, { 2: 'c' }]

    var difference = diff(previous, current)

    expect(difference).toEqual({ addList: [], deleteList: [], editList: [{ 2: 'c' }] })
  })
})
