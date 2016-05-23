function post_location(loc) {
  document.getElementById("latitude").value = loc.coords.latitude;
  document.getElementById("longitude").value = loc.coords.longitude;
  document.getElementById("radius").value = '250';
};

function request_location() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(post_location);
  }
};
