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

    



    #fill nan values with defalut data when set one or two - missing points information.



    new_df = dataframe[dataframe['points'].isnull()]

    #new_df = new_df[new_df['set_index'].isin([2, 1])]
    new_df = new_df[new_df['set_index'].isin(list(dataframe['set_index'].unique()))]

    #print(new_df)
    if not new_df.empty:
        dataframe.drop(new_df.index[0], inplace=True)

        points_if_1player_winner = ['0-0','15-0','30-0','40-0']

        points_if_2player_winner = ['0-0','0-15','0-30','0-40']

        if new_df['player1_game_score'].tolist()[0] > new_df['player2_game_score'].tolist()[0]:

            x = (points_if_1player_winner)

        else:

            x = (points_if_2player_winner)

        new_df = new_df.append([new_df]*3)

        new_df['points'] = x

        dataframe = dataframe.append(new_df)

        dataframe.reset_index(inplace=True)

        dataframe.drop(['index'], axis=1, inplace=True)



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

    title = " Players: <b style='color:red'>"+playernames[0]+"</b> and <b style='color:green'>"+playernames[1] +"</b> Tournament: "+tournament_name+" Round: "+round_number

    

    #sets a new column as servernumber denotes 0 or 1 on basis of who is playing

    dataframe['server_number'] = np.where(dataframe['server'] == playernames[0], 0, 1)



    #in the data frame we could see some points data is missing as a part of data manipulation and cleaning we are filling the empty fields with player socres like 'player1_score-player2_score'

    dataframe['points'] = dataframe.apply(lambda x:fill_nan_in_points(x['points'],x['player1_game_score'],x['player2_game_score']),axis = 1)



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


    game_graph = dataframe[['set_details','player1_game_score','player2_game_score','set_number']]
    dicti = {}
    for i in list(game_graph.set_details.unique()):
        data = game_graph[game_graph['set_details'] == i]
        records = ((data).set_number.unique())
        x=[]
        y=[]
        for j in records:
            data2 = ((data[data['set_number'] == j]).drop_duplicates())
            x.append(data2['player1_game_score'].values[0])
            y.append(data2['player2_game_score'].values[0])
        dicti[i] = {'x':x,'y':y}

    set_numbers_ = list(dataframe['set_details'].unique())
    for r in set_numbers_:
        data_ = dataframe[dataframe['set_details'] == r]
        set_details_ = list(data_['set_number'].unique())
        for rr in set_details_:
            data__ = data_[data_['set_number']  ==rr]
            content = data__.iloc[-1]
            p1 = int(content['points_of_1'])
            p2 = int(content['points_of_2'])
            if int(p1) >= 40 or int(p2) >= 40:
                if int(p1) > int(p2):
                    p1 = '50'
                else:
                    p2 = '50'

                content['points_of_1'] = p1
                content['points_of_2'] = p2
                dataframe = dataframe.append(content,ignore_index = True)
    #plot    
    dataframe = dataframe[dataframe.points.notnull()]
    #print(dataframe.points)
    fig = make_subplots(

        rows=len(no_of_sets) + len(no_of_sets), cols=max(columns_))
    #fig.update_layout(yaxis=dict(color="#FFFFFF"))


    for k in no_of_sets:

        df= dataframe[dataframe['set_details']==k]
        if k == 1:
            k_g = k
            k_s = k+1
        else:
            k_g = k_g+2
            k_s = k_s+2
        max_x = len(dicti[k]['x'])
        x_ = np.arange(0,max_x,1)
        y_ = dicti[k]['x']
        fig.add_trace(go.Scatter(x=x_, y=y_,line_color ="red"),row=k_g, col=1)
        max_x= (len(dicti[k]['y']))
        x_ = x_ = np.arange(0, max_x,1)
        y_ = dicti[k]['y']
        fig.add_trace(go.Scatter(x=x_, y=y_,line_color ="green"),row=k_g, col=1)
        # print(k_g)
        # print(k_s)

        for r in range(1,columns_[k-1]+1):

            

            final_df = (df[df['set_number'] == r])

            max_x= (len(final_df['set_number']))

            x_ = np.arange(0, max_x,1)

            fig.add_trace(

                go.Scatter(x=x_,y=final_df['points_of_1'],line_color = "red"),

                row=k_s, col=r)

            fig.add_trace(

                go.Scatter(x=x_, y=final_df['points_of_2'],line_color ="green"),

                row=k_s, col=r)




    #Update height, width and title

    #fig.update_layout(autosize=False,height=400*len(no_of_sets), width=300*max(columns_), title_text=title[0])
    fig.update_layout(autosize=False,height=400*len(no_of_sets), width=300*max(columns_), title_text=title[0],title_font_color ="#FFFFFF", paper_bgcolor='rgb(0,0,0)')



    #fig.update_yaxes(tickvals=['0', '15', '30', '40'])
    fig.update_yaxes(color="#FFFFFF")

    #update legend
    fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01))



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
    import pandas as pd

    if len(x) == 2:

        if x[0] == ' A':

            x[0] = '45'

        elif x[1] == 'A':

            x[1] = '45'

    return x



def set_number_(lis,set_):

    global i,set_no
    import pandas as pd

    if set_no != set_:

        i = 0

        set_no = set_

    if lis == ['0','0']:

        i = i+1

    return i



def fill_nan_in_points(point, p1_score,p2_score):

    import pandas as pd
    #print(point, type(point))

    if pd.isnull(point) or len(point) > 6:

        #print(len(point))

        point = str(p1_score)+'-'+str(p2_score)

    return point