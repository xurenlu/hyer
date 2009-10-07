HYER_events={}
HYER_tools={}
import copy
def add_event(event_name,event):
    '''add event for event_name'''
    global HYER_events
    if HYER_events.has_key(event_name):
        HYER_events[event_name].append(event)
    else:
        HYER_events[event_name]=[]
        HYER_events[event_name].append(event)
def add_tool(tool_name,tool):
    '''add tool for tool_name '''
    global HYER_tools
    if HYER_tools.has_key(tool_name):
        HYER_tools[tool_name]=tool
    else:
        HYER_tools[tool_name]=[]
        HYER_tools[tool_name].append(tool)
        
def fire_event(event_name,arguments):
    '''fire an event'''
    global HYER_events
    new_arg=copy.copy(arguments)
    if HYER_events.has_key(event_name):
        for e in HYER_events[event_name]:
            e(new_arg) 
def apply_tool(tool_name,data):
    '''tool data'''
    global HYER_tools
    if HYER_tools.has_key(tool_name):
        for f in HYER_tools[tool_name]:
            f(data)
  
