import math
import mysql.connector
import librosa
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from decimal import Decimal

#connector to mysql data
db = mysql.connector.connect(
   host = "localhost",
   user = "root",
   password = "",
   database = "knn"
)

cur = db.cursor()


y, sr = librosa.load(r'C:\Users\STALINIUM\Music\music class\rock\thunder.mp3')
oe = librosa.onset.onset_strength(y=y, sr=sr)
t = librosa.beat.tempo(onset_envelope = oe, sr=sr)
listToStr = ' '.join([str(elem) for elem in t])
mfccs = librosa.feature.mfcc(y=y, sr=sr)
q = mfccs[0, :1]
listToSt = ' '.join([str(elem) for elem in q])
d, r = sf.read(r'C:\Users\STALINIUM\Music\music class\rock\thunder.mp3')
m = pyln.Meter(r)
l = m.integrated_loudness(d)
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
w = librosa.feature.mfcc(S=librosa.power_to_db(S))
e = w[0, :1]
listToS = ' '.join([str(elem) for elem in e])

#store data from sql for processing
x = []
y = []
x2 = []
y2 = []
cla = []
res = []
dict = {}
 
#query sql to get data
sql = "SELECT * FROM music"
cur.execute(sql)
r = cur.fetchall()

#after query data append to array
for data in r:
    x.append(data[1])
    y.append(data[2])
    x2.append(data[3])
    y2.append(data[4])

#eucledian sum
for sum in range(len(x)):
    a = int(float(listToStr)) -  int(float(x[sum]))
    a = a ** 2
    b = int(float(listToSt)) -  int(float(y[sum]))
    b = b ** 2
    c = int(float(l)) -  int(float(x2[sum]))
    c = c ** 2
    d = int(float(listToS)) -  int(float(y2[sum]))
    d = d ** 2
    e = a + b + c + d
    res.append(str(math.sqrt(e)))

m = 0

for r in res:
      m = m + 1
      sql = "UPDATE music SET hitung = %s WHERE id_c = %s"
      val = str(r), str(m)
      cur.execute(sql,val)      
      db.commit()

sql = "SELECT tempo, class, hitung FROM music ORDER BY hitung ASC LIMIT 5"
cur.execute(sql)
r = cur.fetchall()

for data in r:
      cla.append(data[1])

import collections

for w, c in collections.Counter(cla).most_common():
    dict[repr(w)] = c
    f = list(dict)[0]

print(dict)
print(f)
      
 


