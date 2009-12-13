#coding:utf-8
HYER_events={}
HYER_filters={}
import copy
"""
event 和Filter的区别是,
event 是不改变原有值的,
而Filter的目的就是改变原有值;
"""
def add_event(event_name,event):
    '''add event for event_name'''
    global HYER_events
    if HYER_events.has_key(event_name):
        HYER_events[event_name].append(event)
    else:
        HYER_events[event_name]=[]
        HYER_events[event_name].append(event)
def add_filter(filter_name,filter):
    '''add filter for filter_name '''
    global HYER_filters
    if HYER_filters.has_key(filter_name):
        HYER_filters[filter_name]=filter
    else:
        HYER_filters[filter_name]=[]
        HYER_filters[filter_name].append(filter)
        
def fire_event(event_name,arguments):
    '''fire an event'''
    global HYER_events
    new_arg=copy.copy(arguments)
    if HYER_events.has_key(event_name):
        for e in HYER_events[event_name]:
            e(new_arg) 
def apply_filter(filter_name,data):
    '''filter data'''
    global HYER_filters
    if HYER_filters.has_key(filter_name):
        for f in HYER_filters[filter_name]:
            data=f(data)
    return data
