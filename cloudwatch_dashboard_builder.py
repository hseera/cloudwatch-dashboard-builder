'''
The application is build using PySimpleGUI. 
It expects you have setup the aws id/key in
Linux:   /home/[username]/.aws
Windows: /Users/[username]/.aws

'''

import PySimpleGUI as sg
import boto3
from botocore.config import Config
import json
from boto3.session import Session
import threading
# from pathlib import Path
# import pandas as pd
# import datetime



session = boto3.session.Session()


sg.theme('Reddit')
query_list=[]

#The TIP string for the namespace template.
json_template_tip='''TIP:
    
    1: Cloudwatch_template, schema, templates, name, desc & query are keywords for the namespace template.
    2: Make sure double quotes are escaped.
'''


#The TIP string for connecting to AWS account.
connection_tip ='''TIP:
    If you don't want to enter id, key & region, make sure this information is located in the following location:
    Linux:   /home/[username]/.aws
    Windows: /Users/[username]/.aws

'''

#-----------------GUI Layout--------------------------------    
Region = [
    [sg.Text("Region Name (Select Region)")],
    [sg.Listbox(values=[],enable_events=True,size=(24, 8), key="-REGION_LISTBOX-")], 
    [sg.B("List Regions",size=(23, 1))]
    ]


namespaces = [
    [sg.Text("Namespaces")],
    [sg.Listbox(values=[], enable_events=True, size=(30, 10), key="-NAMESPACES_LISTBOX-",right_click_menu=['&Right', ['Refresh Namespaces']])]
    ]


namespace_templates = [
    [sg.Text("Templates")],
    [sg.Listbox(values=[], enable_events=True, size=(32, 10), key="-TEMPLATES_LISTBOX-")]
    ]


template_detail = [
    [sg.Text("Template Detail")],
    [sg.Multiline(size=(50, 4), enable_events=True, key="-TEMPLTDESC_TEXTBOX-", disabled=True)],
    [sg.Multiline(size=(50, 6), enable_events=True, key="-QUERY_TEXTBOX-",right_click_menu=['&Right', ['Add Query']])],
    ]


build_dashboard = [
    [sg.Text("Queries To Add")],
    [sg.Table(values=query_list,headings=["Widget Title","Queries"], auto_size_columns=False, col_widths=[22, 41],enable_events=True, key="-SQL_TABLE-",  num_rows=7,justification='left',right_click_menu=['&Right', ['Remove Query','Generate Dashboard JSON']])],
    [sg.Text("Cloudwatch Dashbaord JSON")],
    [sg.Multiline(size=(80, 10),key="-DASHBOARD_TEXTBOX-")],
    [sg.Text('Dashboard Name:'), sg.Input("",size=(40, 1),key="-DASHBOARD_NAME_INPUT-"),sg.B("Create Dashboard",size=(20, 1))]]

Console = [
    [sg.Text("Existing Dashboards")],
    [sg.Listbox(values=[], enable_events=True, size=(65, 8), key="-DASHBOARD_LISTBOX-",right_click_menu=['&Right', ['Refresh','Show Existing Dashboards']])],
    [sg.Text("Console")],
    [sg.Multiline(size=(65, 12),key="-CONSOLEMSG_TEXTBOX-",disabled=True)],
    [sg.B("Clear Console",size=(26, 1)),sg.B("Save Console",size=(26, 1))]
    ]

dashboard_builder =[[sg.Column(build_dashboard)]]

sql_builder=[
    [sg.Text("Not Yet Implemented")]]

sql_layout = [
    [
        sg.Column(Region),
        sg.VSeperator(),
        sg.Column(namespaces),
        sg.Column(namespace_templates),
        sg.Column(template_detail)
        ],      
     [
      sg.TabGroup(
         [[sg.Tab('Dashboard Builder', dashboard_builder)],
          [sg.Tab('Query Builder', sql_builder)]]),
        sg.VSeperator(),
        sg.Column(Console)]   
]

