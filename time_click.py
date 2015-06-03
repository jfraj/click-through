import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import sqrt
import itertools

import click_succ

colors = itertools.cycle(["r", "b", "g", "y", "m", "k", "c"])


def get_success_time_series(df, dt='D', **kwargs):
    """Return dict with time series."""
    clicked = df[df.click == 1].click.resample(dt, how='count')
    notclicked = df[df.click == 0].click.resample(dt, how='count')
    df_clicks = pd.concat([clicked, notclicked], axis=1,
                          keys=['clicked', 'notclicked'])
    df_clicks.fillna(0, inplace=True)
    df_clicks['success'] = df_clicks['clicked']/(df_clicks['clicked'] + df_clicks['notclicked'])
    df_clicks['success_std'] = df_clicks['clicked'].apply(sqrt)/(df_clicks['clicked'] + df_clicks['notclicked'])
    #df_clicks.fillna(0, inplace=True)
    return df_clicks


def plot_success_trend(df, color='b', **kwargs):
    """Plot the success variable in the given data frame."""
    label = kwargs.get('label', None)
    ax = df.success.plot(c=color, label=label)
    plt.ylabel('Success')
    try:
        plt.fill_between(df.index, df.success - df.success_std,
                         df.success + df.success_std, color=color,
                         alpha=0.2)
    except TypeError:
        pass
    return ax


def get_success_time_series_df(df, field, values, dt="D"):
    """Return success dataframe for the given values of the given field."""
    ts_list = []
    for ival in values:
        #ts_list.append(get_success_time_series(df[df[field] == ival], dt))
        idf = get_success_time_series(df[df[field] == ival], dt)
        ts_list.append(idf.success)
    return pd.concat(ts_list, axis=1, keys=values)

def plot_success_trends(df, field, values, dt="D"):
    """Plot sucess for a list of values from a given field."""
    legend_list = []
    for ival in values:
        idf = get_success_time_series(df[df[field] == ival], dt)
        if len(idf) < 1:
            continue
        ax = plot_success_trend(idf, color=next(colors))
        legend_list.append("{} {}".format(field, ival))
    x1, x2, y1, y2 = plt.axis()
    plt.axis((x1, x2, y1, min(1, y2)))
    ax.legend(legend_list, loc="best")
    return ax


def plot_click_trends(df, field, values, dt="D"):
    """Plot clicks for a list of values from a given field."""
    legend_list = []
    for ival in values:
        idf = get_success_time_series(df[df[field] == ival], dt)
        if idf.clicked.sum() < 1:
            print('\nno values for {}={}...'.format(field, ival))
            continue
        ax = idf.clicked.plot(c=next(colors))
        legend_list.append("{} {}".format(field, ival))
    ax.legend(legend_list, loc="best")
    plt.ylabel('# of clicks')
    return ax

def plot_impression_trends(df, field, values, dt="D"):
    """Plot clicks for a list of values from a given field."""
    legend_list = []
    for ival in values:
        idf = get_success_time_series(df[df[field] == ival], dt)
        if idf.clicked.sum() < 1:
            print('\nno values for {}={}...'.format(field, ival))
            continue
        ax = (idf.clicked + idf.notclicked).plot(c=next(colors))
        legend_list.append("{} {}".format(field, ival))
    ax.legend(legend_list, loc="best")
    plt.ylabel('# of imporessions')
    return ax


def plot_click_bar_trends(df, field, values, dt="D"):
    """Plot clicks for a list of values from a given field."""
    legend_list = []
    width = 0.8/len(values)
    for idx, ival in enumerate(values):
        idf = get_success_time_series(df[df[field] == ival], dt)
        if idf.clicked.sum() < 1:
            print('\nno values for {}={}...'.format(field, ival))
            continue
        ax = idf.clicked.plot(kind='bar',color=next(colors),
                              position=idx+1, width=width)
        legend_list.append("{} {}".format(field, ival))
    ax.legend(legend_list, loc="best")
    plt.ylabel('# of clicks')
    return ax


def get_ts_corr(df_ts, min_periods=10):
    """Return dataframe of value pair correlations of given field"""
    # All possible value pairs for correlations
    ts_pairs = list(itertools.combinations(df_ts.columns, 2))
    pairs = []
    correls = []
    for ipair in ts_pairs:
        icor = df_ts[ipair[0]].corr(df_ts[ipair[1]], min_periods=min_periods)
        if not np.isnan(icor):
            pairs.append(ipair)
            correls.append(icor)
            print("{} : {}".format(ipair, icor))
    dfcorr = pd.DataFrame({'pairs': pairs, 'corr': correls})
    return dfcorr.sort('corr', ascending=False)


def make_all_corr(df):
    """Make plots for all correlations."""
    for icol in df.columns:
        if icol in ('id', 'click', 'hour'):
            continue
        print('processing {}...'.format(icol))
        sys.stdout.flush()
        idf_succ = click_succ.get_most_successfuls_df(df, icol, 1, False)
        itop_val = idf_succ[idf_succ.clicked > 1].index.tolist()
        idfts = get_success_time_series_df(df, icol, itop_val[:50])
        idfcorr = get_ts_corr(idfts)
        if len(idfcorr) < 2:
            print('Not enough correlations made it to the dataframe for field {}'.format(icol))
            continue
        print(idfcorr)
        ifig = plt.figure()
        idfcorr['corr'].hist(bins=30)
        plt.xlabel("paired {} correlations".format(icol))
        ifig.show()
        ifig.savefig('plots/corr_{}.png'.format(icol))



if __name__ == '__main__':
    df = pd.read_csv("data/train.csv", dtype={'id':str})
    #df = pd.read_pickle("data/df_9000000.pkl")
    #df = pd.read_pickle("data/df_10000.pkl")
    df['time'] = pd.to_datetime(df['hour'], format='%y%m%d%H')
    df.set_index('time', inplace=True)
    #plot_click_trends(df, "banner_pos", [0,1])
    #df_ts = get_success_time_series_df(df, "app_domain", df.app_domain.unique())
    #df_corr = get_ts_corr(df_ts)
    #print(df_corr)
    make_all_corr(df)
