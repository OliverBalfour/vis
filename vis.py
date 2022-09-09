import random
import re

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

def vis(fname: str):
  "This returns the visualisation object which can be displayed by IPython"
  from IPython.display import HTML
  with open(fname, 'r') as f:
    html = f.read()
  html = unique_custom_elements(html)
  return HTML(html)


"""
Other desiderata for injection:
* A thing that renders error messages if something fails instead of showing nothing
* A thing that injects relative imports, unless we can get imports to just work
   Relative imports with `import ... from './file.js'` seem to work, but do
   they get updated how you'd expect, or interfere with previous widgets? If so,
   injecting strings is the way to go (for relative imports ONLY)
* console.clear at the start of each new widget?
"""
