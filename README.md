# Multee

Multee is under development.

### Start up

```
git clone

npm install

npm run build
```

### Enrich the json file

`repoSet.json` is a file with all necessary meta information for one or multiple repos.

```
{
  "projects": [
    {
      "gitURL": "https://github.com/isaacs/node-glob.git",
      "entryFile": "glob.js",
      "folder": "node-glob",
      "commit": "d844b2c1debfb7a408a8a219aea6cd5c66cfdea4"
    }
  ]
}
```

### Generate variants

```
sh readJson.sh
```

### Empty functions

There are two ways to generate variants by debloating.
The first way is to "empty" each function in each unused files.
When we say "empty" a function, it means to replace the whole function body with a short string 'lyx'.

```
sh removefunctions.sh node-glob_unused-files.txt node-glob_variants.json
```

### Empty files

The second way is to "empty" the whole unused file which still exites but with no content.

```
sh removefiles.sh node-glob_unused-files.txt
```

### Run test for each variant

```
sh runtest.sh node-glob
```
