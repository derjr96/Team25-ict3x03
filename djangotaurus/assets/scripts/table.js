$(document).ready(function() {
    const tableId = $("table").attr("id");
    const table = $('#'+tableId).DataTable( {
        "dom": 'frti',
        "language": {
            searchPlaceholder: "Search",
            search: "<div class='table-title'>"+tableId.charAt(0).toUpperCase() + tableId.slice(1)+"</div>",
          },
        scrollY:        '60vh',
        responsive:     true,
        deferRender:    true,
        scroller:       true,
        scrollCollapse: true, 
        columnDefs: [
            {
                "targets": [ 0 ],
                "visible": false
            },
            { responsivePriority: 1, targets: 1 },
            { responsivePriority: 2, targets: -1 }
        ],
        "emptyTable": "No data available",
        "zeroRecords": "No matching to records"
    });
    $('.dataTables_filter input').addClass('search');
});
 
