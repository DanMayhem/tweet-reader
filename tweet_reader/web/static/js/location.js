function post_location(loc) {

}

function request_location() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(post_location)
  }
}
