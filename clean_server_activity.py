import re
import pickle
import numpy as np


def clean():
    # Loads a dictionary where the key is the crawled webpage's id for the server
    # and the value is a tuple consisting of server name and server activity as a Pandas DataFrame

    wacraft_server_activity = pickle.load(open("crawled_server_activity.p", 'rb'))

    servername_and_dataframe = {}
    for _, name_df_tuple in wacraft_server_activity.items():
        server_name, dataframe = name_df_tuple
        server_name = re.sub(r" ?- ?[A-Z]{2,}", '', server_name)  # Clean server name of bynames like "PVP

        server_name = re.sub(r"EU-", '', server_name)
        server_name = server_name.strip()
        dataframe = dataframe.drop(["alliance_entries", 'horde_entries'], axis=1).replace(np.nan, 1)

        dataframe = dataframe.sum(axis=1).astype(int, copy=False)  # Sum over alliance and horde activity
        servername_and_dataframe[server_name] = dataframe

    # Remove completely empty DataFrames
    empty_dfs = [key for key in servername_and_dataframe if
                 servername_and_dataframe[key].isin([0]).all().all()]
    for key in empty_dfs:
        servername_and_dataframe.pop(key)

    pickle.dump(servername_and_dataframe, open('cleaned_server_activity.p', 'wb'))
