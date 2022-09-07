import isEqual from 'lodash.isequal'

export const ADD = 'A'
export const DELETE = 'D'
export const EDIT = 'E'

export class DiffItem {
  id: number
  value: any

  constructor(id: number, value: any) {
    this.id = id
    this.value = value
  }
}
export class DiffResult {
  addList: Array<DiffItem>
  deleteList: Array<DiffItem>
  editList: Array<DiffItem>

  constructor(toAdd: Array<DiffItem>, toDelete: Array<DiffItem>, toEdit: Array<DiffItem>) {
    this.addList = toAdd
    this.deleteList = toDelete
    this.editList = toEdit
  }
}

/**
 * Calculates the difference between to arrays.
 * @param previous - Previous state of an array
 * @param current  - New/Current state of an array
 *
 * @returns an object containing 3 lists for adding, removing, and editing items
 */
export function diff(previous: Array<any>, current: Array<any>): DiffResult {
  if (!previous.length) {
    return new DiffResult(convertToDiffItemsArray(current), [], [])
  }

  const arrayOfDifferences = getDifferingElements(previous, current)
  const editList = getItemsToEdit(arrayOfDifferences, current)
  const deleteList = getItemsToDelete(arrayOfDifferences, current)
  const remainingElements = processRemainingElements(previous, current)

  return new DiffResult(remainingElements, deleteList, editList)
}

function convertToDiffItemsArray(current: Array<any>): DiffItem[] {
  return current.map((element, index) => ({
    id: index,
    value: element,
  }))
}

function getDifferingElements(previous: Array<any>, current: Array<any>): Array<Array<any>> {
  const differences = []
  for (const [index, element] of Object.entries(previous)) {
    if (!isEqual(element, current[index])) {
      differences.push([+index, element, current[index]])
    }
  }
  return differences
}

function getItemsToEdit(arrayOfDifferences: Array<Array<any>>, current: Array<any>): DiffItem[] {
  return arrayOfDifferences
    .filter(([id, previous, current]) => current !== undefined)
    .map(([id, previous, current]) => new DiffItem(id, current))
}

function getItemsToDelete(arrayOfDifferences: Array<Array<any>>, current: Array<any>): DiffItem[] {
  return arrayOfDifferences
    .filter(([id, previous, current]) => current === undefined)
    .map(([id, previous, current]) => new DiffItem(id, previous))
}

function processRemainingElements(previous: Array<any>, current: Array<any>): DiffItem[] {
  const remainingElements = []
  for (let index = previous.length; index < current.length; index++) {
    remainingElements.push(new DiffItem(index, current[index]))
  }
  return remainingElements
}