config =[
    [sg.Text('Enter Your AWS Id',size=(30, 1)), sg.InputText(key="-AWSID_INPUT-",size=(30, 1))],
    [sg.Text('Enter Your AWS Key',size=(30, 1)), sg.InputText(key="-AWSKEY_INPUT-",size=(30, 1))],
    [sg.Text('Enter Your Default Region',size=(30, 1)), sg.InputText(key="-DEFAULT_REGION_INPUT-",size=(30, 1))],
    [sg.B("Reset",size=(28, 1)),sg.B("Connect",size=(27, 1))]
    ]

config_tip =[[sg.Multiline(size=(85, 7),key="-CONNECTTIP_TEXTBOX-",disabled=True)]
    ]
config_layout = [[sg.Column(config),
                  sg.Column(config_tip)]]

json_builder =[
    [sg.Multiline(size=(155, 6),key="-JSONTIP_TEXTBOX-",disabled=True)],
    [sg.Multiline(size=(155, 31),key="-JSONFILE-")],
    [sg.B("Load Template",size=(40, 1)),sg.B("Update Template",size=(40, 1))],
    ]
tabgrp = [[sg.TabGroup([[sg.Tab('Config', config_layout, key='_CONFIG_TAB_')],
                        [sg.Tab('Cloudwatch Dashboard Builder', sql_layout, key='_DASHBOARD_TAB_')],
                        [sg.Tab('Namespace Query Template', json_builder, key='_NAMESPACE_TAB_')]
                        ],key='BUILDER_TABS', enable_events=True
                       )]]  

#--------------AWS Sql specific Functions--------------------------------------

        
#Get list of all the dashboards 
def list_dashboards(REGION_NAME):
    REGION_CONFIG = Config(
    region_name = REGION_NAME,
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
        }
    )
    
    CLIENT = session.client('cloudwatch', config=REGION_CONFIG)  
    response = CLIENT.list_dashboards()
    dashboard_list=[]
    for dashboard in response['DashboardEntries']:
        dashboard_list.append(dashboard['DashboardName'])
    return dashboard_list



#Create Cloudwatch dashboard 
def create_dashboards(REGION_NAME, DASHBOARD_NAME, DASHBOARD_JSON):
    REGION_CONFIG = Config(
    region_name = REGION_NAME,
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
        }
    )
    CLIENT = session.client('cloudwatch', config=REGION_CONFIG)  
    
    response = CLIENT.put_dashboard(
                DashboardName=DASHBOARD_NAME,
                DashboardBody=DASHBOARD_JSON
                )
    return response



# get all the AWS regions
def get_az():
    cloudwatch_region = session.get_available_regions('cloudwatch')
    return (cloudwatch_region)


#----------------Cloudwatch Dashboard Threading functions--------------------------------------

def dashboard_function_worker_thread(region_name, window):
    try:
         resp = list_dashboards(region_name)
         window.write_event_value('-WRITE-',resp)
    except Exception as e:
        window.write_event_value('-WRITE-',e)


def create_dashboard_function_worker_thread(region_name,dashboard_name, dashboard_json, window):
    try:
        response = create_dashboards(region_name,dashboard_name, dashboard_json)
        if 'ResponseMetadata' in response:
            window.write_event_value('-CONSOLEWRITE-','Dashboard %s Successfully created' %(dashboard_name))
        else:
            window.write_event_value('-CONSOLEWRITE-',response)        
    except Exception as e:
        if 'Unable to locate credentials' in str(e):
            window.write_event_value('-CONSOLEWRITE-',"Please make sure you have set AWS credentials")
        else:
            window.write_event_value('-CONSOLEWRITE-',e)




#-----------------Cloudwatch Namespace, template, functions-----------------------------------
def load_json_data():
    with open('./template/namespace_query_templates.json', 'r') as data:
        json_data =data.read()
    return json_data

def get_template(schema_name):
        with open('./template/namespace_query_templates.json', 'r') as data:
            sql_data =json.loads(data.read())
            template_list=[]
            for template in sql_data['cloudwatch_template'][schema_name]:
                for name in template['templates']:
                    template_list.append(name['name'])
        return template_list
    


def get_desc(schema_name, Name):
    with open('./template/namespace_query_templates.json', 'r') as data:
        sql_data =json.loads(data.read())
        template_desc=[]
        for template in sql_data['cloudwatch_template'][schema_name]:
            for name in template['templates']:
                if  name['name'] == Name:
                    template_desc.append([name['desc'],name['query']])
    return template_desc


