from __future__ import annotations
import os
import arcgis
import datetime as _dt
from arcgis.gis import GIS, Item
from arcgis.features import Table, FeatureSet, Feature
import pandas as pd
from typing import Any

print(arcgis.__file__)
print(arcgis.__version__)

import urllib.request


def handle_fiddler():
    proxies = urllib.request.getproxies()
    if proxies == {}:
        proxies = None
    else:
        proxies['https'] = proxies['https'].replace("https", "http")
    return proxies


proxies = handle_fiddler()

if __name__ == "__main__":
    username: str = os.environ['AGOL_ACCOUNT']
    password: str = os.environ['AGOL_CREDS']
    ITEM_ID: str = os.environ['ITEM_ID']
    gis: GIS = GIS(
        username=username,
        password=password,
        verify_cert=False,
        proxy=proxies,
    )
    item: Item = gis.content.get(ITEM_ID)
    lyr: Table = item.tables[0]
    credits = gis.admin.credits
    now = _dt.datetime.now()  # tz=_dt.timezone.utc)

    data: dict[str, Any] = credits.credit_usage(
        start_time=now - _dt.timedelta(days=1), time_frame="today"
    )
    data['capture_start'] = now - _dt.timedelta(days=1)
    data['capture_stop'] = now
    df: pd.DataFrame = pd.DataFrame(data=[data])
    print(lyr.edit_features(adds=df))
    print('Credit table updated. See you next time, Space Cowboy!')
