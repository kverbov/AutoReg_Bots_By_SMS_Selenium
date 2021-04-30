var config = {

    mode: "fixed_servers",

    rules: {

      singleProxy: {

        scheme: "http",

        host: "82.146.43.18",
        port: parseInt(443)

      },

      bypassList: ["foobar.com"]

    }

  };



chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});



function callbackFn(details) {

    return {

        authCredentials: {

            username: "NRi5fylnN",

            password: "[MASKED]"

        }

    };

}



chrome.webRequest.onAuthRequired.addListener(

        callbackFn,

        {urls: ["<all_urls>"]},

        ['blocking']

);
