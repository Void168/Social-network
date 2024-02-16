<template>
  <canvas id="post" class="w-full"></canvas>
</template>

<script>
import axios from "axios";
import Chart from "chart.js/auto";

export default (await import("vue")).defineComponent({
  name: "groupgrowth",
  components: { Chart },
  setup() {
    let timeFrom = (X) => {
      let dates = [];
      for (let I = 0; I < Math.abs(X); I++) {
        dates.push(
          new Date(
            new Date().getTime() -
              (X >= 0 ? I : I - I - I) * 24 * 60 * 60 * 1000
          ).toLocaleString()
        );
      }
      return dates;
    };

    const sevenDaysAgo = timeFrom(7).reverse();
    const monthAgo = timeFrom(28).reverse();
    return {
      sevenDaysAgo,
      monthAgo,
    };
  },
  data() {
    return {
      chartData: {
        labels: this.sevenDaysAgo,
        datasets: [
          {
            label: "Bài viết",
            backgroundColor: "#f87979",
            borderColor: "#f87979",
            color: "#fff",
            data: [
              {
                x: this.sevenDaysAgo[0],
                y: 50,
              },
              {
                x: this.sevenDaysAgo[1],
                y: 60,
              },
              {
                x: this.sevenDaysAgo[2],
                y: 20,
              },
              {
                x: this.sevenDaysAgo[3],
                y: 50,
              },
              {
                x: this.sevenDaysAgo[4],
                y: 60,
              },
              {
                x: this.sevenDaysAgo[5],
                y: 20,
              },
              {
                x: this.sevenDaysAgo[6],
                y: 20,
              },
            ],
          },
        ],
      },
    };
  },

  mounted() {
    this.getLikesGrowth();
  },

  methods: {
    getLikesGrowth() {
      axios
        .get(`/api/group/${this.$route.params.id}/growth-likes/`)
        .then((res) => {
          console.log(res.data);
          this.createChart();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    createChart() {
      const config = {
        type: "line",
        data: this.chartData,
        options: {
          scales: {
            x: {
              min: this.sevenDaysAgo[0],
            },
            y: {
              min: 0,
            },
          },
          plugins: {
            legend: {
              labels: {
                color: "#fff",
              },
            },
          },
        },
        responsive: true,
        scaleFontColor: "#FFF",
      };

      new Chart(document.getElementById("post"), config);
      setTimeout(() => {
        Chart.defaults.color = "#ffffff";
      }, 100);
    },
  },
});
</script>
