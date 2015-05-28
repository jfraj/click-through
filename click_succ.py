import pandas as pd
from math import sqrt


def get_field_click_df(df, field):
    """Return dataframe with clicked/not-clicked summary."""
    # Create two groups for clicked/not-clicked
    clicked_byapp = df[df['click'] == 1].groupby(field)
    notclicked_byapp = df[df['click'] == 0].groupby(field)

    # Create a dataframe out of the above groups
    df_clk = pd.DataFrame(dict(clicked=clicked_byapp['id'].count(),
                          notclicked=notclicked_byapp['id'].count()))
    df_clk.fillna(0, inplace=True)

    return df_clk


def get_field_click_success_df(df, field, prefix=''):
    """Return dataframe with click success.

    Success is determined as (# of clicks)/(# of clicks + # of not-clicks)
    """
    # Success field name
    success_str = 'success'
    if len(prefix) >= 1:
        success_str = '{}_'.format(prefix) + success_str
    std_str = '{}_std'.format(success_str)
    df_clk = get_field_click_df(df, field)
    df_clk[success_str] = df_clk.clicked/(df_clk.notclicked + df_clk.clicked)
    df_clk[std_str] = df_clk['clicked'].apply(sqrt)/(df_clk.notclicked + df_clk.clicked)
    df_clk.sort(success_str, ascending=False, inplace=True)
    return df_clk


def get_most_successfuls(df, field, click_thld=30):
    """Return the list of most successful values of the given field.

    The list contains all statistically compatible values
    The compatibility is determined by agreement within standard deviations
    The list is ordered in success (regardless of std)

    Args:
        df (pandas dataframe): with the field 'field'
        field (str): field of df to be search for successful
        click_thld: Minimal number of counts to be a valid result
    """
    df_clk = get_field_click_success_df(df, field)
    # Keep only values above threshold
    df_clk = df_clk[df_clk.clicked > click_thld]

    print('Top sucessful results')
    print(df_clk[:10])
    if len(df_clk) < 1:
        print '\nError: not enough clicks to satisfy threshold conditions\n'
        return None
    # Requesting all results that are compatible with the most successful
    best, best_std = df_clk.iloc[0][['success', 'success_std']]
    df_clk = df_clk[(df_clk.success + df_clk.success_std) >= (best - best_std)]
    # The dataframe now contains all the statistically comparable results
    if len(df_clk) > 1:
        print('\nStatistically comparable results:')
        print(df_clk)
    return df_clk.index.tolist()


def get_top_most_successfuls(df, field, top=10, click_thld=30):
    """Return dict with list of `top` most successful.

    Output:
        dictionary {'top_succesful': [...], 'stat_compatible': [...]}

    list `top_succesful` contains the top successful results
    list  `stat_compatible` contains results within 1 std of the top list
    The list is ordered in success (regardless of std)

    Args:
        df (pandas dataframe): with the field 'field'
        field (str): field of df to be search for successful
        top (int): number of results in the top list
        click_thld (int): Minimal number of counts to be a valid result
    """
    df_clk = get_field_click_success_df(df, field)
    # Keep only values above threshold
    df_clk = df_clk[df_clk.clicked > click_thld]
    if len(df_clk) < 1:
        print '\nError: not enough clicks to satisfy threshold conditions\n'
        return None
    top_successful = df_clk.index[:top].tolist()

    # Get all the results statistically compatible with the top results
    df_clk['succ_minus_std'] = df_clk['success'] - df_clk['success_std']
    df_clk['succ_plus_std'] = df_clk['success'] + df_clk['success_std']
    lowest_compatible = df_clk[:top]['succ_minus_std'].min()
    stat_compatible = df_clk[df_clk['succ_plus_std'] >= lowest_compatible].index.tolist()
    # Exclude elements in the top list
    stat_compatible = [x for x in stat_compatible if x not in top_successful]
    return {'top_successful': top_successful, 'stat_compatible': stat_compatible}

if __name__ == "__main__":
    #df_train = pd.read_csv('data/train.csv', nrows=1000000)
    df_train = pd.read_csv('data/train.csv')
    #print(get_field_click_df(df_train, "app_domain"))
    #field2search = "app_domain"
    field2search = "site_category"
    minclick = 30
    #most_success = get_most_successfuls(df_train, field2search, minclick)
    most_success = get_top_most_successfuls(df_train, field2search, 10, minclick)
    print('\nMost successful {} : {}\n'.format(field2search, most_success))
