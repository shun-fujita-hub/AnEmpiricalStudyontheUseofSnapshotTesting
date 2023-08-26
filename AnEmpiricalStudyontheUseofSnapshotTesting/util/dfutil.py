from statistics import median, mean

import scipy.stats as stats

def calculate_statistics(df, metrics):
    for m in metrics:
        print(m)
        d = df[df.Metrics == m]
        for t in ["UT", "ST", "UT+ST"]:
            values = d[d['Project Type'] == t]['Value']
            print(f"  {t}")
            print(f"    max:{max(values)}")
            print(f"    median:{median(values)}")
            print(f"    average:{mean(values)}")
            print(f"    min:{min(values)}")
            print(f"    len:{len(values)}")

        ut = d[d['Project Type'] == "UT"]['Value']
        st = d[d['Project Type'] == "ST"]['Value']
        ust = d[d['Project Type'] == "UT+ST"]['Value']

        print(f"UT vs ST:{stats.mannwhitneyu(ut,st)}")
        print(f"UT vs UT+ST:{stats.mannwhitneyu(ut,ust)}")
        print(f"ST vs UT+ST:{stats.mannwhitneyu(st,ust)}")
    pass
