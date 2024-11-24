document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("trabajoModal");
    const closeModalBtn = document.getElementById("closeModal");
    const statusSelect = document.getElementById("status");
    const inconvenienteSection = document.getElementById("inconvenienteSection");

    // Abrir modal
    window.openModal = function (trabajoId) {
        // Realizar una llamada a Firebase para obtener los detalles del trabajo
        fetch(`/api/trabajos/${trabajoId}`)
            .then((response) => response.json())
            .then((data) => {
                document.getElementById("client_name").value = data.client_name;
                document.getElementById("phone_number").value = data.phone_number;
                document.getElementById("description").value = data.description;
                document.getElementById("service_cost").value = data.service_cost;
                document.getElementById("advance").value = data.advance;
                document.getElementById("remaining").value = data.remaining;
                document.getElementById("review_date").value = data.review_date;
                document.getElementById("status").value = data.status;
                inconvenienteSection.style.display = data.status === "Inconveniente" ? "block" : "none";
            })
            .catch((error) => console.error("Error al cargar los datos:", error));

        modal.style.display = "block";
    };

    // Cerrar modal
    closeModalBtn.onclick = function () {
        modal.style.display = "none";
    };

    // Manejar cambio de estado
    statusSelect.addEventListener("change", function () {
        if (statusSelect.value === "Inconveniente") {
            inconvenienteSection.style.display = "block";
        } else {
            inconvenienteSection.style.display = "none";
        }
    });

    // Guardar cambios
    document.getElementById("saveChanges").onclick = function () {
        // Lógica para guardar los cambios en Firebase
        const updatedData = {
            service_cost: document.getElementById("service_cost").value,
            advance: document.getElementById("advance").value,
            review_date: document.getElementById("review_date").value,
            status: document.getElementById("status").value,
            inconveniente: document.getElementById("inconveniente").value,
        };

        fetch(`/api/trabajos/${trabajoId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(updatedData),
        })
            .then((response) => response.json())
            .then((data) => {
                alert("Cambios guardados correctamente");
                modal.style.display = "none";
            })
            .catch((error) => console.error("Error al guardar los cambios:", error));
    };
});
