<!-- <template>
  <div id="map"></div>
</template>

<script>
export default (await import("vue")).defineComponent({
  props: {
    query: String,
  },
  data() {
    return {
      map: null,
      service: null,
      infowindow: null,
    };
  },

  mounted() {
    this.initMap();
    this.createMarker();
  },

  methods: {
    initMap() {
      const sydney = new google.maps.LatLng(-33.867, 151.195);

      this.infowindow = new google.maps.InfoWindow();
      this.map = new google.maps.Map(document.getElementById("map"), {
        center: sydney,
        zoom: 15,
      });

      const request = {
        query: this.query,
        fields: ["name", "geometry"],
      };

      this.service = new google.maps.places.PlacesService(this.map);
      this.service.findPlaceFromQuery(request, (results, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK && results) {
          for (let i = 0; i < results.length; i++) {
            this.createMarker(results[i]);
          }

          this.map.setCenter(results[0].geometry.location);
        }
      });
    },

    createMarker(place) {
      if (!place?.geometry || !place?.geometry?.location) return;

      const marker = new google.maps.Marker({
        map: this.map,
        position: place?.geometry?.location,
      });

      google.maps.event.addListener(marker, "click", () => {
        this.infowindow.setContent(place.name || "");
        this.infowindow.open(this.map);
      });
    },
  },
});
</script> -->
