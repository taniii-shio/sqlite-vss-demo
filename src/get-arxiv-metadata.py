import arxiv
import pprint

# Construct the default API client.
client = arxiv.Client()

# Search for the 10 most recent articles matching the keyword "quantum."
search = arxiv.Search(
  query = "data science",
  max_results = 5,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

results = client.results(search)
all_results = list(results)
# all_resultsを辞書型に変換して、キーを'title', 'summary', 'published'に絞る
all_results = [vars(s) for s in all_results]
all_results = [{k: v for k, v in d.items() if k in ('title', 'summary', 'published', 'entry_id')} for d in all_results]
# publishedをdatetime型に変換する
for d in all_results:
  d['published'] = d['published'].strftime('%Y-%m-%d')

# pprint.pprint(all_results)

# all_resultsをjson形式で保存する
import json
with open('data.json', 'w') as f:
  json.dump(all_results, f, indent=2)
