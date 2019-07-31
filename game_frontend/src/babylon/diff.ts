import isEqual from 'lodash.isequal'

export const ADD = 'A'
export const DELETE = 'D'
export const EDIT = 'E'

export class DiffResult {
    addList: Array<any>
    deleteList: Array<any>
    editList: Array<any>

    constructor (toAdd: Array<any>, toDelete: Array<any>, toEdit: Array<any>) {
      this.addList = toAdd
      this.deleteList = toDelete
      this.editList = toEdit
    }
}

export default function diff (previous: Array<any>, current: Array<any>): any {
  var diffResult = new DiffResult([], [], [])

  // If there is no previous array, simply tell them to add everything in a new one.
  if (!previous.length) {
    for (let element of current) { diffResult.addList.push(element) }
    return diffResult
  }

  // Goes through every differing element, if the index exists in both lists, add to Edit.
  // If the element only exists in the previous list, add to Delete.
  for (let index in previous) {
    if (!isEqual(previous[index], current[index])) {
      if (previous[index] !== current[index] && current[index] !== undefined) {
        diffResult.editList.push(current[index])
      } else {
        diffResult.deleteList.push(previous[index])
      }
    }
  }

  // If our current is longer than our previous, add everything in current that's not in
  // previous to add.
  if (previous.length - current.length < 0) {
    for (let leftovers = previous.length; leftovers < current.length; leftovers++) {
      diffResult.addList.push(current[leftovers])
    }
  }

  return diffResult
}
