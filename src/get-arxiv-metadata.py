import arxiv
import pprint

client = arxiv.Client()

# 昨日に投稿された論文を取得
search = arxiv.Search(
  query = 'cat:cs.* AND submittedDate:[20231026000000 TO 20231026235959]',
  max_results = 10,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

results = client.results(search)
all_results = list(results)

pprint.pprint(all_results)
# all_resultsを辞書型に変換して、キーを'title', 'summary', 'published'に絞る
all_results = [vars(s) for s in all_results]
all_results = [{k: v for k, v in d.items() if k in ('title', 'summary', 'published', 'entry_id', 'primary_category')} for d in all_results]
# publishedをdatetime型に変換する
for d in all_results:
  d['published'] = d['published'].strftime('%Y-%m-%d')

pprint.pprint(all_results)

# all_resultsをjson形式で保存する
import json
with open('data.json', 'w') as f:
  json.dump(all_results, f, indent=2)
