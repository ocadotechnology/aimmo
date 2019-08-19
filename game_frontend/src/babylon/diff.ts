import isEqual from 'lodash.isequal'
import { element } from 'prop-types'

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
    noPreviousStateGiven(diffResult, current)
    return diffResult
  }

  computeDiff(diffResult, previous, current)
  return processRemainingElements(diffResult, previous, current)
}

function noPreviousStateGiven (result: DiffResult, current: Array<any>): void {
  current.map((element, index) => {
    result.addList.push({
      id: +index,
      value: element
    })
  })
}

function computeDiff (result: DiffResult, previous: Array<any>, current: Array<any>): void {
  for (let [index, element] of Object.entries(previous)) {
    if (!isEqual(previous[index], current[index])) {
      if (isElementDefinedAndNotEqualToPreviousElement(previous[index], current[index])) {
        result.editList.push({
          id: index,
          value: current[index]
        })
      } else {
        result.deleteList.push({
          id: index,
          value: element
        })
      }
    }
  }
}

function isElementDefinedAndNotEqualToPreviousElement (first: DiffItem, second: DiffItem) {
  return first !== undefined && first !== second
}

function processRemainingElements (result: DiffResult, previous: Array<any>, current: Array<any>) {
  if (previous.length - current.length < 0) {
    for (let [index, element] of Object.entries(current)) {
      if (+index >= previous.length) {
        result.addList.push({
          id: index,
          value: element
        })
      }
    }
  }
  return result
}
