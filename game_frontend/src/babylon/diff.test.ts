/* eslint-env jest */
import diff from './diff'

describe('diff', () => {
    it('returns nothing if arrays are equal', () => {
        var previous = [1, 2, 3, 4, 5]
        var current = [1, 2, 3, 4, 5]

        var difference = diff(previous, current)

        expect(difference).toEqual([])
    })

    it('returns A type changes if elements have been added', () => {
        var previous = [1, 2, 3]
        var current = [1, 2, 3, 4]

        var difference = diff(previous, current)

        expect(difference).toEqual([{ object: 4, updateType: "A" }])
    })

    it('returns A type changes if initial array is empty', () => {
        var previous = []
        var current = [1, 2]

        var difference = diff(previous, current)

        expect(difference).toEqual([{ object: 1, updateType: "A" }, { object: 2, updateType: "A" }])
    })

    it('returns D type changes if elements have been removed', () => {
        var previous = [1, 2]
        var current = [1]

        var difference = diff(previous, current)

        expect(difference).toEqual([{ object: 2, updateType: "D" }])
    })

    it('returns E type changes if elements have been changed', () => {
        var previous = [{ 1: "a" }, { 2: "b" }]
        var current = [{ 1: "a" }, { 2: "c" }]

        var difference = diff(previous, current)

        expect(difference).toEqual([{ object: { 2: "c" }, updateType: "E" }])
    })
})
