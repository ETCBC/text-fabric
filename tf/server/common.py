import sys
import os
import re
from glob import glob
from importlib import import_module

appPat = '^(.*)-app$'
appRe = re.compile(appPat)

msgLinePat = '^( *[0-9]+) (.*)$'
msgLineRe = re.compile(msgLinePat)


def getAppDir(myDir, dataSource):
  parentDir = os.path.dirname(myDir)
  tail = '' if dataSource == '' else f'{dataSource}-app'
  return f'{parentDir}/extra/{tail}'


def getConfig(dataSource):
  try:
    config = import_module('.config', package=f'tf.extra.{dataSource}-app')
  except Exception as e:
    print('getConfig:', e)
    print(f'getConfig: Data source "{dataSource}" not found')
    return None
  return config


def getDebug():
  for arg in sys.argv[1:]:
    if arg == '-d':
      return True
  return False


def getParam():
  myDir = os.path.dirname(os.path.abspath(__file__))
  dataSourcesParent = getAppDir(myDir, '')
  dataSourcesPre = glob(f'{dataSourcesParent}/*/config.py')
  dataSources = set()
  for p in dataSourcesPre:
    parent = os.path.dirname(p)
    d = os.path.split(parent)[1]
    match = appRe.match(d)
    if match:
      app = match.group(1)
      dataSources.add(app)
  dPrompt = '/'.join(dataSources)

  dataSource = None
  for arg in sys.argv[1:]:
    if arg.startswith('-'):
      continue
    dataSource = arg
    break

  if dataSource is None:
    dataSource = input(f'specify data source [{dPrompt}] > ')
  if dataSource not in dataSources:
    dataSource = None
  if dataSource is None:
    print(f'Pass a data source [{dPrompt}] as first argument')
  return dataSource


def _coarsify(n, spread):
  nAbs = int(round(abs(n) / spread)) * spread
  return nAbs if n >= 0 else -nAbs


def pageLinks(nResults, position, spread=10):
  if spread <= 1:
    spread = 1
  elif nResults == 0:
    lines = []
  elif nResults == 1:
    lines = [(1,)]
  elif nResults == 2:
    lines = [(1, 2)]
  else:
    if position == 1 or position == nResults:
      commonLine = (1, nResults)
    else:
      commonLine = (1, position, nResults)
    lines = []

    factor = 1
    while factor <= nResults:
      curSpread = factor * spread
      first = _coarsify(position - curSpread, curSpread)
      last = _coarsify(position + curSpread, curSpread)

      left = tuple(n for n in range(first, last, factor) if n > 0 and n < position)
      right = tuple(n for n in range(first, last, factor) if n > position and n <= nResults)

      both = tuple(n for n in left + (position,) + right if n > 0 and n <= nResults)

      if len(both) > 1:
        lines.append(both)

      factor *= spread

    lines.append(commonLine)

  html = '\n'.join(
      '<div class="pline">' +
      ' '.join(
          f'<a href="#" class="pnav {" focus" if position == p else ""}">{p}</a>'
          for p in line
      )
      +
      '</div>'
      for line in reversed(lines)
  )
  return html


def runSearch(search, query, cache):
  cacheKey = (query, False)
  if cacheKey in cache:
    return cache[cacheKey]
  (queryResults, messages) = search(query, msgCache=True)
  queryResults = sorted(queryResults)
  cache[cacheKey] = (queryResults, messages)
  return (queryResults, messages)


def runSearchCondensed(search, query, cache, condenseFunc):
  cacheKey = (query, True)
  if cacheKey in cache:
    return cache[cacheKey]
  (queryResults, messages) = runSearch(search, query, cache)
  queryResults = condenseFunc(queryResults)
  cache[cacheKey] = (queryResults, messages)
  return (queryResults, messages)


def compose(
    extraApi, results, start, position, opened,
    withNodes=False,
    linked=1,
    **options,
):
  if len(results) == 0:
    return 'no results'

  api = extraApi.api
  F = api.F

  firstResult = results[0][1]
  html = (
      f'''
<div class="dtheadrow">
  <div>n</div><div>{"</div><div>".join(F.otype.v(n) for n in firstResult)}</div>
</div>
'''
      +
      '\n'.join(
          extraApi.plainTuple(
              ns,
              i,
              position=position,
              opened=i in opened,
              withNodes=withNodes,
              linked=linked,
              **options,
          )
          for (i, ns) in results
      )
  )
  return html


def shapeMessages(messages):
  messages = messages.split('\n')
  html = []
  for msg in messages:
    match = msgLineRe.match(msg)
    if match:
      continue
    html.append(f'''
      <div class="eline">
        {msg}
      </div>
    ''')
  return ''.join(html)


def getValues(options, form):
  values = {}
  for (name, option, typ, acro, desc) in options:
    value = form.get(name, None)
    if typ == 'checkbox':
      value = True if value else False
    values[option] = value
  return values


def shapeOptions(options, values):
  html = []
  for (name, option, typ, acro, desc) in options:
    value = values[option]
    if typ == 'checkbox':
      value = 'checked' if value else ''
    else:
      value = f'value="{value}"'
    html.append(
        f'<div><input type="{typ}" id="{acro}" name="{name}" {value}/> {desc}</div>'
    )
  return '\n'.join(html)
