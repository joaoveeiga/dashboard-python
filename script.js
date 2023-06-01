async function executarPython() {
  try {
    const startDate = document.getElementById("startDate").value;
    const endDate = document.getElementById("endDate").value;
    const url = "http://localhost:5000"

    const functions = [
      () => plot(startDate, endDate, `${url}/plot-bar-chart`, "bar-chart"),
      () => plot(startDate, endDate, `${url}/plot-gaussian`, "gaussian-chart"),
      () => plot(startDate, endDate, `${url}/plot-pie-chart`, "pie-chart"),
    ];

    for (const func of functions) {
      await func();
    }
    
  } catch (error) {
    console.error("Erro ao executar o arquivo Python:", error);
  }
}

async function plot(startDate, endDate, url, id) {
  try {
    const response = await fetch(url, {
      method: "POST",
      body: JSON.stringify({ startDate, endDate }),
    });

    if (!response.ok) {
      throw new Error("Erro na requisição");
    }

    const data = await response.arrayBuffer();
    const file = new Blob([data], { type: "image/png" });
    const fileURL = URL.createObjectURL(file);

    const imgElement = document.getElementById(id);
    imgElement.src = fileURL;
  } catch (error) {
    console.error("Erro ao gerar o gráfico:", error);
  }
}

// const btn = document.getElementById("get-charts-button");
// btn.addEventListener("click", function (event) {
//   event.preventDefault();
//   executarPython();
// });
