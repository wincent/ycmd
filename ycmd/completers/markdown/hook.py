from ycmd.completers.markdown.markdown_completer import MarkdownCompleter

def GetCompleter( user_options ):
  return MarkdownCompleter( user_options )
