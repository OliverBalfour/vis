import random
import re

def unique_custom_elements(html: str) -> str:
  """HTML custom elements can't be re-registered/redefined so when developing visualisations
  you need to reload the whole VSCode window / Jupyter tab. As a workaround, we inject random
  numbers into the HTML string at the end of every element name"""
  i = random.getrandbits(16)
  # Scan for <custom-elem or </custom-elem or customElements.define('custom-elem with regex
  return _regex.sub(rf'\1-{i}', html)

# Regex for custom element tags and definitions, should hit most cases
# https://html.spec.whatwg.org/multipage/custom-elements.html#valid-custom-element-name
_tag = r'<\s*/?\s*[a-z][a-z0-9\._-]*-[a-z0-9\._-]*'
_reg = r'customElements.define\(["\'][^"\'\n]+'
_regex = re.compile(rf'({_tag}|{_reg})')

def vis(fname: str):
  from IPython.display import HTML
  with open(fname, 'r') as f:
    html = f.read()
  html = unique_custom_elements(html)
  return HTML(html)
