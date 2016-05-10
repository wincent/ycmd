from ycmd.completers.completer import Completer
from ycmd import extra_conf_store, responses

import redis

class MarkdownCompleter( Completer ):
    def __init__( self, user_options ):
        super( MarkdownCompleter, self ).__init__( user_options )
        self._prefix = None
        self._cache_breaker = None
        self._candidates = None
        self._filtered_candidates = None
        self._redis = redis.StrictRedis()

    def SupportedFiletypes( self ):
        return [ 'markdown' ]

    def ComputeCandidatesInner( self, request_data ):
        return self.FilterAndSortCandidates(
                self._candidates,
                request_data[ 'query' ] )

    def OnBufferVisit( self, request_data ):
        # Hack alert: passing options through the .ycm_extra_conf.py file.
        self._candidates = []
        module = None
        try:
            module = extra_conf_store.ModuleForSourceFile( request_data [ 'filepath' ] )
            if module:
                if hasattr(module, 'markdown_prefix') and module.markdown_prefix:
                    self._prefix = module.markdown_prefix
                else:
                    return
                if hasattr(module, 'markdown_cache_breaker') and module.markdown_cache_breaker:
                    self._cache_breaker = module.markdown_cache_breaker
                else:
                    return
            else:
                return
        except:
            return

        # TODO: show target article in preview window?
        wiki_candidates = [ ( kind, name )
                for kind in [ 'wiki' ]
                for name in self._redis.zrevrange( self._prefix + ':' + self._cache_breaker + ':wiki-index', 0, 10000 ) ]
        blog_candidates = [ ( kind, name )
                for kind in [ 'blog' ]
                for name in self._redis.zrevrange( self._prefix + ':' + self._cache_breaker + ':blog-index', 0, 10000 ) ]
        raw_candidates = wiki_candidates + blog_candidates

        self._candidates = [
                responses.BuildCompletionData(
                    str( '/' + kind + '/' + ( name if kind == 'blog' else name.replace(' ', '_') ) .encode( 'utf-8' ) ),
                    str( kind ),
                    None,
                    str( name.encode( 'utf-8' ) ) )
                for ( kind, name ) in raw_candidates ]
