from ycmd.completers.mail.mail_completer import MailCompleter

def GetCompleter( user_options ):
  return MailCompleter( user_options )
