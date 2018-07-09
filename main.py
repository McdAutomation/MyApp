from flask import Flask, render_template, request, jsonify, session
from us_map import US_country
import pandas as pd
from flask import g
key = 'AIzaSyCl9gfvmpQoyisgz-lt1epZkU5iVMaoLM0'
app = Flask(__name__)
app.secret_key = key

path_service_now_data = r"D:\Users\Default User\Desktop\SN_IE_LMS.csv"
restaurant_data_US = pd.read_csv("C:/Users/atrivedy/Documents/proj/US.txt",sep="\t")

#_data_temp = pd.read_csv("C:/Users/atrivedy/Documents/Visualilzation/plotting/thisisit.csv",sep=',')
@app.route("/")
def jsonWorld():
    session['searchbody_session'] =  {  # default search P1
        "size": 1000,
        "query": {
            "term": {
                "error": 5
            }
        }
    }
    session['errorcode_session'] = 1
    with US_country() as country:
        script1, div1 = country.returnFigureComponents()
        return render_template("WorldJson.html", script=script1, div=div1)


stored_coordinates = {}


@app.route('/circleAsCDS')
def worldJsonWithCircleCds():
    with US_country() as country:
        script, div = country.returnFigureComponents()
        return render_template("WorldJson.html", script=script, div=div)


@app.route('/storesCDS/', methods=['GET','POST'])
def post_data_storesCDS():
    variable = {'x': [], 'y': [],'nsn':[],'addressline':[], 'name': [], 'time': [], 'color': [], 'ISO2':[]}
    prioritycolors = {}
    # red yellow fuchsia aqua
    prioritycolors[1] = "blue"
    prioritycolors[2] = "blue"
    prioritycolors[3] = 'blue'
    prioritycolors[4] = 'blue'
    if request.method == 'GET':
        sn_data = pd.read_csv(path_service_now_data)
        errorcode = request.args.get('d')

        if errorcode == '1':
            error_query = '1 - High'
        elif errorcode == '2':
            error_query = '2 - High'
        elif errorcode == '3':
            error_query = '3 - High'
        elif errorcode == '4':
            error_query = '4 - High'

        ls = sn_data.loc[sn_data['PrioritySort'] == error_query]
        if len(ls) > 0:
            for i in range(len(ls)):
                variable['x'].append(float(
                    restaurant_data_US.loc[restaurant_data_US['NatlStrNumber'] == int(ls.iloc[i]['LocationSort'])][
                        'Longitude']))
                variable['y'].append(float(
                    restaurant_data_US.loc[restaurant_data_US['NatlStrNumber'] == int(ls.iloc[i]['LocationSort'])][
                        'Latitude']))

                variable['name'].append(ls.iloc[i]['NumberSort'])
                variable['time'].append(ls.iloc[i]['OpenedSort'])
                variable['color'].append(prioritycolors[int(errorcode)])
                variable['nsn'].append(int(ls.iloc[i]['LocationSort']))
                variable['addressline'].append(
                    str(restaurant_data_US.loc[restaurant_data_US['NatlStrNumber'] == int(ls.iloc[i]['LocationSort'])][
                            'Region'].iloc[0]
                    )
                    )

        return jsonify(variable)
    if request.method == 'POST':
        concave_hull_column_data_source = []
        data = request.json

        return jsonify({'success':True})


@app.teardown_appcontext
def initialize(obj):
    pass
    #print("teardown")


@app.route('/popup')
def popup_template():
    return render_template("popup.html")

@app.route('/us_states')
def us_states_mcd():
    with US_country() as country:
        script, div = country.returnFigureComponents()
        return render_template("WorldJson.html", script=script, div=div)
if __name__ == '__main__':
    app.run(debug=False)
