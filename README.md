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
sh removefunctions.sh node-glob
```

### Empty files

The second way is to "empty" the whole unused file which still exites but with no content.

```
sh removefiles.sh node-glob
```

### Run test for each variant

```
sh runtest.sh node-glob
```

### Run test and add logs for errors and commons
```
<!-- subtree-based mode -->

sh runtest.sh node-glob Variants 2>>Data/node-glob_errors_func.log  >> Data/node-glob_test_func.log
sh runtest.sh node-glob Variants 2>>Data/node-glob_errors_files.log  >> Data/node-glob_test_files.log

<!-- or dependency-based mode -->

sh runtest.sh node-glob VariantsDeps 2>>Data/node-glob_deps_errors_func.log  >> Data/node-glob_deps_test_func.log
sh runtest.sh node-glob VariantsDeps 2>>Data/node-glob_deps_errors_files.log  >> Data/node-glob_deps_test_files.log
```

### Watch limited logs
```
watch -n 5 cat errors.log
```
