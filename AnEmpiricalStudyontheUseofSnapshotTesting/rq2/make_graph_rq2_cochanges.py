import ast
from collections import Counter

import pandas as pd
import plotly.express as px


from AnEmpiricalStudyontheUseofSnapshotTesting.util.db_util import get_st_update_dataset



def plot_update_rate(df):
    #絞る
    # df = df_.query('Metrics in ["Unit tests", "Snapshot tests"]')
    fig = px.violin(df, y="Ratio", x = "Files", color = 'Files', box=True).update_yaxes(matches=None,
                                                                                                         showticklabels=True,
                                                                                                         title_text=True)
    fig.update_traces(spanmode = 'hard', box_width=0.2, box_fillcolor="rgba(0,0,0,0.2)",box_line_width= 1, box_line_color="rgba(0,0,0,1)", selector=dict(type='violin'))
    fig.update_yaxes(matches=None, showticklabels=True, title_text="Percentage of co-changes with snapshot files")
    fig.update_layout(
        legend=dict(
            x=1.20,#to remove legend
            y=1.2,
            borderwidth=1,
            font=dict(size=12),
        ),
        legend_title=dict(
            font=dict(size=12)
        ),
        height=450, width=800, font=dict(size=12)
    )
    # MANUAL
    # fig.update_yaxes(range=(-32, 1000), row=1, col=1)
    # fig.update_yaxes(range=(-0.5, 25), row=1, col=2)

    fig.write_image("rq2-2.pdf")

def calc_ratio(li_df):

    changed_files_rates = dict()
    for project_df in li_df:
        counter = Counter()
        commits_num = 0
        for idx, commit in project_df.iterrows():
            commits_num +=1
            changed_files = ast.literal_eval(commit['files'])
            file_set = set()
            for f in changed_files:
                if f.endswith(".snap"):
                    continue
                el = f.split("/")
                filename = el[len(el)-1]
                _ = filename.split(".")
                if (len(_)==1):
                    file_type = _[0]
                elif _[-2]=="spec":
                    file_type = "spec."+_[-1]
                elif _[-2]=="test":
                    file_type = "test."+_[-1]
                else:
                    file_type = _[-1]
                file_set.add(file_type)
            for f in file_set:
                counter[f]+=1
        for ele in counter:
            rate = counter[ele]/commits_num
            if ele in changed_files_rates:
                changed_files_rates[ele].append(rate)
            else:
                changed_files_rates[ele] = [rate]
    print(changed_files_rates)
    freq = {}
    for c in changed_files_rates:
        print(c, len(changed_files_rates[c]))
        freq[c] = len(changed_files_rates[c])
    sorted_freq = sorted(freq.items(), key=lambda x:x[1], reverse=True)
    files = []
    values = []
    for filename in sorted_freq[0:10]:
        for rate in changed_files_rates[filename[0]]:
            files.append(filename[0])
            values.append(rate)

    return pd.DataFrame(data={"Ratio": values, "Files": files})

if __name__ == "__main__":

    li_df = get_st_update_dataset()
    df = calc_ratio(li_df)
    plot_update_rate(df)
