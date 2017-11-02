"use strict";

$(document).ready(function() {
  console.log("doc ready");
  $("#rating_num").on('keyup', function() {
    let ratingInput = $("#rating_num").val();
    ratingInput = Number(ratingInput);
    if (( isNaN(ratingInput) ) || ( ratingInput < 1 ) || ( ratingInput > 5 )) {
      $("#rating_num_text").html("Digit 1 to 5, please.");
      $("#submit_rating").attr("disabled", true);
    } else {  
      $("#rating_num_text").html("");
      $("#submit_rating").removeAttr("disabled");

    } // end if
  } //end func
  );
} // end func
);