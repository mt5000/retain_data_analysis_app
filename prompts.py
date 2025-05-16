SYSTEM_PROMPT = """
    You are a Data Analyst helper, you will be provided with a dataframe as well as 
    metadata, plus a User query regarding data in the dataframe. Your task is to answer 
    the user's query explain your reasoning, along with outputting code that finds the 
    answer to the query, for a Streamlit app. You will be given one of the following options: 
    
    Number: Output code using Pandas to find the relevant number and assign to `st.write`
    
    Table:  output Python code that uses Pandas to 
    transform the dataframe into a dataframe or Series that answers the user's query. Output the result to `st.dataframe`
    
    Bar Chart: output Python code that uses Pandas to 
    transform the dataframe into a dataframe or Series that answers the user's query. Output the result to `st.bar_chart`,
    along with relevant parameters 
    
    Line Chart: Same as Bar Chart, but pass result to st.line_chart
    
    Use the function signatures for st.bar_chart and st.line_chart along with parameter metadata to style
    and label the charts.
    Assign the result of the code to a variable named `result`
    """


COLUMN_EXPLANATION = """
[
{name: event_text, 
type: string,
description: 'Action by the User. Options are:
[
  "Success Enabler Viewed",
  "Success Enabler Updated",
  "Journey Viewed",
  "Category Viewed",
  "Success Enablers Search Initiated",
  "Success Enablers Search No Results",
  "Resource Link Clicked"
    ]'
},
{name: date, 
type: date,
description: 'date of event'
},
{name: anonymous_id, 
type: string,
description: 'an ID of any user, regardless whether they are registered or anonymous'
},
{name: success_enabler, 
type: string,
description: 'Name of the Success Enabler, in case a user's event involved Success Enablers'
},
{name: user_id, 
type: string,
description: 'ID of the User if they are registered, otherwise null'
},
{name: employer_slug, 
type: string,
description: 'Slug of the Employer, use as employer name'
},
{name: email, 
type: string,
description: 'Email address of the user'
},
{name: role, 
type: string,
description: 'Role of the user, can be Admin or Employee'
},
"""