def load_namespace():
    with open('./template/namespace_query_templates.json', 'r') as data:
        namespace_list=[]
        sql_data =json.loads(data.read())
        for namespace in sql_data['cloudwatch_template']:
            namespace_list.append(namespace)
                    
    return namespace_list
        

def generate_json(region): #generate dsahboard json
    root_start='{"widgets": ['
    root_end=']}'    
    metric_start=""
    x=0 #widget x coordinate
    y=0 #widget y coordinate
    for index, sql_element in enumerate(query_list): 
        if (index != len(query_list)-1):
            if sql_element[1].startswith('SELECT'):
                metric_start=metric_start+'{"height": 10,"width": 10,"y": '+str(y)+',"x":'+str(x)+',"type": "metric","properties": {"view": "timeSeries","stacked": false,"metrics": [[ { "expression": "'+sql_element[1]+'", "label": "Query'+str(index+1)+'", "id": "q'+str(index+1)+'" } ]],"region": "'+region+'","stat": "Average","period": 300,"title": "'+sql_element[0]+'"}},'
            else:
                metric_element=sql_element[1].replace("\\","")
                metric_start=metric_start+'{"height": 10,"width": 10,"y": '+str(y)+',"x":'+str(x)+',"type": "metric","properties": {"view": "timeSeries","stacked": false,"metrics": ['+metric_element+'],"region": "'+region+'","stat": "Average","period": 300,"title": "'+sql_element[0]+'"}},'
        else:
            if sql_element[1].startswith('SELECT'):
                metric_start=metric_start+'{"height": 10,"width": 10,"y": '+str(y)+',"x":'+str(x)+',"type": "metric","properties": {"view": "timeSeries","stacked": false,"metrics": [[ { "expression": "'+sql_element[1]+'", "label": "Query'+str(index+1)+'", "id": "q'+str(index+1)+'" } ]],"region": "'+region+'","stat": "Average","period": 300,"title": "'+sql_element[0]+'"}}'
            else:
                metric_element=sql_element[1].replace("\\","")
                metric_start=metric_start+'{"height": 10,"width": 10,"y": '+str(y)+',"x":'+str(x)+',"type": "metric","properties": {"view": "timeSeries","stacked": false,"metrics": ['+metric_element+'],"region": "'+region+'","stat": "Average","period": 300,"title": "'+sql_element[0]+'"}}'
        
        if ((index+1) % 2 == 0):
            y=y+10
            x=0
        else:
            x=x+10
        
    dashboard = root_start+metric_start+root_end
    
    return(dashboard)
            


