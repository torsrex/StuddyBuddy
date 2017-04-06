/**
 * Created by danny on 05-Apr-17.
 */

function searchFunction() {
    var input, filter, table, tr, td, i;
    input = document.getElementById("searchFunc");
    filter = input.value.toUpperCase();
    table = document.getElementById("topicTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        td2 = tr[i].getElementsByTagName("td")[1];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1 || td2.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}