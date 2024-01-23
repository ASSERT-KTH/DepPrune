### Node version in environment: v16.17.0

### npm version in environment: v9.3.1

### Start up

```
git clone
```

### Metadata about each package

`repo.json` is a file with all necessary meta information for one or multiple repos.

```
{
  "projects": [
    {
      "folder": "airtap",
      "repo": "airtap/airtap",
      "commit": "034a6cf5c0f0014c94ac7f83b19fee69eda218e4",
      "entryFile": "lib/airtap.js",
      "gitURL": "https://github.com/airtap/airtap.git",
      "testPassSignal": "pass  142",
      "coverage": "78.05 |    62.93 |      75 |   80.31"
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
sh debloat_individually_directly.sh
```

For removing direct dependencies, run the following:

```
sh debloat_individually_indirectly.sh
```

Debloating result will be recorded in log.
Modify the path of the log in `debloat_individually_directly.sh` or `debloat_individually_indirectly.sh` if necessary.

### Debloat entire dependencies

1. Create two files for each repo, in the foldler of `Playground/{repofolder}`:
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
