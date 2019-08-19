import isEqual from 'lodash.isequal'

export const ADD = 'A'
export const DELETE = 'D'
export const EDIT = 'E'

export class DiffItem {
  id: string;
  value: any;

  constructor (id: string, value: any) {
    this.id = id
    this.value = value
  }
}
export class DiffResult {
    addList: Array<DiffItem>
    deleteList: Array<DiffItem>
    editList: Array<DiffItem>

    constructor (toAdd: Array<DiffItem>, toDelete: Array<DiffItem>, toEdit: Array<DiffItem>) {
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
export function diff (previous: Array<any>, current: Array<any>): DiffResult {
  var diffResult = new DiffResult([], [], [])

  if (!previous.length) {
    return noPreviousStateGiven(diffResult, current)
  }

  diffResult = doTheDiff(diffResult, previous, current)
  return processRemainingElements(diffResult, previous, current)
}

function noPreviousStateGiven (result: DiffResult, current: Array<any>): DiffResult {
  let list = JSON.parse(JSON.stringify(result))
  for (let [index, element] of Object.entries(current)) {
    list.addList.push({
      id: index,
      value: element
    })
  }
  return list
}

function doTheDiff (result: DiffResult, previous: Array<any>, current: Array<any>): DiffResult {
  let list = JSON.parse(JSON.stringify(result))
  for (let [index, element] of Object.entries(previous)) {
    if (!isEqual(previous[index], current[index])) {
      if (previous[index] !== current[index] && current[index] !== undefined) {
        list.editList.push({
          id: index,
          value: current[index]
        })
      } else {
        list.deleteList.push({
          id: index,
          value: element
        })
      }
    }
  }

  return list
}

function processRemainingElements (result: DiffResult, previous: Array<any>, current: Array<any>) {
  let list = JSON.parse(JSON.stringify(result))
  if (previous.length - current.length < 0) {
    for (let [index, element] of Object.entries(current)) {
      if (+index >= previous.length) {
        list.addList.push({
          id: index,
          value: element
        })
      }
    }
  }
  return list
}
