import random
import re
import json

def unique_custom_elements(html: str) -> str:
  """HTML custom elements can't be re-registered/redefined so when developing visualisations
  you need to reload the whole VSCode window / Jupyter tab. As a workaround, we inject random
  numbers into the HTML string at the end of every element name"""
  i = random.getrandbits(24)
  # Scan for <custom-elem or </custom-elem or customElements.define('custom-elem with regex
  return _regex.sub(rf'\1-{i}', html)

# Regex for custom element tags and definitions, should hit most cases
# https://html.spec.whatwg.org/multipage/custom-elements.html#valid-custom-element-name
_tag = r'<\s*/?\s*[a-z][a-z0-9\._-]*-[a-z0-9\._-]*'
_reg = r'customElements.define\(["\'][^"\'\n]+'
_regex = re.compile(rf'({_tag}|{_reg})')

def script_for_variables(**kwargs):
  "Creates a <script> tag containing all the kwargs as JS global variables"

  # convert Python objects into things that can be serialized to JS objects
  # string matching the type is hacky (subclasses won't work) but it avoids
  # conditionally importing lots of tensor libraries
  def proc(obj):
    ty = str(type(obj))
    if 'ndarray' in ty: return obj.tolist()
    elif 'torch.Tensor' in ty or 'torch.nn.Parameter' in ty: return obj.tolist()
    else: return obj
  serializable = { name: proc(kwargs[name]) for name in kwargs }

  # concatenate and return
  script = "<script>\nconsole.clear()\nwindow.latest_parameters = {\n"
  for var_name in serializable:
    script += f"  {var_name}: {json.dumps(serializable[var_name])},\n"
  script += "}\n</script>\n"
  return script

def vis(fname: str, **js_global_variable_kwargs):
  "This returns the visualisation object which can be displayed by IPython"
  from IPython.display import HTML
  html = script_for_variables(**js_global_variable_kwargs)
  with open(fname, 'r') as f:
    html += f.read()
  html = unique_custom_elements(html)
  return HTML(html)
