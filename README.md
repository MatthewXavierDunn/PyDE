# PyDE

A simple, modular IDE built in Python.

## Customisation

### 📦 Writing a package

You may wish to add your own flair to the IDE. Good for you, there are some basic styling options to play around with.

#### 🎨 Application Styling

Formatting of package files is trivial. Take a look at the default `styling.json` file:
```json
{
    "tab-bg": "#1f2228",
    "tab-gutter": "#16181d",
    "tab-active-bg": "#282c34",
    "tab-active-fg": "#abb2bf",
    "tab-hover-bg": "#282c34",
    "tab-font": ["Segoe UI", 10],
    "bg": "#282c34",
    "fg": "#abb2bf",
    "linenum-fg": "#505662",
    "active-linenum-fg": "#717580",
    "insert-bg": "#528bff",
    "insert-fg": "#abb2bf",
    "insert-w": 2,
    "select-bg": "#3e4451",
    "font": ["Fira Code", 14],
    "relief": "flat",
    "wrap": "none"
}
```
All options are configurable accordingly:

|Option|Values|Default|
|--|--|--|
|`tab-bg`|`#COLOUR`|`#1f2228`|
|`tab-gutter`|`#COLOUR`|`#16181d`|
|`tab-active-bg`|`#COLOUR`|`#282c34`|
|`tab-active-fg`|`#COLOUR`|`#abb2bf`|
|`tab-hover-bg`|`#COLOUR`|`#282c34`|
|`tab-font`|`["FONT", INT]`|`["Segoe UI", 10]`|
|`bg`|`#COLOUR`|`#282c34`|
|`fg`|`#COLOUR`|`#abb2bf`|
|`linenum-fg`|`#COLOUR`|`#505662`|
|`active-linenum-fg`|`#COLOUR`|`#717580`|
|`insert-bg`|`#COLOUR`|`#528bff`|
|`insert-fg`|`#COLOUR`|`#abb2bf`|
|`insert-w`|`INT`|`2`|
|`select-bg`|`#COLOUR`|`#3e4451`|
|`font`|`["FONT", INT]`|`["Fira Code", 14]`|
|`relief`|`flat | sunken | ridge`|`flat`|
|`wrap`|`none | word`|`none`|

`#COLOUR` - any valid hexadecimal or colour name.

#### 💻 Custom Syntax Highlighting

Less trivial is the customisation of syntax highlighting. However, it is highly configurable and you may wish to write your own custom syntax rule sets. Styling is as follows:

```json
{
  "tags": {
    "custom-tag-name": {
      "colour": "#COLOUR",
      "regex": "ANY VALID REGULAR EXPRESSION"
    }
  }
}
```

**Notes**

1. the highlighter will only highlight characters consumed by the regular expression. Use lookaheads/lookbehinds to prevent unwanted highlighting e.g.
`(?<=class )\w+`
will match any text proceeding the literal `class` but will not highlight `class` itself

2. Any escaped characters must be preceeded by an additional `\` e.g.
`\\w` in place of `\w`
