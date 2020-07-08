export const oidcSettings = {
  authority: process.env.VUE_APP_OIDC_AUTHORITY,
  client_id: process.env.VUE_APP_OIDC_CLIENTID,
  redirect_uri: window.location.origin + '/oidc-callback',
  silent_redirect_uri: window.location.origin + '/oidc-silent-renew',
  automaticSilentRenew: true,
  response_type: 'code',
  scope: 'openid profile email'
}
