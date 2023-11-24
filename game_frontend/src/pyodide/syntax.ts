const namePattern = '[{base}][{base}0-9]*'.replace(/{base}/g, '_a-zA-Z');
const modulePattern = '{name}(?:\\.{name})*'.replace(/{name}/g, namePattern);

export function funcPattern({
  lineStart,
  captureName,
  captureArgs
}: {
  lineStart: boolean
  captureName: boolean
  captureArgs: boolean
}) {
  let pattern = ' *def +{name} *\\({args}\\) *:';

  if (lineStart) pattern = '^' + pattern;

  // TODO: refine
  const argsPattern = '.*';

  pattern = pattern.replace(
    /{name}/g,
    captureName ? `(${namePattern})` : namePattern
  );
  pattern = pattern.replace(
    /{args}/g,
    captureArgs ? `(${argsPattern})` : argsPattern
  );

  return pattern;
}

function splitImports(imports: string) {
  return new Set(imports.split(',').map((_import) => _import.trim()));
}

export function matchImports(code: string) {
  const pattern = new RegExp(
    [
      '^',
      '(?:{func})?'.replace(
        /{func}/g,
        funcPattern({
          lineStart: false,
          captureName: false,
          captureArgs: false
        })
      ),
      ' *import +({module}(?: *, *{module})*)'.replace(
        /{module}/g,
        modulePattern
      ),
      ' *(?:#.*)?',
      '$'
    ].join(''),
    'gm'
  );

  const imports: Set<string> = new Set();
  for (const match of code.matchAll(pattern)) {
    splitImports(match[1]).forEach((_import) => { imports.add(_import); });
  }

  return imports;
}

export function matchFromImports(code: string) {
  const pattern = new RegExp(
    [
      '^',
      '(?:{func})?'.replace(
        /{func}/g,
        funcPattern({
          lineStart: false,
          captureName: false,
          captureArgs: false
        })
      ),
      ' *from +({module}) +import'.replace(
        /{module}/g,
        modulePattern
      ),
      '(?: *\\(([^)]+)\\)| +({name}(?: *, *{name})*))'.replace(
        /{name}/g,
        namePattern
      ),
      ' *(?:#.*)?',
      '$'
    ].join(''),
    'gm'
  );

  const fromImports: Record<string, Set<string>> = {};
  for (const match of code.matchAll(pattern)) {
    let imports: Set<string>;
    if (match[3] === undefined) {
      // Get imports as string and remove comments.
      let importsString = match[2].replace(
        /#.*(\r|\n|\r\n|$)/g,
        ''
      );

      // If imports have a trailing comma, remove it.
      importsString = importsString.trim();
      if (importsString.endsWith(',')) {
        importsString = importsString.slice(0, -1);
      }

      // Split imports by comma.
      imports = splitImports(importsString);

      // If any imports are invalid, don't save them.
      const importPattern = new RegExp(`^${namePattern}$`, 'gm')
      if (imports.has('') ||
        [...imports].every((_import) => importPattern.test(_import))
      ) {
        continue;
      }
    } else {
      imports = splitImports(match[3]);
    }

    fromImports[match[1]] = imports;
  }

  return fromImports;
}
