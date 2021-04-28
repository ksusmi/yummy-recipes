
// 
// function addRow() {
          
//     var IngredientName = document.getElementById("ingredientname");
//     var units = document.getElementById("units");
//     var quantity = document.getElementById("quantity");
//     var table = document.getElementById("myTableData");
 
//     var rowCount = table.rows.length;
//     var row = table.insertRow(rowCount);
 
//     row.insertCell(0).innerHTML= '<input type="button" value = "Delete" onClick="Javacsript:deleteRow(this)">';
//     row.insertCell(1).innerHTML= IngredientName.value;
//     row.insertCell(2).innerHTML= units.value;
//     row.insertCell(2).innerHTML= quantity .value;
 
// }
 
function deleteRow(obj) {
      
    var index = obj.parentNode.parentNode.rowIndex;
    var table = document.getElementById("myTableData");
    table.deleteRow(index);
    
}

// function addTable() {
      
//     var myTableDiv = document.getElementById("myDynamicTable");
      
//     var table = document.createElement('TABLE');
//     table.border='1';
    
//     var tableBody = document.createElement('TBODY');
//     table.appendChild(tableBody);
      
//     for (var i=0; i<1; i++){
//        var tr = document.createElement('TR');
//        tableBody.appendChild(tr);
       
//        for (var j=0; j<3; j++){
//            var td = document.createElement('TD');
//            td.width='75';
//            td.appendChild(document.createTextNode("Cell " + i + "," + j));
//            tr.appendChild(td);
//        }
//     }
//     myTableDiv.appendChild(table);
    
// }

function addrowtotable(){          
        var IngredientName = document.getElementById("ingredientsId");
        var units = document.getElementById("measureId");
        var quantity = document.getElementById("quantityId");
        var table = document.getElementById("myTableData");
        var ingother = document.getElementById("my-ingredients");

        if (IngredientName.value == ""){
            alert("Select Ingredient");
            return;
        }
        if (quantity.value == ""){
            alert("Enter Ingredient Quantity");
            return;
        }
     
        var rowCount = table.rows.length;
        var row = table.insertRow(rowCount);
        row.id = rowCount
     
        row.insertCell(0).innerHTML= '<input type="button" value = "Delete" onClick="Javacsript:deleteRow(this)">';
        if(IngredientName.value == 1){
            //value = IngredientName.value + "," + units.value + "," + quantity.value + ","+ ingother.value;
            value = IngredientName.value + "," + units.options[units.value].text + "," + quantity.value + ","+ ingother.value;
            row.insertCell(1).innerHTML= ingother.value; 
        }
        else{    
        row.insertCell(1).innerHTML= IngredientName.options[IngredientName.value].text; 
        value = IngredientName.value + "," + units.options[units.value].text + "," + quantity.value;
        }
        row.insertCell(2).innerHTML= units.options[units.value].text;
        row.insertCell(3).innerHTML= quantity.value;
        id = "ingrow" + rowCount;
        // if(IngredientName.value == 1){
        //     var ingother = document.getElementById("my-ingredients");    
        //     value = IngredientName.value + "," + units.value + "," + quantity.value + ","+ ingother.value;
        //     row.insertCell(1).innerHTML= ingother.value;
        //     }
        // else{  
        // value = IngredientName.value + "," + units.value + "," + quantity.value; }
        

        
        addhiddenInput(id,value);
        
        var ingrowelement = document.getElementById("ingrow")

        if(document.getElementById("ingrow") != null) {            
            document. getElementById("ingrow").remove();
        }
        addhiddenInput("ingrow", rowCount);
    }

    function addhiddenInput(id,value){
        var input = document.createElement("input");

        input.setAttribute("type", "hidden");
        
        input.setAttribute("name", id);
        input.setAttribute("id", id);
        input.setAttribute("value", value);
        
        //append to form element that you want .
        document.getElementById("form-submityourrecipe").appendChild(input);

    }
 
function load() {
    
    console.log("Page load finished");
 
}