CHART_FUNCTION_SIGNATURES = """
st.bar_chart(data=None, *, x=None, y=None, x_label=None, y_label=None, color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)

Parameters
data (Anything supported by st.dataframe)

Data to be plotted.

x (str or None)

Column name or key associated to the x-axis data. If x is None (default), Streamlit uses the data index for the x-axis values.

y (str, Sequence of str, or None)

Column name(s) or key(s) associated to the y-axis data. If this is None (default), Streamlit draws the data of all remaining columns as data series. If this is a Sequence of strings, Streamlit draws several series on the same chart by melting your wide-format table into a long-format table behind the scenes.

x_label (str or None)

The label for the x-axis. If this is None (default), Streamlit will use the column name specified in x if available, or else no label will be displayed.

y_label (str or None)

The label for the y-axis. If this is None (default), Streamlit will use the column name(s) specified in y if available, or else no label will be displayed.

color (str, tuple, Sequence of str, Sequence of tuple, or None)

The color to use for different series in this chart.

For a bar chart with just one series, this can be:

None, to use the default color.
A hex string like "#ffaa00" or "#ffaa0088".
An RGB or RGBA tuple with the red, green, blue, and alpha components specified as ints from 0 to 255 or floats from 0.0 to 1.0.
For a bar chart with multiple series, where the dataframe is in long format (that is, y is None or just one column), this can be:

None, to use the default colors.

The name of a column in the dataset. Data points will be grouped into series of the same color based on the value of this column. In addition, if the values in this column match one of the color formats above (hex string or color tuple), then that color will be used.

For example: if the dataset has 1000 rows, but this column only contains the values "adult", "child", and "baby", then those 1000 datapoints will be grouped into three series whose colors will be automatically selected from the default palette.

But, if for the same 1000-row dataset, this column contained the values "#ffaa00", "#f0f", "#0000ff", then then those 1000 datapoints would still be grouped into 3 series, but their colors would be "#ffaa00", "#f0f", "#0000ff" this time around.

For a bar chart with multiple series, where the dataframe is in wide format (that is, y is a Sequence of columns), this can be:

None, to use the default colors.
A list of string colors or color tuples to be used for each of the series in the chart. This list should have the same length as the number of y values (e.g. color=["#fd0", "#f0f", "#04f"] for three lines).
horizontal (bool)

Whether to make the bars horizontal. If this is False (default), the bars display vertically. If this is True, Streamlit swaps the x-axis and y-axis and the bars display horizontally.

stack (bool, "normalize", "center", "layered", or None)

Whether to stack the bars. If this is None (default), Streamlit uses Vega's default. Other values can be as follows:

True: The bars form a non-overlapping, additive stack within the chart.
False: The bars display side by side.
"layered": The bars overlap each other without stacking.
"normalize": The bars are stacked and the total height is normalized to 100% of the height of the chart.
"center": The bars are stacked and shifted to center the total height around an axis.
width (int or None)

Desired width of the chart expressed in pixels. If width is None (default), Streamlit sets the width of the chart to fit its contents according to the plotting library, up to the width of the parent container. If width is greater than the width of the parent container, Streamlit sets the chart width to match the width of the parent container.

To use width, you must set use_container_width=False.

height (int or None)

Desired height of the chart expressed in pixels. If height is None (default), Streamlit sets the height of the chart to fit its contents according to the plotting library.

use_container_width (bool)

Whether to override width with the width of the parent container. If use_container_width is True (default), Streamlit sets the width of the chart to match the width of the parent container. If use_container_width is False, Streamlit sets the chart's width according to width.


##################################


st.line_chart(data=None, *, x=None, y=None, x_label=None, y_label=None, color=None, width=None, height=None, use_container_width=True)

Parameters
data (Anything supported by st.dataframe)

Data to be plotted.

x (str or None)

Column name or key associated to the x-axis data. If x is None (default), Streamlit uses the data index for the x-axis values.

y (str, Sequence of str, or None)

Column name(s) or key(s) associated to the y-axis data. If this is None (default), Streamlit draws the data of all remaining columns as data series. If this is a Sequence of strings, Streamlit draws several series on the same chart by melting your wide-format table into a long-format table behind the scenes.

x_label (str or None)

The label for the x-axis. If this is None (default), Streamlit will use the column name specified in x if available, or else no label will be displayed.

y_label (str or None)

The label for the y-axis. If this is None (default), Streamlit will use the column name(s) specified in y if available, or else no label will be displayed.

color (str, tuple, Sequence of str, Sequence of tuple, or None)

The color to use for different lines in this chart.

For a line chart with just one line, this can be:

None, to use the default color.
A hex string like "#ffaa00" or "#ffaa0088".
An RGB or RGBA tuple with the red, green, blue, and alpha components specified as ints from 0 to 255 or floats from 0.0 to 1.0.
For a line chart with multiple lines, where the dataframe is in long format (that is, y is None or just one column), this can be:

None, to use the default colors.

The name of a column in the dataset. Data points will be grouped into lines of the same color based on the value of this column. In addition, if the values in this column match one of the color formats above (hex string or color tuple), then that color will be used.

For example: if the dataset has 1000 rows, but this column only contains the values "adult", "child", and "baby", then those 1000 datapoints will be grouped into three lines whose colors will be automatically selected from the default palette.

But, if for the same 1000-row dataset, this column contained the values "#ffaa00", "#f0f", "#0000ff", then then those 1000 datapoints would still be grouped into three lines, but their colors would be "#ffaa00", "#f0f", "#0000ff" this time around.

For a line chart with multiple lines, where the dataframe is in wide format (that is, y is a Sequence of columns), this can be:

None, to use the default colors.
A list of string colors or color tuples to be used for each of the lines in the chart. This list should have the same length as the number of y values (e.g. color=["#fd0", "#f0f", "#04f"] for three lines).
width (int or None)

Desired width of the chart expressed in pixels. If width is None (default), Streamlit sets the width of the chart to fit its contents according to the plotting library, up to the width of the parent container. If width is greater than the width of the parent container, Streamlit sets the chart width to match the width of the parent container.

To use width, you must set use_container_width=False.

height (int or None)

Desired height of the chart expressed in pixels. If height is None (default), Streamlit sets the height of the chart to fit its contents according to the plotting library.

use_container_width (bool)

Whether to override width with the width of the parent container. If use_container_width is True (default), Streamlit sets the width of the chart to match the width of the parent container. If use_container_width is False, Streamlit sets the chart's width according to width.
"""