/* eslint-env jest */
import { DiffProcessor, DiffHandling } from './interfaces'
import { DiffItem, diff } from './diff'
import isEqual from 'lodash.isequal'

class DummyHandler implements DiffHandling {
  items: Array<any>
  constructor(arr: Array<any>) {
    this.items = arr
  }

  add(item: DiffItem): void {
    this.items.push(item.value)
  }

  edit(item: DiffItem): void {
    this.items[item.id] = item.value
  }

  remove(item: DiffItem): void {
    this.items.splice(item.id)
  }
}

describe('Diff processor', () => {
  it('deletes elements marked for delete', () => {
    const startArray = [1, 2, 3, 4, 5]
    const newArray = [1, 2, 3, 4]
    const diffArray = diff(startArray, newArray)

    const handler = new DummyHandler(startArray)
    const diffProcessor = new DiffProcessor(handler)

    diffProcessor.handleDifferences(diffArray)
    expect(handler.items.length).toBe(4)
    expect(
      handler.items.find(function (element) {
        return isEqual(element, 5)
      })
    ).toBeUndefined()
  })

  it('changes an element marked for an update', () => {
    const startArray = [1, 2, 3, 4, 5]
    const newArray = [1, 2, 100, 4, 5]
    const diffArray = diff(startArray, newArray)

    const handler = new DummyHandler(startArray)
    const diffProcessor = new DiffProcessor(handler)
    diffProcessor.handleDifferences(diffArray)
    expect(handler.items.length).toBe(5)
    expect(handler.items[2]).toBe(100)
  })

  it('adds new elements', () => {
    const startArray = [1, 2, 3, 4, 5]
    const newArray = [1, 2, 3, 4, 5, 6]
    const diffArray = diff(startArray, newArray)

    const handler = new DummyHandler(startArray)
    const diffProcessor = new DiffProcessor(handler)

    diffProcessor.handleDifferences(diffArray)
    expect(handler.items.length).toBe(6)
    expect(handler.items[5]).toBe(6)
  })

  it('handles adding and updating in the same update', () => {
    const startArray = [1, 2, 3, 4, 5]
    const newArray = [1, 2, 100, 4, 5, 6]
    const diffArray = diff(startArray, newArray)

    const handler = new DummyHandler(startArray)
    const diffProcessor = new DiffProcessor(handler)
    diffProcessor.handleDifferences(diffArray)

    expect(handler.items.length).toBe(6)
    expect(handler.items[5]).toBe(6)
    expect(handler.items[2]).toBe(100)
  })

  it('handles deleting and updating in the same update', () => {
    const startArray = [1, 2, 3, 4, 5]
    const newArray = [1, 2, 100, 4]
    const diffArray = diff(startArray, newArray)

    const handler = new DummyHandler(startArray)
    const diffProcessor = new DiffProcessor(handler)
    diffProcessor.handleDifferences(diffArray)
    expect(handler.items.length).toBe(4)
    expect(handler.items[2]).toBe(100)
    expect(
      handler.items.find(function (element) {
        return isEqual(element, 5)
      })
    ).toBeUndefined()
  })
})
