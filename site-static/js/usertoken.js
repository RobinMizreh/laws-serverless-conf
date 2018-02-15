var data = {
  UserPoolId: _config.cognito.userPoolId,
  ClientId: _config.cognito.userPoolClientId
};

var userPool = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserPool(data);
var cognitoUser = userPool.getCurrentUser();
var email = '';

$(document).ready(function() {
  if(cognitoUser != null) {
    cognitoUser.getSession(function(err, session) {
      if (err) {
        swal('Oops', err.message, 'error');
        return;
      }
      window._session = session;
      cognitoUser.getUserAttributes(function(err, result) {
        if (err) {
            swal('Oops', err.message, 'error');
            return;
        }
        else {
          if (_session.isValid()) {
            for (i = 0; i < result.length; i++) {
              if (result[i].getName() == "email") {
                email = result[i].getValue();
                showActiveTabsWhenConnected();
              }
            }
          }
        }
      });
    });
  }
  else {
    showActiveTabsWhenDisconnected();
  }
});

function logout() {
  if (cognitoUser != null) {
    cognitoUser.signOut();
  }
  window.location = 'index.html';
};

function showActiveTabsWhenConnected() {
  $('.connected').removeClass('disabled');
  $('.disconnected').addClass('disabled');
  $('.disconnected > a').attr("href", "#");
  $('.disconnected > a').removeAttr("data-toggle");
}

function showActiveTabsWhenDisconnected() {
  $('.connected').addClass('disabled');
  $('.disconnected').removeClass('disabled');
  $('.connected > a').attr("href", "#");
  $('.connected > a').removeAttr("data-toggle");
  $('.connected > a').attr("onclick", "");
}