#-----------------Main function------------------------------------
def main():
    
    window = sg.Window('AWS Cloudwatch Dashboard Builder', tabgrp)#layout
    global guery_list

    region_loop = False
    while True: # The Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        #---------Connection Tab-----------------------------
        if event == 'Reset':
            try:
                window["-AWSID_INPUT-"].update("")
                window["-AWSKEY_INPUT-"].update("")
                window["-DEFAULT_REGION_INPUT-"].update("")
                window["-AWSID_INPUT-"].SetFocus(force = True)
            except Exception as e:
                sg.popup(e)
        
        if event == 'Connect':
            try:
                global session
                
                if values['-DEFAULT_REGION_INPUT-'] == "":
                    sg.popup("Region Field is missing")
                elif values['-AWSID_INPUT-'] == "":
                    sg.popup("AWS ID Field is missing")
                elif values['-AWSKEY_INPUT-'] == "":
                    sg.popup("AWS KEY Field is missing")
                else:
                    session = Session(region_name=values['-DEFAULT_REGION_INPUT-'], 
                                      aws_access_key_id=values['-AWSID_INPUT-'],
                                      aws_secret_access_key=values['-AWSKEY_INPUT-'])
                    #need to validate if connection is successful or not
                    sg.popup("Connection Established")
            except Exception as e:
                sg.popup(e)
        
        #-------Clicked SQL Dashboard Builder Tab & popluate namespace data---------
        if event == 'BUILDER_TABS':
            activeTab = values['BUILDER_TABS']
            if activeTab == '_DASHBOARD_TAB_':
                try:
                    namespace_list = load_namespace()
                    window["-NAMESPACES_LISTBOX-"].update(namespace_list)
                except Exception as e:
                    window["-CONSOLEMSG_TEXTBOX-"].update("JSON File "+str(e)+"\n", append=True)
            if activeTab == '_NAMESPACE_TAB_':
                try:
                    window["-JSONTIP_TEXTBOX-"].update(json_template_tip)
                except Exception as e:
                    window["-CONSOLEMSG_TEXTBOX-"].update(str(e)+"\n", append=True)
            if activeTab == '_CONFIG_TAB_':
                try:
                    window["-CONNECTTIP_TEXTBOX-"].update(connection_tip)
                except Exception as e:
                    window["-CONSOLEMSG_TEXTBOX-"].update(str(e)+"\n", append=True)
            
            
        #---------Send SQL Message Tab------------------------
        
       
        if event == 'List Regions':
            try:
                if region_loop == False: #don't refresh list everytime
                    region_list = get_az()
                    window["-REGION_LISTBOX-"].update(region_list)
                    region_loop = True
            except Exception as e:
                window["-CONSOLEMSG_TEXTBOX-"].update(str(e)+"\n", append=True )
                
        
        if event =='Show Existing Dashboards':
            try:
                if not values['-REGION_LISTBOX-']:
                    window["-CONSOLEMSG_TEXTBOX-"].update("Please select a region\n", append=True)
                    
                else:
                    threading.Thread(target=dashboard_function_worker_thread,
                                      args=(values['-REGION_LISTBOX-'][0],
                                            window,),  daemon=True).start()
            except Exception as e:
                if 'NoCredentialsError' in str(e):
                    window["-CONSOLEMSG_TEXTBOX-"].update("Please make sure you have set AWS credentials\n", append=True)
                else:
                    window["-CONSOLEMSG_TEXTBOX-"].update(str(e)+"\n", append=True)
            
        
        # if event == '-REGION_LISTBOX-':
        #     try:
        #             threading.Thread(target=dashboard_function_worker_thread,
        #                               args=(values['-REGION_LISTBOX-'][0],
        #                                     window,),  daemon=True).start()
        #     except Exception as e:
        #         window["-CONSOLEMSG_TEXTBOX-"].update(str(e)+"\n", append=True)
        
        if event == '-NAMESPACES_LISTBOX-': #populate sql templates for selected namespace
            try:
                window["-TEMPLATES_LISTBOX-"].update("")
                window["-TEMPLTDESC_TEXTBOX-"].update("")
                window["-QUERY_TEXTBOX-"].update("")
                template_list = get_template(values["-NAMESPACES_LISTBOX-"][0])
                window["-TEMPLATES_LISTBOX-"].update(template_list)
            except Exception as e:
                window["-CONSOLEMSG_TEXTBOX-"].update(str(e)+"\n", append=True)
        
        if event == '-TEMPLATES_LISTBOX-':  #populate description & sql for selected sql template
            try: 
                window["-TEMPLTDESC_TEXTBOX-"].update("")
                window["-QUERY_TEXTBOX-"].update("")
                desc_list = get_desc(values["-NAMESPACES_LISTBOX-"][0],values["-TEMPLATES_LISTBOX-"][0])
                window["-TEMPLTDESC_TEXTBOX-"].update(desc_list[0][0])
                window["-QUERY_TEXTBOX-"].update(desc_list[0][1].replace("\"","\\\""))
            except Exception:
                window["-CONSOLEMSG_TEXTBOX-"].update("Please select a namespace\n", append=True)
        
         
        if event == 'Add Query': #add sql query to query list for which dashboard needs to be generated
            if values["-QUERY_TEXTBOX-"]=="":
                sg.popup("No SQL to Add or not selected",title="Add Query")
            else:
                query_list.append([values["-TEMPLATES_LISTBOX-"][0],values["-QUERY_TEXTBOX-"]])
                window["-SQL_TABLE-"].update(query_list)
            
        if event == 'Remove Query': #remove sql query from query list if don't need for the dashboard
            if (len(query_list)==0 or values["-SQL_TABLE-"]==[]):
                sg.popup("No SQL query to remove or not selected",title="Remove Query")
            else:
                query_list.pop(values["-SQL_TABLE-"][0])
                window["-SQL_TABLE-"].update(query_list)
        
        if event == 'Generate Dashboard JSON': #generate Cloudwatch dashboard JSON
            if (len(query_list)==0 or values["-REGION_LISTBOX-"]==[]):
                sg.popup("Nothing to generate or Region not selected",title="Generate Dashboard")
            else:
                json_result=generate_json(values["-REGION_LISTBOX-"][0])
                window["-DASHBOARD_TEXTBOX-"].update(json.dumps(json.loads(json_result),indent=4))
        
        if event == 'Refresh Namespaces': #refresh namespace list if json file is updated. Reset all other fields too.
            namespace_list = load_namespace()
            window["-NAMESPACES_LISTBOX-"].update(namespace_list)
            window["-TEMPLATES_LISTBOX-"].update("")
            window["-TEMPLTDESC_TEXTBOX-"].update("")
            window["-QUERY_TEXTBOX-"].update("")
            query_list.clear()
            window["-SQL_TABLE-"].update(query_list)
            
        
        if event == 'Create Dashboard': #make AWS API call to create Cloudwatch dashboard
            try:
                if (values['-DASHBOARD_NAME_INPUT-']=='' or values["-REGION_LISTBOX-"]==[] or window["-JSONFILE-"]==[]):
                    window["-CONSOLEMSG_TEXTBOX-"].update("Missing Region or Payload or dashboard name\n", append=True)
                else:
                    threading.Thread(target=create_dashboard_function_worker_thread,
                                      args=(values['-REGION_LISTBOX-'][0],values['-DASHBOARD_NAME_INPUT-'],
                                            json_result, window,),  daemon=True).start()
            except Exception as e:
                if 'NoCredentialsError' in str(e):
                    window["-CONSOLEMSG_TEXTBOX-"].update("Please make sure you have set AWS credentials\n", append=True)
                else:
                    window["-CONSOLEMSG_TEXTBOX-"].update(str(e)+"\n", append=True)
                
        if event == 'Refresh': 
            try:
                    threading.Thread(target=dashboard_function_worker_thread,
                                      args=(values['-REGION_LISTBOX-'][0],
                                            window,),  daemon=True).start()
            except Exception as e:
                window["-CONSOLEMSG_TEXTBOX-"].update(str(e)+"\n", append=True)
        

