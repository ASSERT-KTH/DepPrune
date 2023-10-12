# Multee

Multee is under development.

### Node version: v16.17.0

### Start up

```
git clone

```

### Enrich the json file

`repo.json` is a file with all necessary meta information for one or multiple repos.

```
{
  "projects": [
    {
        "folder": "roe-scripts",
        "repo": "kaelzhang/roe-scripts",
        "commit": "f9ee9d3af61f6a3c5c779da176e4d0fff1b8a866",
        "entryFile": "src/index.js",
        "gitURL": "https://github.com/kaelzhang/roe-scripts.git",
        "testPassSignal": "50 tests passed",
        "coverage": "99.53 |    93.84 |   99.23 |   99.51"
    }
  ]
}
```

### Detect Unreachalbe dependencies for the repo

```
sh detect_bloated.sh
```

### Automatically, individually debloat direct dependencies and indirect dependencies.

For removing direct dependencies, run the following:
```
sh debloat_directly.sh
```

For removing direct dependencies, run the following:
```
sh debloat_indirectly.sh
```

Debloating result will be recorded in log. 
Modify the path of the log in `debloat_directly.sh` or `debloat_indirectly.sh` if necessary.

### Debloat entire dependencies

1. Create two files for each repo, in the foldler of `Playground/repofolder`:
direct_confirmed_deps.txt, which is used for remove direct dependencies.
individual_confirmed_deps.txt, which is used for remove indirect dependencies.
Respectively copy the result of the previous logs with only bloated dependencies that passed the tests.

2. Debloat entirely
Run the following:

```
sh debloat_entirely.sh
```
The debloated version of the package will be resolve in the root /DebloatedPackages folder.
We can observe that new versions of `package.json` and `package-lock.json` is generated, without the info of the bloated dependencies.