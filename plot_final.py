def plotly(df): 
    #imports
    import pandas as pd
    import numpy as np
    import re
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    #reads the input file which has data and converts it into a dataframe
    dataframe = df
    #dataframe = pd.read_csv('match_data3.csv')
    

    #final result details
    results_ = dataframe.result.unique()

    #the followinng code will find the max points reached in the game, so that we can plot that many columns on graph
    de = re.split('-|,| ',results_[0])
    de = [int(x) for x in de if x!= '']
    #columns_ = max(de)
    dataframe.rename(columns={'round':'round_'}, inplace = True)
    tournament_name = dataframe.tournament.unique()
    round_number = dataframe.round_.unique()
    #Drops unrequired columns
    dataframe.drop(['player1_name','player2_name','tournament','round_','break_point','result','surface','date'], axis=1, inplace=True)

    #Finds the players names
    playernames = dataframe.server.unique()
    title = (' Players: '+playernames[0]+' and '+playernames[1] +' Tournament: '+tournament_name+' Round: '+round_number)
    
    #sets a new column as servernumber denotes 0 or 1 on basis of who is playing
    dataframe['server_number'] = np.where(dataframe['server'] == playernames[0], 0, 1)

    #follwing code takes the points and splits the points into sepeate values for two players.
    # def split_it(point):
    #     x = point.split('-')
    #     return x
    dataframe['points_to_list'] = dataframe['points'].apply(split_it)
    dataframe[['points_of_1','points_of_2']] = pd.DataFrame(dataframe.points_to_list.tolist())

    #rename few columns name for further operation like set_index
    dataframe.rename(columns={'set_index':'set_details'}, inplace = True)

    #no_of_sets for use of no of plots.
    no_of_sets = dataframe.set_details.unique()

    dataframe['set_number']= 0

    #following code to create x axis, like only markers
    # def set_number_(lis,set_):
    #     global i,set_no
    #     if set_no != set_:
    #         i = 0
    #         set_no = set_
    #     if lis == ['0','0']:
    #         i = i+1
    #     return i

    #global variables i and set_no
    global i,set_no
    i = 0
    set_no = 0
    dataframe['set_number'] = dataframe.apply(lambda x: set_number_(x['points_to_list'],x['set_details']), axis = 1)

    columns_ = []
    for k in no_of_sets:
        set_details_unique_ = dataframe.where(dataframe['set_details']==k).set_number.unique()
        cleanedList = [int(x) for x in set_details_unique_ if str(x) != 'nan']
        columns_.append(max(cleanedList))

    #plot
    fig = make_subplots(
        rows=len(no_of_sets), cols=max(columns_))


    for k in no_of_sets:
        df= dataframe[dataframe['set_details']==k]
        for r in range(1,columns_[k-1]+1):
            
            final_df = (df[df['set_number'] == r])
            max_x= (len(final_df['set_number']))
            x_ = np.arange(0, max_x,1)
            fig.add_trace(
                go.Scatter(x=x_,y=final_df['points_of_1'],line_color = "red"),
                row=k, col=r)
            fig.add_trace(
                go.Scatter(x=x_, y=final_df['points_of_2'],line_color ="blue"),
                row=k, col=r)
        


    #Update height, width and title
    fig.update_layout(autosize=False,height=1000, width=3000, title_text=title[0])

    fig.update_yaxes(tickvals=['0', '15', '30', '40'])

    #Make labels disappear on x axis
    fig.update_xaxes(showticklabels=False)

    #Don't display the trace values in the charts
    fig.update_layout(showlegend=False)

    #Make x axes disappear
    fig.update_xaxes(showgrid=False,zeroline=False)

    #Make y axes disappear
    fig.update_yaxes(showgrid=False,zeroline=False)

    #Display all charts
    #fig.show()
    return fig

def split_it(point):
    x = point.split('-')
    return x

def set_number_(lis,set_):
    global i,set_no
    if set_no != set_:
        i = 0
        set_no = set_
    if lis == ['0','0']:
        i = i+1
    return i