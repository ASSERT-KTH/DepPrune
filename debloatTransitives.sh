path='transitive_debloating.txt'
cat $path | while read rows
do

    python3 excludeTransitives.py $rows
    echo "I am package "$rows" ......."
    echo "I am package "$rows" ......." >> /dev/stderr
    # List dep-tree before excluding
    cd "VariantsPureDep/"$rows"/variant_deps/"$rows
    echo "dependency tree before excluding transitives"
    echo "dependency tree before excluding transitives" >> /dev/stderr
    npm list --all --omit=dev
    
    # Exclude transitive bloated dependencies
    npm i npm-dependency-exclusion
    npx npm-dependency-exclusion

    npm i npm-dependency-exclusion
    npx npm-dependency-exclusion

    npm i npm-dependency-exclusion
    npx npm-dependency-exclusion

    # List dep-tree after excluding
    echo "dependency tree after excluding transitives"
    echo "dependency tree after excluding transitives" >> /dev/stderr
    npm list --all --omit=dev

    npm run test

    cd ../../../../
done