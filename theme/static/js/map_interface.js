mapboxgl.accessToken =
  "pk.eyJ1IjoiaGVwcGxlcmoiLCJhIjoiY2xwc3cyN3UyMDdlOTJqbTgwcmZjeWJuYSJ9.wmrR3E8vqsQb3Ml7v0HX-A";
const map = new mapboxgl.Map({
  container: "map",
  style: "mapbox://styles/mapbox/streets-v10",
  zoom: 9,
});

// turn off mouse zoom
map.scrollZoom.disable();
// turn on controls
map.addControl(new mapboxgl.NavigationControl());

let arnhem = [5.89873, 51.985103];
map.flyTo({
  center: arnhem,
  zoom: 9,
});

const loadingMessage = document.getElementById("loading");
loadingMessage.innerHTML = "Please wait, the map is loading data...";

function showLoading(dataType) {
  const loadingMessage = document.getElementById("loading");
  loadingMessage.innerHTML = `Loading ${dataType}...`;
  loadingMessage.style.display = "block";
}

function hideLoading() {
  const loadingMessage = document.getElementById("loading");
  loadingMessage.style.display = "none";
}

// fetch our people data
fetch("/api/people/")
  .then((response) => response.json())
  .then((data) => {
    console.log("people", data);
    const features = data.map(function (person) {
      return {
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [person.longitude, person.latitude],
        },
        properties: {
          name: person.first_name + " " + person.last_name,
          point_type: "person",
        },
      };
    });

    const geojson = {
      type: "FeatureCollection",
      features: features,
    };

    map.addLayer({
      id: "circles",
      type: "circle",
      source: {
        type: "geojson",
        data: geojson,
      },
      paint: {
        "circle-radius": 5,
        "circle-color": "blue",
        "circle-opacity": 0.75,
      },
    });

    // when a user clicks on a Person circle on the map, we tell Alpine to set isOpen to true
    // Assuming 'map' is your Mapbox GL JS map instance
    map.on("click", function (e) {
      // Use queryRenderedFeatures to check if a circle was clicked
      const features = map.queryRenderedFeatures(e.point, {
        layers: ["circles"],
      });
      console.info("A circle was clicked", features[0].properties.name);
      if (features.length) {
        window.sidebarComponent.open = true;
      }
    });
  })
  .catch((error) => console.error(error));

// add the Postmarks
fetch("/api/postmarks/")
  .then((response) => response.json())
  .then((data) => {
    console.log("postmarks", data);
    // filter null values
    data = data.filter(function (postmark) {
      return postmark.latitude && postmark.longitude;
    });
    const features = data.map(function (postmark) {
      return {
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [postmark.longitude, postmark.latitude],
        },
        properties: {
          name: postmark.postmark,
        },
      };
    });
    const geojson = {
      type: "FeatureCollection",
      features: features,
    };
    map.addLayer({
      id: "postmarks",
      type: "circle",
      source: {
        type: "geojson",
        data: geojson,
      },
      paint: {
        "circle-radius": 5,
        "circle-color": "red",
        "circle-opacity": 0.75,
      },
    });

    map.on("click", "postmarks", function (e) {
      new mapboxgl.Popup()
        .setLngLat(e.features[0].geometry.coordinates)
        .setHTML(e.features[0].properties.name)
        .addTo(map);
    });
  })
  .catch((error) => console.error(error));

// add the Censors

fetch("/api/censors/")
  .then((response) => response.json())
  .then((data) => {
    console.log("censors", data);
    //filter null lat/lon values
    data = data.filter(function (censor) {
      return censor.latitude && censor.longitude;
    });
    const features = data.map(function (censor) {
      return {
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [censor.longitude, censor.latitude],
        },
        properties: {
          name: censor.censor,
        },
      };
    });
    const geojson = {
      type: "FeatureCollection",
      features: features,
    };
    map.addLayer({
      id: "censors",
      type: "circle",
      source: {
        type: "geojson",
        data: geojson,
      },
      paint: {
        "circle-radius": 15,
        "circle-color": "pink",
        "circle-opacity": 0.75,
      },
    });

    map.on("click", "censors", function (e) {
      new mapboxgl.Popup()
        .setLngLat(e.features[0].geometry.coordinates)
        .setHTML(e.features[0].properties.name)
        .addTo(map);
    });
  })
  .catch((error) => console.error(error));

// draw the routes
fetch("/api/objects/")
  .then((response) => response.json())
  .then((data) => {
    console.log("routes", data);
    // filter null lat/lon values
    data = data.filter(function (route) {
      return (
        route.sender_name.latitude &&
        route.sender_name.longitude &&
        route.addressee_name.latitude &&
        route.addressee_name.longitude
      );
    });
    const features = data.map(function (route) {
      return {
        type: "Feature",
        geometry: {
          type: "LineString",
          coordinates: [
            [route.sender_name.longitude, route.sender_name.latitude],
            [route.addressee_name.longitude, route.addressee_name.latitude],
          ],
        },
        properties: {
          name: route.sender_name + " to " + route.addressee_name,
        },
      };
    });
    const geojson = {
      type: "FeatureCollection",
      features: features,
    };
    map.addLayer({
      id: "routes",
      type: "line",
      source: {
        type: "geojson",
        data: geojson,
      },
      paint: {
        "line-color": "gray",
        "line-opacity": 0.6,
        "line-width": 1,
      },
    });

    hideLoading();
  })
  .catch((error) => console.error(error));