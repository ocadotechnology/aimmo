/* eslint-env jest */
import { diff, DiffResult, DiffItem } from './diff'

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
    expect(difference).toEqual(new DiffResult([{ id: 2, value: { 3: 'c' } }], [], []))
  })

  it('returns add changes if initial array is empty', () => {
    var previous = []
    var current = [{ 1: 'a' }, { 2: 'b' }]

    var difference = diff(previous, current)

    expect(difference).toEqual(
      new DiffResult(
        [
          { id: 0, value: { 1: 'a' } },
          { id: 1, value: { 2: 'b' } },
        ],
        [],
        []
      )
    )
  })

  it('returns delete changes if elements have been removed', () => {
    var previous = [{ 1: 'a' }, { 2: 'b' }]
    var current = [{ 1: 'a' }]

    var difference = diff(previous, current)

    expect(difference).toEqual(new DiffResult([], [new DiffItem(1, { 2: 'b' })], []))
  })

  it('returns edit changes if elements have been changed', () => {
    var previous = [{ 1: 'a' }, { 2: 'b' }]
    var current = [{ 1: 'a' }, { 2: 'c' }]

    var difference = diff(previous, current)

    expect(difference).toEqual(new DiffResult([], [], [new DiffItem(1, { 2: 'c' })]))
  })
})
