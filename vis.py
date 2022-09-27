import random
import re
import json
from IPython.display import display, HTML

def make_names_unique(html: str) -> str:
  """HTML custom elements can't be re-registered/redefined so when developing visualisations
  you need to reload the whole VSCode window / Jupyter tab. As a workaround, we inject random
  numbers into the HTML string at the end of every element name.
  We also make the latest parameter mounting point unique."""
  i = random.getrandbits(24)
  # Scan for <custom-elem or </custom-elem or customElements.define('custom-elem with regex
  return _regex.sub(rf'\1_{i}', html)

# Regex for custom element tags and definitions, should hit most cases
# https://html.spec.whatwg.org/multipage/custom-elements.html#valid-custom-element-name
_custom_element_tag = r'<\s*/?\s*[a-z][a-z0-9\._-]*-[a-z0-9\._-]*'
_custom_element_def = r'customElements.define\(["\'][^"\'\n]+'
_latest_parameters = r'window\.latest_parameters'
_regex = re.compile(rf'({_custom_element_tag}|{_custom_element_def}|{_latest_parameters})')

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

class WrappedHTML(HTML):
  def browser(self):
    import webbrowser as wb
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
      f.write(self.data)
      wb.open('file://' + f.name, new=2)

def vis(fname: str, **js_global_variable_kwargs):
  "This returns the visualisation object which can be displayed by IPython"
  html = script_for_variables(**js_global_variable_kwargs)
  with open(fname, 'r') as f:
    html += f.read()
  html = make_names_unique(html)
  return WrappedHTML(html)
