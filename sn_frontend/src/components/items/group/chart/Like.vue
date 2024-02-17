<template>
    <canvas id="like" class="w-full"></canvas>
  </template>
  
  <script>
  import axios from "axios";
  import Chart from "chart.js/auto";
  
  export default (await import("vue")).defineComponent({
    components: { Chart },
    setup() {
      let timeFromString = (X) => {
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
  
      const sevenDaysAgo = timeFromString(7).reverse();
      const monthAgo = timeFromString(28).reverse();
      const sixtyDaysAgo = timeFromString(60).reverse();
  
      return {
        sevenDaysAgo,
        monthAgo,
        sixtyDaysAgo,
        timeFromString,
      };
    },
  
    props: {
      setLikesLength: Function,
      selectedDays: String,
    },
  
    data() {
      return {
        likes: [],
        likesChart: null,
      };
    },
  
    mounted() {
      this.getLikesGrowth();
    },
  
    watch: {
      selectedDays(val) {
        if (val) {
          this.likesChart.destroy();
          this.createChart();
        }
      },
    },
  
    methods: {
      getLikesGrowth() {
        axios
          .get(`/api/group/${this.$route.params.id}/growth-likes/`)
          .then((res) => {
            this.likes = res.data.likes
            // console.log(this.likes)
            this.setLikesLength(this.likes.length);
            this.createChart();
          })
          .catch((error) => {
            console.log(error);
          });
      },
      createChart() {
        let likesInSevenDaysData = [];
        let likesInTwentyEightDaysData = [];
        let likesInSixtyDaysData = [];
  
        let timeFrom = (X) => {
          let dates = [];
          for (let I = 0; I < Math.abs(X); I++) {
            dates.push(
              new Date(
                new Date().getTime() -
                  (X >= 0 ? I : I - I - I) * 24 * 60 * 60 * 1000
              )
            );
          }
          return dates;
        };
  
        // 7 days data
        if (this.selectedDays === "7 ngày trước") {
          for (let i = 0; i < timeFrom(7).reverse().length; i++) {
            const length = this.likes.filter(
              (like) =>
                Date.parse(like.created_at) > timeFrom(7).reverse()[i] &&
                Date.parse(like.created_at) < timeFrom(7).reverse()[i + 1]
            ).length;
            const object = {
              x: this.sevenDaysAgo[i],
              y: length,
            };
  
            likesInSevenDaysData.push(object);
          }
        }
  
        // 28 days data
        if (this.selectedDays === "28 ngày trước") {
          for (let i = 27; i >= 0; i -= 7) {
            const length = this.likes.filter(
              (like) =>
                Date.parse(like.created_at) < timeFrom(28).reverse()[i] &&
                Date.parse(like.created_at) > timeFrom(28).reverse()[i - 7]
            ).length;
            const object = {
              x: this.monthAgo[i],
              y: length,
            };
  
            likesInTwentyEightDaysData.push(object);
          }
        }
  
        // 60 days data
        if (this.selectedDays === "60 ngày trước") {
          for (let i = 59; i >= 0; i -= 7) {
            const length = this.likes.filter(
              (like) =>
                Date.parse(like.created_at) < timeFrom(60).reverse()[i] &&
                Date.parse(like.created_at) > timeFrom(60).reverse()[i - 7]
            ).length;
            const object = {
              x: this.sixtyDaysAgo[i],
              y: length,
            };
  
            likesInSixtyDaysData.push(object);
          }
        }
  
        let data;
        let scaleDaysMin;
        let scaleDaysMax;
        let labels
        switch (this.selectedDays) {
          case "7 ngày trước":
            data = likesInSevenDaysData;
            scaleDaysMin = this.sevenDaysAgo[0];
            scaleDaysMax = this.sevenDaysAgo[6];
            labels = this.sevenDaysAgo
            break;
          case "28 ngày trước":
            data = likesInTwentyEightDaysData.reverse();
            scaleDaysMin = this.monthAgo[0];
            scaleDaysMax = this.monthAgo[27];
            labels = [this.monthAgo[0], this.monthAgo[6], this.monthAgo[13], this.monthAgo[20], this.monthAgo[27]]
            break;
          case "60 ngày trước":
            data = likesInSixtyDaysData.reverse();
            scaleDaysMin = this.sixtyDaysAgo[0];
            scaleDaysMax = this.sixtyDaysAgo[59];
            labels = [this.sixtyDaysAgo[0], this.sixtyDaysAgo[10], this.sixtyDaysAgo[17], this.sixtyDaysAgo[24], this.sixtyDaysAgo[31], this.sixtyDaysAgo[38], this.sixtyDaysAgo[45], this.sixtyDaysAgo[52], this.sixtyDaysAgo[59]]
            break;
          default:
            data = likesInSevenDaysData;
            scaleDaysMin = this.sevenDaysAgo[0];
            scaleDaysMax = this.sevenDaysAgo[6];
            labels = this.sevenDaysAgo
            break;
        }
  
        // console.log(data);
        // console.log(scaleDaysMin);
        // console.log(scaleDaysMax);
  
        const config = {
          type: "line",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Cảm xúc",
                backgroundColor: "#28d399",
                borderColor: "#28d399",
                data: data
              },
            ],
          },
          options: {
            scales: {
              x: {
                min: scaleDaysMin,
                max: scaleDaysMax,
              },
              y: {
                min: 0,
                ticks: {
                  stepSize: 1,
                },
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
  
        this.likesChart = new Chart(document.getElementById("like"), config);
        setTimeout(() => {
          Chart.defaults.color = "#ffffff";
          Chart.defaults.borderColor = "#a3987e";
        }, 100);
      },
    },
  });
  </script>
  