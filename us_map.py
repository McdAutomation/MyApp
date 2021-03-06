from bokeh.plotting import figure
from bokeh.models import HoverTool, TapTool
from bokeh.models.callbacks import CustomJS
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.models import Text
#  internal imports
from plotting import plot_county, plot_restaurants

class US_country:

    def __init__(self):
        self.map = figure(plot_width=1160, plot_height=600, x_range=(-160, -60), y_range=(15, 55), #w:h 1382:700 x--200 50 y- 0 100
                          output_backend="webgl", x_axis_label="x", y_axis_label='y', toolbar_location='left')


        self.map.axis.visible = False
        self.renderedBy = {}

    def __enter__(self):
        print("entered")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exited")
        pass
    '''
    def create_hover_tool_map(self):
        """Generates the HTML for the Bokeh's hover data tool on our graph."""
        hover_html = """
          <div>
            <span class="hover-tooltip">Country: @NAME
          </div>
            """
        return HoverTool(renderers=[self.renderedBy['patch']], tooltips=hover_html)
    '''
    def returnFigureComponents(self):
        #  self.renderedBy['patch'] = self.figPatch.patches('x', 'y', source=bokPatch, line_color='black', line_width=0.3,legend='World', name='patchCustomName')
        #self.draw_patch(bokPatch, legend='World', name='patchCustomName')

        #  for Ajax calls
#        cir = AjaxDataSource(data_url=request.url_root + 'stores/',  # change to listen to different endpoints
#                                polling_interval=3000, mode='replace', name='circleAjax')

