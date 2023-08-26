
import pandas as pd
import plotly.express as px
import seaborn as sns
from pandas import DataFrame
import matplotlib.pyplot as plt

from AnEmpiricalStudyontheUseofSnapshotTesting.util.db_util import get_jest_minimum_and_size_dataset

from AnEmpiricalStudyontheUseofSnapshotTesting.util.dfutil import calculate_statistics

def data_preparation(df):
    data = []
    for label in ["Test cases per 1K-LOC", "Number of Assertions", "Unit Test cases per 1K-LOC", "Snapshot Test cases per 1K-LOC", "lines"]:#"numberOfNotSnapshotTestMethod", "numberOfSnapshotTestMethod"
        data.append(classify(df, label))
    return pd.concat(data, axis=0)

def classify(df: DataFrame, column):
    types = []
    values = []
    metrics = []
    for index, data in df.iterrows():#TODO: Be Pythonic
        if data["numberOfTestMethod"] == 0:
            continue
        values.append(data[column])
        metrics.append(column)
        if data["hasST"] == 0:
            types.append("UT")
        else:
            if data["numberOfTestMethod"] == data["numberOfSnapshotTestMethod"]:
                types.append("ST")
            else:
                types.append("UT+ST")
            pass
    return DataFrame(data={"Project Type":types, "Value": values, "Metrics": metrics})

sns.set(font_scale=10)
plt.style.use('default')
sns.set()
def plot_projects(df_, v, ylim):
    df1 = df_.query(f'Metrics in ["{v}"]')#"Number of Assertions"
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    sns.violinplot(data=df1, x="Project Type", y="Value",ax=ax,cut=0, linewidth=1.5)#.set(title=v)
    ax.set_ylim(0, ylim)
    plt.xlabel('')
    plt.ylabel('')
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.savefig(f'{v}.pdf')

    # fig.write_image("rq1.pdf")


def plot_vs(df_, v, ylim):
    df1 = df_.query(f'Metrics in ["{v}"]')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    sns.violinplot(data=df1, x="Project Type", y="Value",ax=ax,cut=0, linewidth=1.5)#.set(title=v)
    ax.set_ylim(0, ylim)
    plt.xlabel('')
    plt.ylabel('')
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.savefig(f'{v}.pdf')


if __name__ == "__main__":
    df = get_jest_minimum_and_size_dataset()
    df = data_preparation(df)

    df = df.sort_values(by=['Project Type'])
    df = df.replace('numberOfTestMethod', 'Test cases')
    calculate_statistics(df, ["lines", "Test cases per 1K-LOC", "Number of Assertions", "Unit Test cases per 1K-LOC", "Snapshot Test cases per 1K-LOC"])
    plot_projects(df,"Test cases per 1K-LOC", 300)
    plot_projects(df,"Number of Assertions", 25)
    plot_vs(df, "Unit Test cases per 1K-LOC", 400)
    plot_vs(df, "Snapshot Test cases per 1K-LOC", 100)