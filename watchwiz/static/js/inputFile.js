document.addEventListener("DOMContentLoaded", () => {
    const inputFile = document.getElementById("id_imagen");
    const preview = document.getElementById("preview");
    const icon = document.getElementById("icon");
    const labelText = document.getElementById("label-text");

    inputFile.addEventListener("change", (event) => {
        const file = event.target.files[0];

        // Verifica que el archivo sea una imagen
        if (file && file.type.startsWith("image/")) {
            const reader = new FileReader();

            // Muestra la vista previa al cargar la imagen
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = "block";
                icon.style.display = "none"; // Oculta el ícono
                labelText.style.display = "none"; // Oculta el texto
            };

            reader.readAsDataURL(file); // Lee el archivo como Data URL
        } else {
            // Restablece el estado si no es una imagen válida
            preview.src = "#";
            preview.style.display = "none";
            icon.style.display = "block"; // Muestra el ícono
            labelText.style.display = "block"; // Muestra el texto
            alert("Por favor, selecciona un archivo de imagen válido.");
        }
    });

    const checkboxes = document.querySelectorAll(".checkweek input[type='checkbox']");

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", function() {
            const parentDiv = checkbox.closest("div");
            if (checkbox.checked) {
                parentDiv.classList.add("checked");
            } else {
                parentDiv.classList.remove("checked");
            }
        });
    });
});
