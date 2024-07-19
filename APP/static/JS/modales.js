$(document).ready(function(){
    $("#btnActulizar").click(function(){
        cargarmodal("../modalTare.html");
    });
});

function cargarmodal(){
    $("#Mtareas").load(ruta,function(){
        $("#Mtareas").modal("show");
    })
}