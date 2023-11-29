/* eslint-env jest */
import { matchFromImports, matchImports } from './syntax';
jest.mock('threads/worker')


describe('validate imports', () => {
  it('match imports', () => {
    const imports = matchImports(`
import a
import b, c

def import_d():
    import d

def import_e(): import e

import f.f2
`);

    return expect(imports).toEqual(new Set([
      'a',
      'b',
      'c',
      'd',
      'e',
      'f.f2'
    ]));
  });

  it('match imports with comments', () => {
    const imports = matchImports(`
import a # some comment
import b #
import c#touching
import d # some # comment
import e, f #
`);

    return expect(imports).toEqual(new Set([
      'a',
      'b',
      'c',
      'd',
      'e',
      'f'
    ]));
  });

  it('match imports with irregular spacing', () => {
    const imports = matchImports(`
import     a     
import   b,    c    
import d , e
import f,g
`);

    return expect(imports).toEqual(new Set([
      'a',
      'b',
      'c',
      'd',
      'e',
      'f',
      'g'
    ]));
  });

  it('match imports with invalid syntax', () => {
    const imports = matchImports(`
import a,
import b,,c
import d.
`);

    return expect(imports).toEqual(new Set());
  });

  it('match from-imports', () => {
    const fromImports = matchFromImports(`
from a import ( # after import
    b, # after b
    c, # after b
) # after end

from d.d1 import (
    e,
    f
) 

from g import (
    h,,
    i
) 

def foo(): from j import (
    k,
    l
)

from m import (n, o)
from p import q, r # some comment
`);

    return expect(fromImports).toEqual({
      'a': new Set(['b', 'c']),
      'd.d1': new Set(['e', 'f']),
      'j': new Set(['k', 'l']),
      'm': new Set(['n', 'o']),
      'p': new Set(['q', 'r']),
    });
  });
});