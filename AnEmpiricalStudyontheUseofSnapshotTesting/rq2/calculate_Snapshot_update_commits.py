import sqlite3
from AnEmpiricalStudyontheUseofSnapshotTesting.settings import db_dir

Amount_Snapshot_update_commits=0
commits=0
"""
only commit that there is a possibility to update snapshot file in are counted
so if no ST test method in a commit,the commit is ignored
"""


for i in range(476):
    conn=sqlite3.connect(db_dir+'dbStupdate/'+str(i)+'STupdate.db')
    cur=conn.cursor()
    cur.execute('SELECT * FROM stupdates ORDER BY id desc')
    oldest=cur.fetchone()
    if oldest is not None:
        Amount_Snapshot_update_commits+=int(oldest[2])
        commits+=int(oldest[3])
    print(Amount_Snapshot_update_commits)
    print(commits)

print(Amount_Snapshot_update_commits/commits)