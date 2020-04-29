from ..fabric import Fabric
from ..parameters import URL_TFDOC, TEMP_DIR
from ..lib import readSets
from ..core.helpers import console, setDir
from .find import findAppConfig
from .helpers import dh
from .settings import setAppSpecs, setAppSpecsApi
from .links import linksApi, outLink
from .text import textApi
from .sections import sectionsApi
from .display import displayApi
from .search import searchApi
from .data import getModulesData


# SET UP A TF API FOR AN APP


class App:
    def __init__(
        self,
        appName,
        appPath,
        commit,
        release,
        local,
        hoist=False,
        version=None,
        checkout="",
        mod=None,
        locations=None,
        modules=None,
        api=None,
        setFile="",
        silent=False,
        _browse=False,
    ):
        for (key, value) in dict(
            appName=appName, api=api, version=version, silent=silent, _browse=_browse
        ).items():
            setattr(self, key, value)

        cfg = findAppConfig(appName, appPath, commit, release, local, version=version)
        setAppSpecs(self, cfg)
        aContext = self.context
        version = aContext.version

        self.isCompatible = cfg["isCompatible"]

        setDir(self)

        if not self.api:
            self.sets = None
            if setFile:
                sets = readSets(setFile)
                if sets:
                    self.sets = sets
                    console(f'Sets from {setFile}: {", ".join(sets)}')
            specs = getModulesData(
                self, mod, locations, modules, version, checkout, silent
            )
            if specs:
                (locations, modules) = specs
                self.tempDir = f"{self.repoLocation}/{TEMP_DIR}"
                TF = Fabric(locations=locations, modules=modules, silent=silent or True)
                api = TF.load("", silent=silent or True)
                if api:
                    self.api = api
                    excludedFeatures = aContext.excludedFeatures
                    allFeatures = TF.explore(silent=silent or True, show=True)
                    loadableFeatures = allFeatures["nodes"] + allFeatures["edges"]
                    useFeatures = [
                        f for f in loadableFeatures if f not in excludedFeatures
                    ]
                    result = TF.load(useFeatures, add=True, silent=silent or True)
                    if result is False:
                        self.api = None
            else:
                self.api = None

        if self.api:
            linksApi(self, appName, silent)
            searchApi(self)
            sectionsApi(self)
            setAppSpecsApi(self, cfg)
            displayApi(self, silent)
            textApi(self)
            if hoist:
                docs = self.api.makeAvailableIn(hoist)
                if not silent:
                    dh(
                        "<details open><summary><b>API members</b>:</summary>\n"
                        + "<br/>\n".join(
                            ", ".join(
                                outLink(
                                    entry,
                                    f"{URL_TFDOC}/Api/{head}/#{ref}",
                                    title="doc",
                                )
                                for entry in entries
                            )
                            for (head, ref, entries) in docs
                        )
                        + "</details>"
                    )
        else:
            if not _browse:
                console(
                    f"""
There were problems with loading data.
The Text-Fabric API has not been loaded!
The app "{appName}" will not work!
""",
                    error=True,
                )

    def reuse(self, hoist=False):
        aContext = self.context
        appPath = aContext.appPath
        appName = aContext.appName
        local = aContext.local
        commit = aContext.commit
        release = aContext.release
        version = aContext.version
        api = self.api

        cfg = findAppConfig(appName, appPath, commit, release, local, version=version)
        setAppSpecs(self, cfg)

        if api:
            linksApi(self, appName, True)
            searchApi(self)
            sectionsApi(self)
            setAppSpecsApi(self, cfg)
            displayApi(self, True)
            textApi(self)
            if hoist:
                api.makeAvailableIn(hoist)
