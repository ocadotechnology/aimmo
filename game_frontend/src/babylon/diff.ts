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

export default function diff (previous: Array<any>, current: Array<any>): DiffResult {
  var diffResult = new DiffResult([], [], [])

  // If there is no previous array, simply tell them to add everything in a new one.
  if (!previous.length) {
    for (let [index, element] of Object.entries(current)) {
      diffResult.addList.push({
        id: index,
        value: element
      })
    }
    return diffResult
  }

  // Goes through every differing element, if the index exists in both lists, add to Edit.
  // If the element only exists in the previous list, add to Delete.
  for (let [index, element] of Object.entries(previous)) {
    if (!isEqual(previous[index], current[index])) {
      if (previous[index] !== current[index] && current[index] !== undefined) {
        diffResult.editList.push({
          id: index,
          value: current[index]
        })
      } else {
        diffResult.deleteList.push({
          id: index,
          value: element
        })
      }
    }
  }

  // If our current is longer than our previous, add everything in current that's not in
  // previous to add.
  if (previous.length - current.length < 0) {
    for (let [index, element] of Object.entries(current)) {
      if (+index >= previous.length) {
        diffResult.addList.push({
          id: index,
          value: element
        })
      }
    }
  }
  return diffResult
}
