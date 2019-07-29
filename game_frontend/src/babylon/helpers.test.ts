/* eslint-env jest */
import React from 'react'
import * as BABYLON from 'babylonjs'
import arrayDiff from './helpers';

describe('arrayDiff', () => {
    it('returns nothing if arrays are equal', () => {
        var previous = [1, 2, 3, 4, 5]
        var current = [1, 2, 3, 4, 5]

        var diff = arrayDiff(previous, current)

        expect(diff).toEqual([])
    })

    it('returns A type changes if elements have been added', () => {
        var previous = [1, 2, 3]
        var current = [1, 2, 3, 4]

        var diff = arrayDiff(previous, current)

        expect(diff).toEqual([{ object: 4, updateType: "A" }])
    })

    it('returns A type changes if initial array is empty', () => {
        var previous = []
        var current = [1, 2]

        var diff = arrayDiff(previous, current)

        expect(diff).toEqual([{ object: 1, updateType: "A" }, { object: 2, updateType: "A" }])
    })

    it('returns D type changes if elements have been removed', () => {
        var previous = [1, 2]
        var current = [1]

        var diff = arrayDiff(previous, current)

        expect(diff).toEqual([{ object: 2, updateType: "D" }])
    })

    it('returns E type changes if elements have been changed', () => {
        var previous = [{ 1: "a" }, { 2: "b" }]
        var current = [{ 1: "a" }, { 2: "c" }]

        var diff = arrayDiff(previous, current)

        expect(diff).toEqual([{ object: { 2: "c" }, updateType: "E" }])
    })
})
