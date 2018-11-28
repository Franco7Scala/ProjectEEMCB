import pandas
import matplotlib.pyplot as plotter

df = pandas.read_csv("/Users/francesco/Desktop/dataset_refixed.txt", sep=" ")
columns = df.columns
for column in columns:
    fig = plotter.figure()
    plotter.title(column)
    plotter.plot(df[column])
    fig.set_size_inches(78.5, 10.5)
    fig.savefig(column + ".pdf", format="pdf")

