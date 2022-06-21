var amount = document.getElementById('fee_amount')

function changeToAmount(event_name, fees){    
    var id = event_name + "_checkbox"
    var checkbox = document.getElementById(id)
    if(checkbox.checked){
        var totalFee = amount.innerHTML
        totalFee = parseInt(totalFee) + parseInt(fees)
        amount.innerHTML = totalFee
    }
    else{
        var totalFee = amount.innerHTML
        totalFee = parseInt(totalFee) - parseInt(fees)
        amount.innerHTML = totalFee
    }

}




// function validate_form() {
//     var contact_no = document.getElementById("contactno").value;
//     var email = document.getElementById("email").value;
    

//     /* Regex for email and Contact No. validation*/
//     regx_contact_no = /^[6-9][0-9]{9}$/;
//     //regx_email = /^([a-zA-Z\.-+_]+)@([a-zA-Z]+)(.[a-zA-Z]{2,8})(.[a-zA-Z]{2,8}])?$/;
//         regx_email = /^([a-zA-Z0-9\.-\_]+)@([a-zA-Z0-9]+).([a-z]{2,8}).([a-z]{2,8})?$/;

//     if(!regx_contact_no.test(contact_no)){
//         alert("Contact No. is invalid");
//     }


//     if(!regx_email.test(email)){
//         alert("Email ID is invalid");
//     }
// }

