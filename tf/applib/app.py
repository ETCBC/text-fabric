import sys

from importlib import util

from ..parameters import (
    ORG,
    APP_CODE
)
from ..core.helpers import console
from .repo import RepoData


def findApp(dataSource, checkoutApp, lgc, check, silent=False):
  rData = RepoData(
      ORG,
      f'app-{dataSource}',
      APP_CODE,
      checkoutApp,
      lgc,
      check,
      False,
      True,
      silent,
      isApp=True,
  )
  rData.makeSureLocal()
  base = rData.base
  return (rData.commitOff, rData.releaseOff, base) if base else (None, None, False)


def findAppConfig(dataSource, appDir):
  config = None
  appPath = f'{appDir}/config.py'

  try:
    spec = util.spec_from_file_location(f'tf.apps.{dataSource}.config', appPath)
    config = util.module_from_spec(spec)
    spec.loader.exec_module(config)
  except Exception as e:
    console(f'findAppConfig: {str(e)}', error=True)
    console(f'findAppConfig: Configuration for "{dataSource}" not found', error=True)
  return config


def findAppClass(dataSource, appDir):
  appClass = None
  moduleName = f'tf.apps.{dataSource}.app'

  try:
    spec = util.spec_from_file_location(
        moduleName,
        f'{appDir}/app.py',
    )
    code = util.module_from_spec(spec)
    sys.path.insert(0, appDir)
    spec.loader.exec_module(code)
    sys.path.pop(0)
    appClass = code.TfApp
  except Exception as e:
    console(f'findAppClass: {str(e)}', error=True)
    console(f'findAppClass: Api for "{dataSource}" not found')
  return appClass