#---------------JSON file events---------------------------------------
        
        if event == 'Load Template': 
            try:
                json_result=load_json_data()
                window["-JSONFILE-"].update(json.dumps(json.loads(json_result),indent=4))
                
            except Exception as e:
                window["-CONSOLEMSG_TEXTBOX-"].update(str(e)+"\n", append=True)
                
        if event == 'Update Template':
            try:
                with open('./template/namespace_query_templates.json', 'w') as data:
                    data.write(values["-JSONFILE-"])
                sg.popup("JSON File Successfully Saved")
            except Exception as e:
                window["-CONSOLEMSG_TEXTBOX-"].update(str(e)+"\n", append=True)

#---------------Console events---------------------------------------
        if event == '-WRITE-':
            try:
                window["-DASHBOARD_LISTBOX-"].update(values['-WRITE-'])
            except Exception as e:
                if 'NoCredentialsError' in str(e):
                    window["-CONSOLEMSG_TEXTBOX-"].update("Please make sure you have set AWS credentials\n", append=True)
                else: 
                    window["-CONSOLEMSG_TEXTBOX-"].update(str(e)+"\n", append=True)
        
        if event == '-CONSOLEWRITE-':
            try:
                window["-CONSOLEMSG_TEXTBOX-"].update(values['-CONSOLEWRITE-']+"\n", append=True)
            except Exception as e:
                window["-CONSOLEMSG_TEXTBOX-"].update(str(e)+"\n", append=True)


        if event == 'Save Console':
            try:
                file= open("output.txt", 'a+')
            except FileNotFoundError:
                file= open("output.txt", 'w+')
            file.write(str(window["-CONSOLEMSG_TEXTBOX-"].get()))
            file.close()
            sg.popup("File Saved")
        
        
        if event == 'Clear Console':
            window["-CONSOLEMSG_TEXTBOX-"].update("")
    window.close()


if __name__ == '__main__':
    main()