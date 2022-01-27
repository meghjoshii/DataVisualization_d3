from django.http import HttpResponse
from django.shortcuts import render
import pandas_gbq
from google.oauth2 import service_account

# Make sure you have installed pandas-gbq at first;
# You can use the other way to query BigQuery.
# please have a look at
# https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-nodejs
# To get your credential

credentials = service_account.Credentials.from_service_account_file('/Users/meghanajoshi/Desktop/Big Data Analytics/BDA HW3/Code/hw3_part2/hw3_part2/micro-flight-331021-4e0a6fdd956d.json')

def hello(request):
    context = {}
    context['content1'] = 'Hello World!'
    return render(request, 'helloworld.html', context)


# def dashboard(request):
#     pandas_gbq.context.credentials = credentials
#     pandas_gbq.context.project = "micro-flight-331021"

#     SQL = "SELECT *"\
#           "FROM `micro-flight-331021.hw3.wordcount3`"\
#           "LIMIT 10"

#     df = pandas_gbq.read_gbq(SQL)
#     df_list = df.to_dict('records')
    
#     li= []
#     for row in df_list:
#         row1 = dict()
#         row1["Time"] = row["time"].strftime(format = "%H:%M")
#         row = dict(row)
#         row.pop("time")
#         row1["count"] = row
#         li.append(row1)

#     data = {}
#     data["data"] = li

#     '''
#         TODO: Finish the SQL to query the data, it should be limited to 8 rows. 
#         Then process them to format below:
#         Format of data:
#         {'data': [{'Time': hour:min, 'count': {'ai': xxx, 'data': xxx, 'good': xxx, 'movie': xxx, 'spark': xxx}},
#                   {'Time': hour:min, 'count': {'ai': xxx, 'data': xxx, 'good': xxx, 'movie': xxx, 'spark': xxx}},
#                   ...
#                   ]
#         }

#     '''
#     print(data)
#     return render(request, 'dashboard.html', data)

def dashboard(request):
    pandas_gbq.context.credentials = credentials
    pandas_gbq.context.project = "micro-flight-331021"

    SQL = "SELECT * FROM `micro-flight-331021.hw3.wordcount3` LIMIT 10"
    df = pandas_gbq.read_gbq(SQL)

    data = {}

    '''
        TODO: Finish the SQL to query the data, it should be limited to 8 rows. 
        Then process them to format below:
        Format of data:
        {'data': [{'Time': hour:min, 'count': {'ai': xxx, 'data': xxx, 'good': xxx, 'movie': xxx, 'spark': xxx}},
                  {'Time': hour:min, 'count': {'ai': xxx, 'data': xxx, 'good': xxx, 'movie': xxx, 'spark': xxx}},
                  ...
                  ]
        }
    '''
    res = []
    words = ['ai', 'data', 'good', 'movie', 'spark']
    time = sorted(list(df.time))
    for i in time:
        if str(i) == "2019-10-23 02:37:20+00:00" or str(i) == "2019-10-23 02:38:20+00:00":
            #print("here", i)
            continue
        temp = {}
        temp['Time'] = str(i)[11:16]
        temp['count'] = {}
        for j in words:
            temp['count'][j] = int(df[df.time == i][j])
        res.append(temp)
    data['data'] = res
    return render(request, 'dashboard.html', data)


def connection(request):
    pandas_gbq.context.credentials = credentials
    pandas_gbq.context.project = "micro-flight-331021"

    SQL1 = 'SELECT node ' \
           'FROM `micro-flight-331021.hw3.nodes`'
    df1 = pandas_gbq.read_gbq(SQL1)

    SQL2 = 'SELECT source, target ' \
           'FROM `micro-flight-331021.hw3.edges`'
    df2 = pandas_gbq.read_gbq(SQL2)

    data = {
        'n': list(df1.T.to_dict().values()),
        'e': list(df2.T.to_dict().values())
    }

    '''
        TODO: Finish the SQL to query the data, it should be limited to 8 rows. 
        Then process them to format below:
        Format of data:
        {'n': [xxx, xxx, xxx, xxx],
         'e': [{'source': xxx, 'target': xxx},
                {'source': xxx, 'target': xxx},
                ...
                ]
        }
    '''
    return render(request, 'connection.html', data)
