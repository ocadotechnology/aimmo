import isEqual from 'lodash.isequal'


export const ADD = "A"
export const DELETE = "D"
export const EDIT = "E"

export default function diff(previous: Array<any>, current: Array<any>): Array<any> {
    let createDiffObject = function (element: any, type: string) {
        return { object: element, updateType: type }
    }

    var finalDiff = []

    // If there is no previous array, simply tell them to add everything in the new one.
    if (!previous.length) {
        for (let element of current)
            finalDiff.push(createDiffObject(element, ADD))
        return finalDiff
    }

    // Goes through every differing element, if the index exists in both lists, mark as Edit.
    // If the element only exists in the previous list, mark as a delete.
    for (let index in previous) {
        if (!isEqual(previous[index], current[index])) {
            if (previous[index] != current[index] && current[index] !== undefined) {
                finalDiff.push(createDiffObject(current[index], EDIT))
            }
            else {
                finalDiff.push(createDiffObject(previous[index], DELETE))
            }
        }
    }

    // If our current is longer than our previous, mark everything in current that's not in
    // previous as an add.
    if (previous.length - current.length < 0) {
        for (let leftovers = previous.length; leftovers < current.length; leftovers++) {
            finalDiff.push(createDiffObject(current[leftovers], ADD))
        }
    }

    return orderDiff(finalDiff)
}

function orderDiff(diff: Array<any>): Array<any> {
    const toAdd = diff.filter(function (item: any): boolean {
        return (item.updateType === ADD)
    })
    const toDelete = diff.filter(function (item: any): boolean {
        return (item.updateType === DELETE)
    })
    const toEdit = diff.filter(function (item: any): boolean {
        return (item.updateType === EDIT)
    })

    return toDelete.concat(toEdit.concat(toAdd))
}