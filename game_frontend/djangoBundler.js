const Bundler = require('parcel-bundler')
const Path = require('path')
const shell = require('shelljs')
const fs = require('fs')

const file = Path.join(__dirname, './index.html')
const outDir = Path.join(__dirname, '../players/static/react')

const options = {
  outDir,
  outFile: 'index.html',
  publicUrl: './',
  watch: process.env.NODE_ENV !== 'production',
  minify: process.env.NODE_ENV === 'production',
  target: 'browser',
  cache: process.env.NODE_ENV === 'production'
}

const templateFolder = Path.resolve(Path.join(__dirname, '../players/templates/players'))

const bundler = new Bundler(file, options)

bundler.on('bundled', (bundle) => {
  let entryPointHTML = shell.cat(bundle.name).stdout
  entryPointHTML = '{% load static %}\n' + entryPointHTML
  entryPointHTML = entryPointHTML.replace(/(<script src=")(.*\.js)("><\/script>)/g, '$1{% static "react/$2" %}$3')
  entryPointHTML += '<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.7.4/socket.io.min.js"></script>'
  fs.writeFile(`${templateFolder}/game_ide.html`, entryPointHTML, (error) => {
    if (error) { return console.log(error) }
    console.log('game_ide.html django template generated sucessfully')
  })
})

bundler.bundle()
