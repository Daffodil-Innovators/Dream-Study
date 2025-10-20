$(document).ready(function() {
    // Initialize DataTable
    var table = $('#myTable').DataTable({
        drawCallback: function(settings) {
            calculateTotals();
        }
    });

    // Date filter event listeners
    $('#from_date, #to_date').on('change', function() {
        table.draw();
    });

    // Custom filtering function which will filter data based on date range
    $.fn.dataTable.ext.search.push(
        function(settings, data, dataIndex) {
            var dateString = data[2]; // Use data for the date column
          
            var invoiceDate = parseDate(dateString, 'm/d/y');

            var fromDate = $('#from_date').val();
            var toDate = $('#to_date').val();

            // Parse from and to dates
            var from = fromDate ? parseDate(fromDate, 'y-m-d') : null;
            var to = toDate ? parseDate(toDate, 'y-m-d') : null;

            if (
                (from === null && to === null) ||
                (from === null && invoiceDate <= to) ||
                (to === null && invoiceDate >= from) ||
                (invoiceDate >= from && invoiceDate <= to)
            ) {
                return true;
            }
            return false;
        }
    );

    function calculateTotals() {
        var totalAmount = 0;
        var totalPaid = 0;
        var totalDue = 0;

        $('#myTable tbody tr:visible').each(function() {
            var amount = parseFloat($(this).find('td:eq(4)').text()) || 0;
            var paid = parseFloat($(this).find('td:eq(5)').text()) || 0;
            var due = parseFloat($(this).find('td:eq(6)').text()) || 0;

            totalAmount += amount;
            totalPaid += paid;
            totalDue += due;
        });

        $('#totalAmount').text(totalAmount.toFixed(2));
        $('#totalPaid').text(totalPaid.toFixed(2));
        $('#totalDue').text(totalDue.toFixed(2));
    }

    // Initial calculation
    calculateTotals();
});

// Function to parse date strings
function parseDate(dateString, format) {
    var parts = dateString.split('-');
    if (format === 'm/d/y') {
        parts = dateString.split('/');
        var day = parseInt(parts[0], 10);
        var month = parseInt(parts[1], 10) - 1; // Months are zero-based in JavaScript Date object
        var year = parseInt(parts[2], 10);
        return new Date(year, month, day);
    } else if (format === 'y-m-d') {
        var year = parseInt(parts[0], 10);
        var month = parseInt(parts[1], 10) - 1;
        var day = parseInt(parts[2], 10);
        return new Date(year, month, day);
    }
}