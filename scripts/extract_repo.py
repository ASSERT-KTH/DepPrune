import pandas as pd
import re

csv_data = pd.read_csv('./Csvs/2707-valid-giturl-bq-results-20230522.csv')

data_partial = pd.DataFrame(csv_data, columns = ['Name', 'Version', 'URL', 'NDependencies'])

data_deduplicated_url = data_partial.drop_duplicates(subset=['URL'])

pattern1 = r"github\.com/(.*?)\."
pattern2 = r"github\.com:(.*?)\."
# print(re.search(pattern, text).group(1))
# data_deduplicated_url['URL'] = re.search(pattern, data_deduplicated_url['URL']).group(1)
def extract(text):
    match1 = re.search(pattern1, text)
    match2 = re.search(pattern2, text)

    if match1:
        substring = match1.group(1)
    elif match2:
        substring = match2.group(1)
    else:
        substring = text.split("github.com/")[1]

    return substring

data_deduplicated_url['URL'] = data_deduplicated_url['URL'].apply(lambda x: extract(x))
data_deduplicated_url.to_csv('./Csvs/2707-deduplicated.csv', index=False)