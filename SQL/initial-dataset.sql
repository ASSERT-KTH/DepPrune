-- SQL: 10000->2707
-- The following SQL fetchs the top 10000 Npm packages, and excludes packages:
-- 1. with a name starts with @, since we run our experiment automatically and avoid packages with a same folder name after download from github.
-- 2. with a valid Repo link with a substring "github.com"

DECLARE
  Sys STRING DEFAULT 'NPM';

WITH
  HighestReleases AS (
    SELECT
      Name,
      Version,
    FROM (
      SELECT
        Name,
        Version,
        ROW_NUMBER()
          OVER (PARTITION BY
                  Name
                ORDER BY
                  VersionInfo.Ordinal DESC) AS RowNumber
        FROM
          `bigquery-public-data.deps_dev_v1.PackageVersionsLatest`
        WHERE
          System = Sys
          AND VersionInfo.IsRelease)
    WHERE RowNumber = 1),

    TopDependencies AS (
      SELECT
        D.Name,
        D.Version,
        COUNT(*) AS NDependencies
      FROM
        `bigquery-public-data.deps_dev_v1.DependenciesLatest` AS D
      JOIN
        HighestReleases AS H
      ON
        D.Name = H.Name AND D.Version = H.Version
      WHERE
        D.System = Sys
      GROUP BY
        Name,
        Version
      ORDER BY
        NDependencies DESC
      LIMIT
        10000)

  SELECT
    P.Name,
    P.Version,
    lnk.URL,
    T.NDependencies
  FROM 
    `bigquery-public-data.deps_dev_v1.PackageVersions` AS P, unnest(Links) as lnk
  JOIN 
    TopDependencies AS T
  ON 
    T.Name = P.Name AND T.Version = P.Version
  WHERE
    P.System = Sys
    AND P.Name NOT LIKE '%@%'
    AND lnk.Label = 'SOURCE_REPO'
    AND lower(lnk.URL) LIKE '%github.com%'
  GROUP BY
    P.Name,
    P.Version,
    lnk.URL,
    T.NDependencies
  ORDER BY
    T.NDependencies DESC
