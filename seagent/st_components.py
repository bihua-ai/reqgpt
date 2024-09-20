import streamlit.components.v1 as components
import seagent_file, re, json
import streamlit as st

_component_func  = components.declare_component(
    "st_action_component", 
    url="http://localhost:3002")

def st_action_component(action_identifier, variable_list_json, spec_json):
    """Create a new instance of "st_action_component"."""
    return _component_func(action_identifier=action_identifier, variable_list_json=variable_list_json, spec_json=spec_json)

_component_func  = components.declare_component(
    "st_attributes_component", 
    url="http://localhost:3003")

def st_attributes_component(variable_identifier, spec_json):
    """Create a new instance of "st_action_component"."""
    return _component_func(variable_identifier=variable_identifier, spec_json=spec_json)

_component_func  = components.declare_component(
    "st_navigation_component", 
    url="http://localhost:3001")

def st_navigation_component(tree_json):
    """Create a new instance of "my_component"."""
    return _component_func(tree_json=tree_json)

_component_func  = components.declare_component(
    "st_states_component", 
    url="http://localhost:3004")

def st_states_component(variable_identifier, spec_json, key=None, default=None):
    """Create a new instance of "st_states_component"."""
    return _component_func(variable_identifier=variable_identifier, spec_json=spec_json)

