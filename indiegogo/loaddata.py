import pandas as pd

projects = pd.read_csv('projects.tsv',delimiter='\t')
goals = pd.read_csv('goals.tsv',delimiter='\t')
users = pd.read_csv('users.tsv',delimiter='\t')
backers = pd.read_csv('backers.tsv',delimiter='\t')


projects[['url','category','location']] = projects[['url','category','location']].astype(str)
projects = projects.dropna(how='any', subset=['start_date','end_date'])
projects[['start_date','end_date']] = projects[['start_date','end_date']].apply(pd.to_datetime)
locations = projects['location'].str.split(', ')
projects['city'] = locations.str[0]
projects['country'] = locations.str[-1]
booleans = locations.str[1] != locations.str[-1]
rows_with_states = locations[booleans].str[1]
projects['state'] = rows_with_states
projects['state'] = projects['state'].fillna('')

#import matplotlib as mpl
#mpl.use('Agg')

#def do_plot(plotobj, xlabel, ylabel, title, filename):
#    mpl.pyplot.ylabel(ylabel)
#    mpl.pxplot.xlabel(xlabel)
#    mpl.pyplot.title(title)
#    figure = plotobj.get_figure()
#    figure.savefig(filename)
#    mpl.pyplot.clf()

#import IPython
#IPython.embed(user_ns=locals())
