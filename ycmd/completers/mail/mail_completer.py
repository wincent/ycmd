import subprocess
import string

from ycmd.completers.completer import Completer
from ycmd import responses
from ycmd import utils

class MailCompleter( Completer ):
    def __init__( self, user_options ):
        super( MailCompleter, self ).__init__( user_options )
        self._wrapper = self.FindReattachToUserNamespaceBinary()
        self._binary = self.FindLbdbqBinary()
        self._candidates = None

    def FindLbdbqBinary( self ):
        return utils.PathToFirstExistingExecutable( [ 'lbdbq' ] )

    def FindReattachToUserNamespaceBinary( self ):
        return utils.PathToFirstExistingExecutable(
                [ 'reattach-to-user-namespace' ] )

    def Lbdbq( self, query ):
        if not self._binary:
            return None
        if self._wrapper:
            command = [ self._wrapper, self._binary, query ]
        else:
            command = [ self._binary, query ]
        proc = utils.SafePopen( command, stdout = subprocess.PIPE )
        out, err = proc.communicate()
        if not proc.returncode:
            lines = string.split( out, '\n' )
            if len( lines ) > 1:
                lines.pop( 0 )
                return lines
        return None

    def SupportedFiletypes( self ):
        return [ 'mail' ]

    def ComputeCandidatesInner( self, request_data ):
        return self.FilterAndSortCandidates(
                self._candidates,
                request_data[ 'query' ] )

    def OnBufferVisit( self, request_data ):
        self._candidates = []
        data = self.Lbdbq( '.' )
        raw_candidates = []
        if data:
            for line in data:
                try:
                    address, name, source = string.split(
                            line.encode( 'utf-8'),
                            '\t' )
                    if name:
                        address = name + ' <' + address + '>'
                    raw_candidates.append( ( address, source ) )
                except:
                    pass

        self._candidates = [
                responses.BuildCompletionData(
                    address.encode( 'utf-8' ),
                    source,
                    None,
                    address.encode( 'utf-8' ) )
                for ( address, source ) in raw_candidates ]
