const Bundler = require("parcel-bundler");
const Path = require("path");
const fs = require("fs");
const Handlebars = require("handlebars");

const file = Path.join(__dirname, "./public/index.html");
const outDir = Path.join(__dirname, "../aimmo/static/react");

const cloudEnvironments = new Set(["production", "staging"]);

const options = {
  outDir,
  outFile: "index.html",
  publicUrl: "./",
  watch: !cloudEnvironments.has(process.env.NODE_ENV),
  minify: cloudEnvironments.has(process.env.NODE_ENV),
  target: "browser",
  cache: cloudEnvironments.has(process.env.NODE_ENV)
};

const templateFolder = Path.resolve(
  Path.join(__dirname, "../aimmo/templates/players")
);
const handlebarsTemplatePath = Path.resolve(
  Path.join(__dirname, "./public/handlebars_template.html")
);

const bundler = new Bundler(file, options);

function getReactURL(entryPointHTML) {
  const regex = /(<script src=")(.*\.js)("><\/script>)/g;
  return regex.exec(entryPointHTML)[2];
}

Handlebars.registerHelper("if_eq", function(a, b, opts) {
  if (a === b) {
    return opts.fn(this);
  } else {
    return opts.inverse(this);
  }
});

function generateGameIDEHTML(reactFileName) {
  const templateString = fs.readFileSync(handlebarsTemplatePath, "utf-8");
  const template = Handlebars.compile(templateString);
  return template({
    reactUrl: `react/${reactFileName}`,
    environment: process.env.NODE_ENV
  });
}

bundler.on("bundled", bundle => {
  const entryPointHTML = fs.readFileSync(bundle.name, "utf-8");
  const reactUrl = getReactURL(entryPointHTML);
  const gameIDEHTML = generateGameIDEHTML(reactUrl);

  fs.writeFile(`${templateFolder}/game_ide.html`, gameIDEHTML, error => {
    if (error) {
      return console.log(error);
    }
    console.log("game_ide.html django template generated sucessfully");
  });
});

bundler.bundle();
