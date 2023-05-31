// async function executarPython() {
//   try {
//     const response = await fetch("http://localhost:5000/executar-python", {
//       method: "POST",
//       headers: {
//         "Content-Type": "image/png",
//       },
//     });

//     if (!response.ok) {
//       throw new Error("Erro na requisição");
//     }

//     const data = await response.json();
//     console.log("Resposta do servidor:", data);
//   } catch (error) {
//     console.error("Erro ao executar o arquivo Python:", error);
//   }
// }

async function executarPython() {
  try {
    const startDate = document.getElementById("startDate").value;
    const endDate = document.getElementById("endDate").value;
    const response = await fetch("http://localhost:5000/executar-python", {
      method: "POST",
      body: JSON.stringify({ startDate, endDate }),
    });

    if (!response.ok) {
      throw new Error("Erro na requisição");
    }

    const data = await response.arrayBuffer();
    const file = new Blob([data], { type: "image/png" });
    const fileURL = URL.createObjectURL(file);

    // Exibir o arquivo na tag <img>
    const imgElement = document.getElementById("imagem");
    imgElement.src = fileURL;
  }  catch (error) {
    console.error("Erro ao executar o arquivo Python:", error);
  }
}

const btn = document.getElementById("osksoks");
btn.addEventListener("click", function (event) {
  event.preventDefault(); // Impede o comportamento padrão do botão
  executarPython();
});
