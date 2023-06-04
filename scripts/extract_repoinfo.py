import pandas as pd
import re

csv_data = pd.read_csv('./Csvs/40040-valid-giturl-bq-results-20230529.csv')

data_partial = pd.DataFrame(csv_data, columns = ['Name', 'Version', 'URL', 'NDependencies'])

# Here we drop off the duplicated URLs
data_deduplicated_url = data_partial.drop_duplicates(subset=['URL'])

pattern1 = r"github\.com/(.*?)\."
pattern2 = r"github\.com:(.*?)\."

def extract(text):
    match1 = re.search(pattern1, text)
    match2 = re.search(pattern2, text)

    if text == "https://github.com":
        return

    if match1:
        substring = match1.group(1)
        print(substring)
    elif match2:
        substring = match2.group(1)
        print(substring)
    else:
        substring = text.split("github.com/")[1]
        print(substring)


    return substring

# And we extract the repoinfo
data_deduplicated_url['URL'] = data_deduplicated_url['URL'].apply(lambda x: extract(x))

data_deduplicated_url.to_csv('./Csvs/40040-deduplicated.csv', index=False)