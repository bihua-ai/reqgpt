import streamlit.components.v1 as components
import os

# IF True， use component buit; False, we run npm start, so we can modify code easily
_RELEASE = True # or False. Change this line manually
# _RELEASE = False # or False. Change this line manually


if not _RELEASE:
    _component_func  = components.declare_component(
        "st_navigation_component", 
        url="http://localhost:3001")

else:
    # __file__ is /opt/bihua/reqgpt/seagent/
    # folder destination is /opt/bihua/reqgpt/seagent/component-template/template/st_navigation_component/frontend
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "component-template/template/st_navigation_component/frontend/build")
    _component_func = components.declare_component("st_navigation_component", path=build_dir)



def st_navigation_component(tree_json, key=None):
    """Create a new instance of "st_navigation_component"."""
    return _component_func(tree_json=tree_json, key=key, default=None)