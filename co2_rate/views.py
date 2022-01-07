from datetime import datetime
from django.shortcuts import render
import requests

from co2_rate.models import RealData, InterpolateData
import pandas as pd


# Create your views here.
def get_data(request):
    if not RealData.objects.exists():
        response = requests.get("https://api-recrutement.ecoco2.com/v1/data/",
                                params={'start': datetime.strptime('2017-01-01T00:00:00',
                                                                   '%Y-%m-%dT%H:%M:%S').timestamp(),
                                        'end': datetime.strptime('2018-12-31T23:59:00',
                                                                 '%Y-%m-%dT%H:%M:%S').timestamp()})
        datas = pd.DataFrame(response.json())
        datas['datetime'] = pd.to_datetime(datas['datetime'], format='%Y-%m-%dT%H:%M:%S')
        RealData.objects.bulk_create([RealData(date_time=datas.loc[i, 'datetime'],
                                               rate=datas.loc[i, 'co2_rate'])
                                      for i in range(len(datas))])
    else:
        datas = pd.DataFrame([(data.date_time, data.rate) for data in RealData.objects.all()],
                             columns=['datetime', 'co2_rate'])
    datas = datas.set_index('datetime')

    if not InterpolateData.objects.exists():
        other_frequency = pd.date_range(start='2017-01-01T00:00:00',
                                        end='2018-12-31T23:59:00',
                                        freq='1H')
        new_dataframe = datas[datas.index.isin(other_frequency)].reset_index()
        InterpolateData.objects.bulk_create([InterpolateData(date_time=new_dataframe.loc[j, 'datetime'],
                                                             rate=new_dataframe.loc[j, 'co2_rate'])
                                             for j in range(len(new_dataframe))])
    else:
        new_dataframe = pd.DataFrame([(data.date_time, data.rate) for data in InterpolateData.objects.all()],
                                     columns=['datetime', 'co2_rate'])
    new_dataframe = new_dataframe.set_index('datetime')
    new_dataframe = new_dataframe.reindex(
        pd.date_range(start='2017-01-01T00:00:00',
                      end='2018-12-31T23:59:00',
                      freq='30min')
    )
    new_dataframe['real_data'] = datas['co2_rate']
    new_dataframe = new_dataframe.interpolate(method='linear')
    week = new_dataframe[new_dataframe.index.dayofweek < 5]  # filter DataFrame into working days
    weekends = new_dataframe[new_dataframe.index.dayofweek > 4]  # filter DataFrame into weekends
    df = new_dataframe[-20:]
    plot = df.plot(figsize=(10, 10))
    fig = plot.get_figure()
    fig.savefig("media/plot.png")

    new_dataframe.loc['mean working day'] = week.mean()
    new_dataframe.loc['mean weekends'] = weekends.mean()

    return render(request, 'index.html', context={'dataframe': new_dataframe[-22:].to_html()})
