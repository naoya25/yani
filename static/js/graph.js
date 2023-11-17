const title = "タバコの本数";
const labels = document.getElementById("labels").value.split(",");
const data = document.getElementById("data").value.split(",");
const ctx = document.getElementById("myChart");

// Create a bar chart using Chart.js
new Chart(ctx, {
  type: "line",
  data: {
    labels: labels,
    datasets: [
      {
        label: "本数",
        data: data,
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      x: {
        title: {
          display: true,
          text: "日付",
        },
      },
      y: {
        title: {
          display: true,
          text: "本数",
        },
        min: 0,
        max: 20,
      },
    },
    plugins: {
      title: {
        display: true,
        text: title,
      },
    },
  },
});
