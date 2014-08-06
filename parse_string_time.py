# Title: Convert a string time stamp in the form 2008-12-02 11:11:00 into multiple numeric fields [year] [month] [day] [hour] [minute] [second] 
import graphlab as gl

sf = gl.SFrame({'dtime':['2000-08-21 03:02:01','2013-06-08 17:25:00','2001-02-29 12:45:00'],'id':[1,2,3]})
print sf
def extract_time_fields(data):
  date_splits = data.split()[0].split('-')
  time_splits = data.split()[1].split(':')
  return {
    'year': int(date_splits[0]),
    'month': int(date_splits[1]),
    'day': int(date_splits[2]),
    'hour': int(time_splits[0]),
    'minute': int(time_splits[1]),
    'second': int(time_splits[2])
  }

time_splits = sf['dtime'].apply(lambda x: extract_time_fields(x))
sf.add_columns(time_splits.unpack())
print sf
