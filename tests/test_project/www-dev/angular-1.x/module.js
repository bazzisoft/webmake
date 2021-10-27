angular.module("WebmakeTest", [])
  .factory("TestFactory", function () {
    this.foo = function () {
      alert("foo")
    }
  })
  .controller("TestController", function (TestFactory) {
    TestFactory.foo()
  });