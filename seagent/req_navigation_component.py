import streamlit.components.v1 as components
import os

######### will be relocated ###############
# Declare the component:
# parent_dir = os.path.dirname(os.path.abspath(__file__))
# build_dir = os.path.join(parent_dir, "frontend/build")
# build_dir = "/opt/bihua/reqgpt/seagent/component-template/template/my_component/frontend/build"
# # print(parent_dir)
# _component_func  = components.declare_component(
#     "st_navigation_component", 
#     path=build_dir)

_component_func  = components.declare_component(
    "st_navigation_component", 
    url="http://localhost:3001")

def st_navigation_component(tree_json, key=None):
    """Create a new instance of "st_navigation_component"."""
    return _component_func(tree_json=tree_json, key=key, default=None)