### Start up

```
git clone
```

### Configurations about each package

`repo.json` is a file with all necessary meta information for one or multiple repos.

```
{
  "projects": [
    {
      "folder": "airtap",
      "repo": "airtap/airtap",
      "commit": "034a6cf5c0f0014c94ac7f83b19fee69eda218e4",
      "gitURL": "https://github.com/airtap/airtap.git",
      "unitTest": "test"
    }
  ]
}
```

### Detect Unused dependencies for the repo

```
sh detect_bloated_strace.sh
```

### Automatically remove dependencies.

```
sh remove_bloated_dependencies.sh
```
### Generate debloated metadata files.

```
python debloat_pck_json.py package_name
python debloat_lock_file.py package_name
```

We can observe that new versions of `package.json` and `package-lock.json` is generated, without the bloated dependencies.

##### Node version in environment: v16.17.0

##### npm version in environment: v9.3.1
