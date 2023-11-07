import arxiv, datetime
from db.db import insert_paper

client = arxiv.Client()

dt_now_jst_aware = datetime.datetime.now(
    datetime.timezone(datetime.timedelta(hours=9))
)
dt_yesterday = dt_now_jst_aware - datetime.timedelta(days=1)
dt_yesterday = dt_yesterday.strftime('%Y%m%d')

search = arxiv.Search(
  query = f'cat:cs.* AND submittedDate:[{dt_yesterday}000000 TO {dt_yesterday}235959]',
  max_results = 1000,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

results = client.results(search)
all_results = list(results)

all_results = [vars(s) for s in all_results]
all_results = [{k: v for k, v in d.items() if k in ('title', 'summary', 'published', 'entry_id', 'primary_category')} for d in all_results]

for d in all_results:
  d['published'] = d['published'].strftime('%Y-%m-%d')
  d['url'] = d.pop('entry_id')
  d['abstract'] = d.pop('summary')

for data in all_results:
  insert_paper(data['published'], data['title'], data['primary_category'], data['url'], data['abstract'])
