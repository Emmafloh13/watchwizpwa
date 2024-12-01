document.addEventListener("DOMContentLoaded", function () {
    const btn_lft_lista = document.getElementById("btn-lft-lista");
    const btn_rgt_lista = document.getElementById("btn-rgt-lista");

    const contenedorRL = document.getElementById("contenedorRL");

    const lista_hoy = document.getElementById("lista-hoy");
    const lista_man = document.getElementById("lista-man");

    function vistaLista() {
        btn_lft_lista.classList.toggle("no-mostrar");
        btn_rgt_lista.classList.toggle("no-mostrar");
        btn_lft_lista.classList.toggle("mostrar");

        contenedorRL.classList.toggle("rgt");

        lista_hoy.classList.toggle("no-ver");
        lista_man.classList.toggle("no-ver");
    }

    // btn_lft_lista.addEventListener("click", function () {
    //     console.log("Botón izquierdo clickeado");
    //     btn_lft_lista.classList.toggle("no-mostrar");
    //     btn_rgt_lista.classList.toggle("no-mostrar");
    // });

    // btn_rgt_lista.addEventListener("click", function () {
    //     console.log("Botón derecho clickeado");
    //     btn_lft_lista.classList.toggle("no-mostrar");
    //     btn_rgt_lista.classList.toggle("no-mostrar");
    // });
    btn_rgt_lista.addEventListener("click", vistaLista);
    btn_lft_lista.addEventListener("click", vistaLista);
});
