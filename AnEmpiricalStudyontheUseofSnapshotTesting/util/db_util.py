import glob
import os
import pathlib
import sqlite3
import pandas as pd

from AnEmpiricalStudyontheUseofSnapshotTesting.settings import db_dir


def get_snapshot_minimum_dataset():
    conn = sqlite3.connect(f'allhasst.db')
    df = pd.read_sql_query('SELECT * FROM repos', conn)
    df = df[df["numberOfTestMethod"]!=0]
    conn.close()
    df["Number of Assertions"] = df["numberOfAssertions"]/df["numberOfTestMethod"]
    return df

def get_jest_full_dataset():
    conn = sqlite3.connect(f'{db_dir}/jsts.db')
    df = pd.read_sql_query('SELECT * FROM repos', conn)
    conn.close()
    return df

def get_snapshot_full_dataset():
    df_snapshot = get_snapshot_minimum_dataset()
    df_jest = get_jest_full_dataset()
    return pd.merge(df_snapshot, df_jest, how="left", on="name")

sizes_db_name = f'sizes.db'
def get_size_dataset():
    print(pathlib.Path(sizes_db_name).resolve())
    conn = sqlite3.connect(sizes_db_name)
    df = pd.read_sql_query('SELECT * FROM sizes', conn)
    conn.close()
    return df

def get_jest_minimum_and_size_dataset():
    df_snapshot = get_snapshot_minimum_dataset()
    assert len(df_snapshot) > 0
    df_size = get_size_dataset()
    assert len(df_size) > 0
    df = pd.merge(df_snapshot, df_size, how="left", on="name")
    df["Test cases per 1K-LOC"] = df["numberOfTestMethod"]/(df["lines"]/1000)
    df["Unit Test cases per 1K-LOC"] = df["numberOfNotSnapshotTestMethod"]/(df["lines"]/1000)
    df["Snapshot Test cases per 1K-LOC"] = df["numberOfSnapshotTestMethod"]/(df["lines"]/1000)
    # for idx, d in df.iterrows():
    #     print(d['Test cases per 1K-LOC'],d['Unit Test cases per 1K-LOC'],d['Snapshot Test cases per 1K-LOC'],
    #           d['Test cases per 1K-LOC']==(d['Unit Test cases per 1K-LOC']+d['Snapshot Test cases per 1K-LOC']) )
    return df


def _get_st_birth_dataset():
    conn = sqlite3.connect(f'{db_dir}/firstST.db')
    df = pd.read_sql_query('SELECT * FROM stupdates', conn)
    conn.close()
    return df

def _get_ut_birth_dataset():
    conn = sqlite3.connect(f'{db_dir}/firstUT.db')
    df = pd.read_sql_query('SELECT * FROM utupdates', conn)
    conn.close()
    return df

def get_birth_dataset():

    df_s = _get_st_birth_dataset()
    df_u = _get_ut_birth_dataset()
    values = []
    metrics = []
    for idx, v in df_s.iterrows():
        if v["AllSTamount"] != 0:
            u = v["FirstSTamount"]/(v["AllSTamount"])
            values.append(u)
            metrics.append("Snapshot tests")
        for idx, v in df_u.iterrows():
            if v["AllUTamount"] != 0:
                u = v["FirstUTamount"]/(v["AllUTamount"])
                values.append(u)
                metrics.append("Unit tests")
    #Classify
    # calc one ratio
    # df = pd.DataFrame({'Unit tests': u_arrays, 'Snapshot tests': s_arrays})
    return pd.DataFrame(data={"Value": values, "Metrics": metrics})


def get_st_update_dataset():
    directory = f"{db_dir}/dbStupdate/"
    li = []
    for name in glob.glob(f'{directory}/*.db'):
        conn = sqlite3.connect(name)
        df = pd.read_sql_query('SELECT files FROM stupdates', conn)
        li.append(df)
        conn.close()
    return li
