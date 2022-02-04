# Code Structure
```
- app.py
- index.py
- apps
   |-- __init__.py
   |-- dashboard.py
   |-- dashboard2.py
```
##### This is how the structure of the multi-page app was defined.

# Implementation of the Code
```
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/apps/dashboard':
        return dashboard.next_page
    else:
        return index_page
```
##### Callback was used to determine whether to stay on the index page or proceed to the ROI dashboard page based on if the login button is clicked. This code was ran on index.py, which then uses different callbacks to interact with dashboard.py.

# Heroku App Deployment
##### The link to the deployed Heroku app can be seen here: https://dash-lenard.herokuapp.com/

##### Authors of the application: JZ Abella, Lenard Cheng
