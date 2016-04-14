import utils
import sys
import matplotlib
matplotlib.use('Agg')
import pylab as pl
import numpy as np
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve , auc

if len(sys.argv) !=2:
    print "Usage: python create_chart.py db-col-name"
    sys.exit(0)

column=sys.argv[-1]
db=utils.get_db_con()
cur=db.cursor()
cur.execute("SELECT category,"+ column+" FROM newsitem where category is not NULL;")
true_labels=[]
predicted_labels=[]
for i in cur:
    if int(i[0])==1 or int(i[0])==2:
	true_labels.append(1)
    else:
	true_labels.append(0)
    predicted_labels.append(int(i[1]))

pl.clf()
precision, recall, thresholds = precision_recall_curve(true_labels, predicted_labels)
pl.plot(recall, precision, linestyle='-')
print "PR curve: %s_pr.png" %column
pl.xlabel('Recall')
pl.ylabel('Precision')
pl.title('PR')
pl.savefig(column+'_pr.png')

### ROC
pl.clf()
fpr, tpr, thresholds = roc_curve(true_labels, predicted_labels)
pl.plot(fpr, tpr, linestyle='-')
print "ROC curve: %s_roc.png" %column
pl.xlabel('False Positive Rate')
pl.ylabel('True Positive Rate')
pl.title('ROC')
pl.savefig(column+'_roc.png')
