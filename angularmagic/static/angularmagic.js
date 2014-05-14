var module = angular.module('django.angularmagic', []);


module.factory('contextStorage', function() {
  var storage = {
    _storage: null,
    set: function(dataString) {
      this._storage = JSON.parse(dataString, function(attr, obj) {
        if (obj) {
          var type = obj['py/object'], value = obj.value;

          switch (type) {
            case 'datetime.time': {
              var parts = [];
              angular.forEach(value.split(':'), function(part){
                parts.push(parseInt(part));
              });
              return new Date(0, 0, 0, parts[0], parts[1], parts[2]);
            }
            case 'datetime.date':
            case 'datetime.datetime': 
            case 'datetime.timedelta': {
              return new Date(Date.parse(value));
            }
          }
        };
        return obj;
      });
    },
    get: function() {return this._storage}
  }
  return storage;
})
.directive('djangoContextItem', function(contextStorage) {
  return {
    restrict: 'E',        
    link: function(scope, element, attrs) {
      contextStorage.set(element.text());
      element.empty();

      if (attrs.debug) {
        console.log('Recieved Django context ' +
                    '(' + attrs.bytes + ' bytes):\n',
                    contextStorage.get());
      }
    }
  };
})
.directive('bindDjangoContext', function(contextStorage) {
  return {
    restrict: 'A',
    // ngController has priority = 500
    priority: 500 + 1,
    controller: function($scope, $element) {
      angular.extend($scope, contextStorage.get());
    },        
  }
});