#       cir.data = dict(x=[], y=[], name=[], color=[])

        #pt = self.figPatch.circle(x='x', y='y', source=cir, size=5, color='color', legend='Restaurant')

        cir = ColumnDataSource(dict(x=[], y=[], name=[], color=[], addressline=[], nsn=[], time=[]))

        self.renderedBy['restaurant'] = self.map.circle(x='x', y='y', size=5, source=cir, color='color',
                                                         legend='Restaurant', name='circleCDS')

        self.renderedBy['county'], county_column_source = plot_county(self.map)

        def create_pop_up_marker():  # remember bokPatch is the source here which is ColumnDataSource
            tap_to_get = CustomJS(args=dict(source=cir), code="""

                window.toBeClearedTimer = 1; // clear timer on next click
                window.drawnTimer = 1;

                data = source.data;

                //var inds = cb_obj.source.attributes.selected['1d'].indices; 
                //d = cb_obj.data;
                var popupWindow = window.open("/popup", "MsgWindow", "top=200, left=200, width=800, height=500");


                /*var a = myWindow.document.createElement('a');
                var linkText = myWindow.document.createTextNode("Click Here!!");
                a.appendChild(linkText);
                a.title = "my title text";
                a.href = "http://www.google.com";
                myWindow.document.body.appendChild(a);*/


                selectedVariable = source.selected['1d'].indices;
                console.log(selectedVariable.length);
                //d = cb_obj.data;

                //console.log(cb_data);
                //console.log(cb_obj);
                //console.log(selectedVariable);
                //console.log(data["NAME"][selectedVariable[0]]); //extraction of attributes of selected glyph done!!!

                //myWindow.document.write(cb_data.geometries);

                //var ind = cb_obj.selected['1d'].index;
                //var country = cb_obj.get('NAME');
                //var st="anupam";     
                //myWindow.document.write("<p>hey there</p>");
                //ctry_name = data['name'][selectedVariable];
                //console.log(ctry_name);

                var arr_timedata= data['time'][selectedVariable].split(':');
                hr = parseInt(arr_timedata[0]);
                min = parseInt(arr_timedata[1]);

                //ctx.restore();
                ctx.clearRect(-100, -100, canvas.width, canvas.height);
                window.color = JSON.stringify(data['color'][selectedVariable]);
                console.log(window.color);
                if (window.color == JSON.stringify("red")){
    window.minuteSLA = 15;
                }else if(window.color == JSON.stringify("yellow")){
                    window.minuteSLA = 45;
                }else if(window.color == JSON.stringify("fuchsia")){
                    window.minuteSLA = 90;
                }else if(window.color == JSON.stringify("aqua")){
                    window.minuteSLA = 120;
                }
                ctx.fillStyle = JSON.parse(window.color);
                console.log(window.minuteSLA);
                ctx.beginPath();
                ctx.moveTo(0,0);
                var now = new Date();
                var hour = now.getHours();
                var minute = now.getMinutes();
                var second = now.getSeconds();

                var timeMinutes = (hour - hr)*60*60 + (minute - min)*60+second;

                if( (timeMinutes/60 >= window.minuteSLA ) || (hour<hr) || ((minute<min) && (hour==hr)) ){
                    //clearInterval(window.refreshIntervalId);
                    ctx.clearRect(-radius-5, -radius-5, canvas.width, canvas.height);
                    animCtx.clearRect(-radius-5, -radius-5, canvas.width, canvas.height);
                    clearInterval(window.refreshIntervalId);
                    ctx.arc(0, 0, radius, -Math.PI/2, 3*Math.PI/2);
                    console.log(window.color);
                    ctx.fillStyle = window.color;
                    ctx.fill();
                    console.log("cleared");
                    console.log(hr+" "+hour+" "+timeMinutes/60);
                  }
                else{
                     window.refreshIntervalId = setInterval(drawClock, 1000/60); // to stop later
                     console.log("started");
                }              

                //set data to pop up window in following code
                //console.log(data['name'][selectedVariable]);
                
                //popupWindow.document.getElementById("area").innerHTML = data['name'][selectedVariable];

                popupWindow.window.onload = function() {
                    popupWindow.document.getElementById('nsn').innerHTML = data['nsn'][selectedVariable];
                    popupWindow.document.getElementById('fullName').innerHTML = data['name'][selectedVariable];
                    popupWindow.document.getElementById('area').innerHTML = data['addressline'][selectedVariable];
                    popupWindow.document.getElementById('time').innerHTML = data['time'][selectedVariable];
                               
                }
            """)
            return TapTool(renderers=[self.renderedBy['restaurant']], callback=tap_to_get)

        def create_hover_tool_marker():
            hover_html = """
                  <div>
                    <span class="hover-tooltip">City: @name
                  </div>
                    """
            hover_to_get = CustomJS(args=dict(source=cir), code="""
            var hovered_ind = cb_data.index['1d'].indices[0];
            data = source.data;
            if(hovered_ind != undefined){
                //console.log('inside', hovered_ind);
                //console.log('inside', cb_data['geometry']);

                //console.log("this is the end , my only friend"+data['time'][hovered_ind]);

                var arr_timedata= data['time'][hovered_ind].split(':');
                hr = parseInt(arr_timedata[0]);
                min = parseInt(arr_timedata[1]);

                //ctx.restore();
                ctx.clearRect(-100, -100, canvas.width, canvas.height);
                window.color = JSON.stringify(data['color'][hovered_ind]);
                console.log(window.color);
                if (window.color == JSON.stringify("red")){
    window.minuteSLA = 15;
                }else if(window.color == JSON.stringify("yellow")){
                    window.minuteSLA = 45;
                }else if(window.color == JSON.stringify("fuchsia")){
                    window.minuteSLA = 90;
                }else if(window.color == JSON.stringify("aqua")){
                    window.minuteSLA = 120;
                }
                ctx.fillStyle = JSON.parse(window.color);
                console.log(window.minuteSLA);
                ctx.beginPath();
                ctx.moveTo(0,0);
                var now = new Date();
                var hour = now.getHours();
                var minute = now.getMinutes();
                var second = now.getSeconds();

                var timeMinutes = (hour - hr)*60*60 + (minute - min)*60+second;

                if( (timeMinutes/60 >= window.minuteSLA ) || (hour<hr) || ((minute<min) && (hour==hr)) ){
                    //clearInterval(window.refreshIntervalId);
                    ctx.clearRect(-radius-5, -radius-5, canvas.width, canvas.height);
                    animCtx.clearRect(-radius-5, -radius-5, canvas.width, canvas.height);
                    clearInterval(window.refreshIntervalId);
                    ctx.arc(0, 0, radius, -Math.PI/2, 3*Math.PI/2);
                    console.log(window.color);
                    ctx.fillStyle = window.color;
                    ctx.fill();
                    console.log("cleared");
                    console.log(hr+" "+hour+" "+timeMinutes/60);
                  }
                else{
                     window.refreshIntervalId = setInterval(drawClock, 1000/60); // to stop later
                     console.log("started");
                }              
            }
            """)
            return HoverTool(renderers=[self.renderedBy['restaurant']], tooltips=hover_html, callback=hover_to_get)

        def show_region_wise_data():  # remember bokPatch is the source here which is ColumnDataSource
            tap_to_get = CustomJS(args=dict(source=county_column_source), code="""
                selectedVariable = cb_data.source.selected['1d'].indices[0];
                selectedRegion = source.data["Region"][selectedVariable];
                
                var ds = Bokeh.documents[0].get_model_by_name('circleCDS');
                pointDataSource = ds.attributes.data_source.data;
                totalPoints = ds.attributes.data_source.data['x'].length;
                count = 0;
                
                for(i = 0;i<totalPoints;i++){
                console.log(pointDataSource['addressline'][i]);
                    if((pointDataSource['addressline'][i]) == String(selectedRegion)) 
                    {
                        count += 1;
                    }
                    
                }
                document.getElementById("region").innerHTML = selectedRegion;
                document.getElementById("count").innerHTML = count;
            """)
            return TapTool(renderers=[self.renderedBy['county']], callback=tap_to_get)
        self.map.add_tools(create_pop_up_marker())
        self.map.add_tools(show_region_wise_data())
        return components(self.map)
