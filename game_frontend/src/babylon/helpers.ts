export default function arrayDiff(previous: Array<any>, current: Array<any>): Array<any> {
    let createDiffObject = function (element: any, type: string) {
        return { object: element, updateType: type }
    }

    var finalDiff = []

    // If there is no previous array, simply tell them to add everything in the new one.
    if (!previous.length) {
        for (let element of current)
            finalDiff.push(createDiffObject(element, "A"))
        return finalDiff
    }

    // Goes through every differing element, if the index exists in both lists, mark as Edit.
    // If the element only exists in the previous list, mark as a delete.
    for (let index in previous) {
        if (!isEquivalent(previous[index], current[index])) {
            if (previous[index] != current[index] && current[index] !== undefined) {
                finalDiff.push(createDiffObject(current[index], "E"))
            }
            else {
                finalDiff.push(createDiffObject(previous[index], "D"))
            }
        }
    }

    // If our current is longer than our previous, mark everything in current that's not in
    // previous as an add.
    if (previous.length - current.length < 0) {
        for (let leftovers = previous.length; leftovers < current.length; leftovers++) {
            finalDiff.push(createDiffObject(current[leftovers], "A"))
        }
    }
    return finalDiff
}


function isEquivalent(a: any, b: any): boolean {
    if (a && b) {
        // Create arrays of property names
        var aProps = Object.getOwnPropertyNames(a);
        var bProps = Object.getOwnPropertyNames(b);

        // If number of properties is different,
        // objects are not equivalent
        if (aProps.length != bProps.length) {
            return false
        }

        for (var i = 0; i < aProps.length; i++) {
            var propName = aProps[i]

            // If values of same property are not equal,
            // objects are not equivalent
            if (a[propName] !== b[propName]) {
                return false
            }
        }

        // If we made it this far, objects
        // are considered equivalent
        return true
    } else
        return false
}
