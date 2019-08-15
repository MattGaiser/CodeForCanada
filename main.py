import csv
import random
from datetime import datetime
from flask import Flask, render_template


def compareTime(date1, date2):
    if datetime.strptime(date1, '%Y-%m-%d %H:%M') > datetime.strptime(date2,'%Y-%m-%d %H:%M'):
        return date2
    else:
        return date1

def compareTime2(date1, date2):
    if datetime.strptime(date1, '%Y-%m-%d %H:%M') > datetime.strptime(date2, '%Y-%m-%d %H:%M'):
        return date1
    else:
        return date2

class code_violation:
  def __init__(self, category, earlydate, laterdate):
    self.category = category
    self.earlydate = earlydate
    self.laterdate = laterdate
    self.count = 1

app = Flask(__name__, template_folder='template')

@app.route('/')
def chart():
    with open('C4C-dev-challenge-2018.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        i = 0
        category_list = []
        for row in reader:
            if (i == 0):
                i += 1
                continue
            else:
                    alert = False
                    for l in category_list:
                        if (row[2] == l.category):
                            alert = True
                            l.count += 1
                            l.earlydate = compareTime(row[3], l.earlydate)
                            l.laterdate = compareTime2(row[3], l.laterdate)
                            break
                    if (alert == False):
                        violation = code_violation(row[2], row[3], row[3])
                        category_list.append(violation)

    labels, values, tabledata = [[],[],[]]
    colours = []
    r = lambda: random.randint(0, 255)
    for l in category_list:
        labels.append(l.category)
        values.append(l.count)
        temp = []
        temp.append(l.category)
        temp.append(l.earlydate)
        temp.append(l.laterdate)
        tabledata.append(temp)
        colours.append('#%02X%02X%02X' % (r(), r(), r()))

    print(colours)
    return render_template('index.html', set=zip(values, labels, colours),tableList=tabledata)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)