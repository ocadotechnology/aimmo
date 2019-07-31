/* eslint-env jest */
import diff from './diff'

describe('diff', () => {
  it('returns nothing if arrays are equal', () => {
    var previous = [{ 1: 'a' }, { 2: 'b' }]
    var current = [{ 1: 'a' }, { 2: 'b' }]

    var difference = diff(previous, current)

    expect(difference).toEqual({ addList: [], deleteList: [], editList: [] })
  })

  it('returns add changes if elements have been added', () => {
    var previous = [{ 1: 'a' }, { 2: 'b' }]
    var current = [{ 1: 'a' }, { 2: 'b' }, { 3: 'c' }]

    var difference = diff(previous, current)

    expect(difference).toEqual({ addList: [{ 3: 'c', id: '2' }], deleteList: [], editList: [] })
  })

  it('returns add changes if initial array is empty', () => {
    var previous = []
    var current = [{ 1: 'a' }, { 2: 'b' }]

    var difference = diff(previous, current)

    expect(difference).toEqual({ addList: [{ 1: 'a', id: '0' }, { 2: 'b', id: '1' }], deleteList: [], editList: [] })
  })

  it('returns delete changes if elements have been removed', () => {
    var previous = [{ 1: 'a' }, { 2: 'b' }]
    var current = [{ 1: 'a' }]

    var difference = diff(previous, current)

    expect(difference).toEqual({ addList: [], deleteList: [{ 2: 'b', id: '1' }], editList: [] })
  })

  it('returns edit changes if elements have been changed', () => {
    var previous = [{ 1: 'a' }, { 2: 'b' }]
    var current = [{ 1: 'a' }, { 2: 'c' }]

    var difference = diff(previous, current)

    expect(difference).toEqual({ addList: [], deleteList: [], editList: [{ 2: 'c', id: '1' }] })
  })
})
