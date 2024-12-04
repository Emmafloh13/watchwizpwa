// calendario.js

$(document).ready(function() {
    // Inicializando FullCalendar
    $('#calendario').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        events: [
            {
                title: 'Evento 1',
                start: '2024-12-05',
                end: '2024-12-05',
                description: 'Descripción del evento 1'
            },
            {
                title: 'Evento 2',
                start: '2024-12-10',
                end: '2024-12-10',
                description: 'Descripción del evento 2'
            }
            // Puedes agregar más eventos aquí
        ],
        eventClick: function(event) {
            alert('Descripción: ' + event.description);
        }
    });

    // Acción para el botón de agregar evento
    $('#agregar').click(function() {
        var title = prompt('Título del evento:');
        var start = prompt('Fecha de inicio (YYYY-MM-DD):');
        var end = prompt('Fecha de fin (YYYY-MM-DD):');

        if (title && start && end) {
            $('#calendario').fullCalendar('renderEvent', {
                title: title,
                start: start,
                end: end
            });
        }
    });
});
