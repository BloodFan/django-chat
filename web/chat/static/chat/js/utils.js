$(function () {

});

function debounce(func, delay) {
  var timer = 0;
  return function debouncedFn() {
    if (Date.now() - timer > delay) {
      func();
    }
    timer = Date.now();
  };
}
