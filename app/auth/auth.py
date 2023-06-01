import oauth2
import oauth2.grant
import oauth2.error
import oauth2.store.memory
import oauth2.tokengenerator
import oauth2.web.wsgi


class ExampleSiteAdapter(oauth2.web.AuthorizationCodeGrantSiteAdapter, oauth2.web.ImplicitGrantSiteAdapter):
    TEMPLATE = '''
        <html>
            <body>
                <p>
                    <a href="{url}&confirm=confirm">confirm</a>
                </p>
                <p>
                    <a href="{url}&deny=deny">deny</a>
                </p>
            </body>
        </html>
    '''

    def authenticate(self, request, environ, scopes, client):
        if request.post_param("confirm") == "confirm":
            return {}

        raise oauth2.error.UserNotAuthenticated

    def render_auth_page(self, request, response, environ, scopes,
                         client):
        url = request.path + "?" + request.query_string
        response.body = self.TEMPLATE.format(url=url)
        return response

    def user_has_denied_access(self, request):

        if request.post_param("deny") == "deny":
            return True
        return False

        client_store = oauth2.store.memory.ClientStore()

        client_store.add_client(client_id="abc", client_secret="xyz", redirect_uris=["http://localhost/callback"])

        site_adapter = ExampleSiteAdapter()

        token_store = oauth2.store.memory.TokenStore()

        provider = oauth2.Provider(
            access_token_store=token_store,
            auth_code_store=token_store,
            client_store=client_store,
            token_generator=oauth2.tokengenerator.Uuid4()
        )

        provider.add_grant(oauth2.grant.AuthorizationCodeGrant(site_adapter=site_adapter))
        provider.add_grant(oauth2.grant.ImplicitGrant(site_adapter=site_adapter))

        provider.add_grant(oauth2.grant.RefreshToken(expires_in=2592000))

        app = oauth2.web.wsgi.Application(provider=provider)

