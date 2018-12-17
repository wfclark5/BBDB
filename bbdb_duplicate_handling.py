import pandas

bbdb_duplicates = pandas.read_csv("bbdb_duplicates.csv")

df = bbdb_duplicates.groupby(bbdb_duplicates['fnlmerge'])
df = df.max().reset_index()

df.to_csv("test.csv")