---
title: "I/O Overrides"
permalink: /docs/io/
toc: true
---

# I/O Overrides
`input()` and `print()` are overridden to add "magic" features.

## `print()`

* `print()` does not have any new parameters.
* String inputs are evaluated into HTML using `markdownify`, meaning you can insert arbitrary HTML simply by printing the snippet, e.g.: `print("# Title") -> <p><h1>Title</h1></p>`.
* Each `print()` statement wraps it's contents in `<p>...</p>` tags. If inlining elements, etc., print these tags together, e.g.: `print("# Title", "<span> Inline subtitle</span>") -> <p><h1>Title</h1><span> Inline subtitle</span></p>`.
* Since strings are evaluated as raw HTML, this also allows use of `<img>`, `<style>` and `<script>` tags for more advanced app control (beware allowing unfiltered user input!).

### Examples
```python
# display some text wrapped in `small` HTML tags
print("<small>This is some subtext, it's not important.</small>")
```

```html
<small>This is some subtext, it's not important.</small>
```

```python
# inject a `style` tag into the page.
print("<style>#logo{height: 32px; width: 32px}</style>")
```

```html
<style>#logo{height: 32px; width: 32px}</style>
```

```python
# display an image from an external src
# control it's appearence (size, etc.) using the `logo` CSS id
print("<img id='logo' src='https://cdn2.iconfinder.com/data/icons/activity-5/50/1F3A8-artist-palette-1024.png'>")
```

```html
<img id='logo' src='https://cdn2.iconfinder.com/data/icons/activity-5/50/1F3A8-artist-palette-1024.png'>
```

## `input()`

* `input()` has several new (_optional_) parameters for controlling what type of input is displayed.
* By default, a textbox is used.
* By setting `type`, the `<input>` tag can be customised (see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Input#input_types for a comprehensive list of supported types).
* By setting `options` (expecting a `list`) the `prompt` is used as a `<label>` and multiple `<input>`s of `type` (recommended types are `button`, `radio`) are created. Return value is whichever item from `option` list is selected. 
* By setting `attrs`, you can set additional attributes, such as `class` and `id`. Pass a dictionary in the format `{attribute: value}`, e.g.: `{'id': "myelement", 'class': "myclass"}`.

### Custom attribute examples
```python
# return a number between 1-100
input("Pick a number between 1-100", type='range', attrs={'min': 0, 'max': 100})
```

```html
<label>Pick a number between 1-100</label>
<input type='range' min=0 max=100>
```

```python
# return a phone number, with client side validation for a correct pattern
input("Enter your telephone number", type='tel', attrs={'pattern': "[0-9]{3}-[0-9]{2}-[0-9]{3}"})
```

```html
<label>Enter your telephone number</label>
<input type='tel' pattern=[0-9]{3}-[0-9]{2}-[0-9]{3}>
```

## Custom option examples
For input types such as `button`, `radio` and `checkbox`, multiple inputs can be rendered at once. This is an optional argument for all inputs, but will only have an effect for these listed input types.

`button` and `radio` inputs can return a single option, or `None`, e.g.:
```python
# display 2 buttons
# return the selected option (or None if `submit` button pressed instead)
input("Do you like watermelon?", type='button', options=['yes', 'no'])
```

```html
<label>Do you like watermelon?</label>
<input type='submit' value='yes'> <input type='button' value='no'>
```

`checkbox` inputs can return any combination of options, or `None`, e.g.:
```python
# display 2 checkbox options
# if more than 1 item selected, return selected items as a list (or None if `submit` button pressed instead)
input("Which Sci-fi series do you like?", type='checkbox', options=['star wars', 'star trek'])
```

```html
<label>Which Sci-fi series do you like?</label>
<input type='checkbox' value='star wars'> <input type='checkbox' value='star trek'>
```

If an input is required (e.g.: `None` is not acceptable), set the `required` attribute, which will prevent form submission until an option is selected. E.g.:
```python
# display radio options (only 1 can be selected)
# return the selected option (`required` is set, so an option must be selected)
# if `submit` is pressed, the form will prompt the user to make a selection before being allowed to submit
input("What's your thoughts on Marmite?", type='radio', options=['love it', 'hate it'], attrs={'required': True})
```

```html
<label>What's your thoughts on Marmite?</label>
<input type='radio' value='love it' required> <input type='radio' value='hate it' required>
```
