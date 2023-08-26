import os
import sys
sys.path.append(os.pardir)


from statistics import median, mean
import plotly.express as px
from AnEmpiricalStudyontheUseofSnapshotTesting.util.db_util import get_birth_dataset
import scipy.stats as stats




def plot_birth_rate(df):
    #絞る
    # df = df_.query('Metrics in ["Unit tests", "Snapshot tests"]')
    fig = px.violin(df, y="Value", x = "Metrics", color = 'Metrics', box=True).update_yaxes(matches=None,
                                                                                                         showticklabels=True,
                                                                                                         title_text=None)
    fig.update_traces(spanmode = 'hard', box_width=0.09, box_fillcolor="rgba(0,0,0,0.2)",box_line_color="rgba(0,0,0,1)",box_line_width= 0.9, selector=dict(type='violin'))
    fig.update_yaxes(matches=None, showticklabels=True)#title_text="Percentage of the files made with file creation"
    fig.update_layout(
    legend = dict(
        x=1.2,
        y=1.2,
        borderwidth=1,
        font=dict(size=12),
    ),
    legend_title = dict(
        font=dict(size=12)
    ),
        height=350, width=600, font=dict(size=12)
    )

    # MANUAL
    # fig.update_yaxes(range=(-32, 1000), row=1, col=1)
    # fig.update_yaxes(range=(-0.5, 25), row=1, col=2)
    # fig.show()
    fig.write_image("rq2.pdf")

def calculate_statistics(df):
    print(df)
    for t in ["Snapshot tests", "Unit tests"]:
        values = df[df['Metrics'] == t]['Value']
        print(f"  {t}")
        print(f"    max:{max(values)}")
        print(f"    median:{median(values)}")
        print(f"    average:{mean(values)}")
        print(f"    min:{min(values)}")
        print(f"    len:{len(values)}")

    ut = df[df['Metrics'] == "Unit tests"]['Value']
    st = df[df['Metrics'] == "Snapshot tests"]['Value']

    print(f"UT vs ST:{stats.mannwhitneyu(ut,st)}")


if __name__ == "__main__":
    df = get_birth_dataset()
    plot_birth_rate(df)
    calculate_statistics(df)
