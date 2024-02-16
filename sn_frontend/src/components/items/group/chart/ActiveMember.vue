<template>
    <canvas id="activeMember" class="w-full"></canvas>
  </template>
  
  <script>
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
              label: "Thành viên hoạt động",
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
      this.createChart();
    },
  
    methods: {
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
          scaleFontColor: "#FFF"
        };
  
        new Chart(document.getElementById("activeMember"), config);
        setTimeout(() => {
            Chart.defaults.color = "#ffffff";
        }, 100)
      },
    },
  });
  </script>
  